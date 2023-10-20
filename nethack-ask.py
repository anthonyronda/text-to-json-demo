# imports
import ast  # for converting embeddings saved as strings back to arrays
import openai  # for calling the OpenAI API
import pandas as pd  # for storing text and embeddings data
import tiktoken  # for counting tokens
from scipy import spatial  # for calculating vector similarities for search
from secretkey import openai_secret_key
from templates import nethack_monster_template

# json template
json_template='''
{
        "hp": {
          "hd": "a string such as \"1d8\" where 1 is the number of dice and 8 is the number of sides",
          "value": average hp as integer,
          "max": average hp as integer
        },
        "ac": {
          "value": ac as integer,
          "mod": stat-based modifier for ac as integer
        },
        "aac": {
          "value": aac as integer,
          "mod": stat-based modifier for aac as integer
        },
        "thac0": {
          "value": thac0 as integer,
          "bba": the number inside the brackets of thac0 as integer,
          "mod": {
            "missile": 0,
            "melee": 0
          }
        },
        "saves": {
          "death": {
            "value": the number after D in saving throws as integer
          },
          "wand": {
            "value": the number after W in saving throws as integer
          },
          "paralysis": {
            "value": the number after P in saving throws as integer
          },
          "breath": {
            "value": the number after B in saving throws as integer
          },
          "spell": {
            "value": the number after S in saving throws as integer
          }
        },
        "movement": {
          "base": the first number in the movement string as integer
        },
        "initiative": {
          "value": 0,
          "mod": 0
        }
      },
        "details": {
        "biography": "",
        "alignment": "",
        "xp": 0,
        "specialAbilities": the number of asterisks after the HD number as integer,
        "treasure": {
          "table": "the string "Table _" where the blank is the letter after tt",
          "type": ""
        },
        "appearing": {
          "d": "a string for number appearing such as \"1d8\" where 1 is the number of dice and 8 is the number of sides",
          "w": "a string inside the parentheses for number appearing such as \"1d8\" where 1 is the number of dice and 8 is the number of sides",
        },
        "morale": the number after ml as integer
      },
      "attacks": ""
}
      '''


# models
EMBEDDING_MODEL = "text-embedding-ada-002"
GPT_MODEL = "gpt-3.5-turbo"

openai.api_key = openai_secret_key


# download pre-chunked text and pre-computed embeddings
# this file is ~200 MB, so may take a minute depending on your connection speed
embeddings_path = "data/nethack_monsters.csv"

df = pd.read_csv(embeddings_path)

# convert embeddings from CSV str type back to list type
df['embedding'] = df['embedding'].apply(ast.literal_eval)

# This code defines a function called strings_ranked_by_relatedness
# that takes a query string, a pandas DataFrame, a relatedness function,
# and a number top_n as arguments. The function uses an embedding
# model to calculate the similarity between the query string and each
# string in the DataFrame. It then sorts the strings based on their
# relatedness to the query and returns the top top_n strings along with
# their relatedness scores.
def strings_ranked_by_relatedness(
    query: str,
    df: pd.DataFrame,
    relatedness_fn=lambda x, y: 1 - spatial.distance.cosine(x, y),
    top_n: int = 100
) -> tuple[list[str], list[float]]:
    """Returns a list of strings and relatednesses, sorted from most related to least."""
    query_embedding_response = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=query,
    )
    query_embedding = query_embedding_response["data"][0]["embedding"]
    strings_and_relatednesses = [
        (row["text"], relatedness_fn(query_embedding, row["embedding"]))
        for i, row in df.iterrows()
    ]
    strings_and_relatednesses.sort(key=lambda x: x[1], reverse=True)
    strings, relatednesses = zip(*strings_and_relatednesses)
    return strings[:top_n], relatednesses[:top_n]

# This code defines a function called num_tokens that takes a string
# text and an optional string model as input. It uses the tiktoken
# library to encode the text using the specified model and then returns
# the number of tokens in the encoded string.
def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# This code defines a function called query_message that takes in four
# parameters: query (a string), df (a pandas DataFrame), model
# (a string), and token_budget (an integer). The function returns
# a message for the GPT model, with relevant source texts pulled from
# the DataFrame.

# The function starts by calling a helper function
# strings_ranked_by_relatedness to get a list of strings and their
# relatedness scores based on the query and the DataFrame. Then,
# it defines an introduction string and a question string based
# on the query.

# The function then iterates through the list of strings and appends
# each string to the message if the total number of tokens (including
# the message, the next article, and the question) is within the
# token budget. If the token budget is exceeded, the loop breaks.
# Finally, the function returns the message concatenated with the
# question.
def query_message(
    query: str,
    df: pd.DataFrame,
    model: str,
    token_budget: int
) -> str:
    """Return a message for GPT, with relevant source texts pulled from a dataframe."""
    strings, relatednesses = strings_ranked_by_relatedness(query, df)
    introduction = 'For each line of the JSON template, if a key-value description is present, replace that description with the relevant data in provided wiki articles about the provided monster. SPECIAL INSTRUCTION: also translate all text to Polish language. If no key-value description is present, or confidence is low, leave the line as-is.'
    question = f"\n\nMONSTER: {query}"
    template = f"\n\nJSON template:\n{nethack_monster_template}"
    message = introduction
    for string in strings:
        next_article = f'\n\nWiki article section:\n"""\n{string}\n"""'
        if (
            num_tokens(message + template + next_article + question, model=model)
            > token_budget
        ):
            break
        else:
            message += next_article
    return message + template + question

# This code defines a function called ask that takes in a
# query string, a pandas DataFrame, a model name, a token budget,
# and a boolean flag for printing a message. It returns a string
# as the response message. The function uses the query_message
# function to create a message based on the query, DataFrame,
# model, and token budget. If the print_message flag is set to
# true, the message is printed. Then, a list of messages is
# created with a system message and the user message. The
# openai.ChatCompletion.create method is called to generate a
# response using the specified model and messages. The response
# message is extracted and returned.
def ask(
    query: str,
    df: pd.DataFrame = df,
    model: str = GPT_MODEL,
    token_budget: int = 4096 - 500,
    print_message: bool = False,
) -> str:
    """Answers a query using GPT and a dataframe of relevant texts and embeddings."""
    message = query_message(query, df, model=model, token_budget=token_budget)
    if print_message:
        print(message)
    messages = [
        {"role": "system", "content": "You input data about role playing game monsters into the provided JSON template."},
        {"role": "user", "content": message},
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0
    )
    response_message = response["choices"][0]["message"]["content"]
    print(response_message)
    return response_message

ask("Gelatinous Cube")
ask("Zruty")

# Foundry VTT Game Compendium GitHub Action Lifecycle
#
# 1. Repo owner creates a new release on the repo
# 2. Action starts, checks out code from repo

# 3. Action gets the latest wiki pages using mwclient
# 3. Action stores the titles of the wiki pages
# 4. Action splits the wiki pages into sections
# 5. Action counts the number of tokens in each section
# 6. Action filters out irrelevant sections
# 7. Action creates an embedding for each section and enters it into the database
# 8. For each title in the titles list, Action queries the OpenAI API using title and provided JSON template
