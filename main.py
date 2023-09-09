# imports
import mwclient  # for downloading example Wiki articles
import mwparserfromhell  # for splitting Wiki articles into sections
import openai  # for generating embeddings
import pandas as pd  # for DataFrames to store article sections and embeddings
import re  # for cutting <ref> links out of Wiki articles
import tiktoken  # for counting tokens
from secretkey import openai_secret_key

# get Wiki pages about OSE monsters

CATEGORY_TITLE = "Category:Monsters"
WIKI_HOSTNAME = "oldschoolessentials.necroticgnome.com"
WIKI_PATH = "/srd/"

openai.api_key = openai_secret_key


# This code defines a function titles_from_category that takes a Wiki
# category and a maximum depth as input. It returns a set of page
# titles in the given category and its subcategories. The function
# iterates over the members of the category and adds the names of pages
# to the set. If a member is a subcategory and the maximum depth has not
# been reached, the function recursively calls itself to retrieve the
# titles from the subcategory and updates the set. The resulting set of
# titles is returned.
def titles_from_category(
    category: mwclient.listing.Category, max_depth: int
) -> set[str]:
    """Return a set of page titles in a given Wiki category and its subcategories."""
    titles = set()
    for cm in category.members():
        if type(cm) == mwclient.page.Page:
            # ^type() used instead of isinstance() to catch match w/ no inheritance
            titles.add(cm.name)
        elif isinstance(cm, mwclient.listing.Category) and max_depth > 0:
            deeper_titles = titles_from_category(cm, max_depth=max_depth - 1)
            titles.update(deeper_titles)
    return titles


site = mwclient.Site(host=WIKI_HOSTNAME, path=WIKI_PATH)
category_page = site.pages[CATEGORY_TITLE]
titles = titles_from_category(category_page, max_depth=0)
# ^note: max_depth=1 means we go one level deep in the category tree
print(f"Found {len(titles)} article titles in {CATEGORY_TITLE}.")

# define functions to split Wiki pages into sections

SECTIONS_TO_IGNORE = []

# This code defines a function all_subsections_from_section
# that takes in a section of Wiki code, a list of parent_titles,
# and a sections_to_ignore set. The function returns a flattened
# list of all nested subsections within the given section.

# Each subsection is represented as a tuple, where the first element
# is a list of parent subtitles (starting with the page title) and
# the second element is the text of the subsection
# (excluding any children).

# The function first extracts the headings from the section and
# checks if the first heading is in the sections_to_ignore set.
# If it is, an empty list is returned.

# Otherwise, the function builds the titles list by combining
# the parent_titles with the current title. It then extracts
# the full text of the section and splits it to get the text
# of the current section.

# If there is only one heading, the function returns a list containing
# a tuple of the titles and section_text. Otherwise, it extracts
# the first subtitle, splits the section_text to remove any text
# after the first subtitle, and initializes a results list with a
# tuple representing the current section.

# The function then iterates over the subsections of the section
# (using get_sections) with a level greater than the length of the
# titles. For each subsection, it recursively calls the
# all_subsections_from_section function and extends the results
# list with the returned subsections.

# Finally, the function returns the results list containing all
# the subsections of the section.
def all_subsections_from_section(
    section: mwparserfromhell.wikicode.Wikicode,
    parent_titles: list[str],
    sections_to_ignore: set[str],
) -> list[tuple[list[str], str]]:
    """
    From a Wiki section, return a flattened list of all nested subsections.
    Each subsection is a tuple, where:
        - the first element is a list of parent subtitles, starting with the page title
        - the second element is the text of the subsection (but not any children)
    """
    headings = [str(h) for h in section.filter_headings()]
    title = headings[0]
    if title.strip("=" + " ") in sections_to_ignore:
        # ^wiki headings are wrapped like "== Heading =="
        return []
    titles = parent_titles + [title]
    full_text = str(section)
    section_text = full_text.split(title)[1]
    if len(headings) == 1:
        return [(titles, section_text)]
    else:
        first_subtitle = headings[1]
        section_text = section_text.split(first_subtitle)[0]
        results = [(titles, section_text)]
        for subsection in section.get_sections(levels=[len(titles) + 1]):
            results.extend(all_subsections_from_section(subsection, titles, sections_to_ignore))
        return results

# This code defines a function all_subsections_from_title
# that takes a title as input and returns a list of
# all nested subsections from a Wiki page. Each subsection
# is represented as a tuple, where the first element is a list
# of parent subtitles and the second element is the text of
# the subsection. The function uses the mwclient library to
# interact with the Wiki API and mwparserfromhell library
# to parse the text of the Wiki page. It recursively calls
# the all_subsections_from_section function to process each
# subsection and build the result list.
def all_subsections_from_title(
    title: str,
    sections_to_ignore: set[str] = SECTIONS_TO_IGNORE,
) -> list[tuple[list[str], str]]:
    """From a Wiki page title, return a flattened list of all nested subsections.
    Each subsection is a tuple, where:
        - the first element is a list of parent subtitles, starting with the page title
        - the second element is the text of the subsection (but not any children)
    """
    site = mwclient.Site(WIKI_HOSTNAME, WIKI_PATH)
    page = site.pages[title]
    text = page.text()
    parsed_text = mwparserfromhell.parse(text)
    headings = [str(h) for h in parsed_text.filter_headings()]
    if headings:
        summary_text = str(parsed_text).split(headings[0])[0]
    else:
        summary_text = str(parsed_text)
    results = [([title], summary_text)]
    for subsection in parsed_text.get_sections(levels=[2]):
        results.extend(all_subsections_from_section(subsection, [title], sections_to_ignore))
    return results

# split pages into sections
# may take ~1 minute per 100 articles
wiki_sections = []
for title in titles:
    wiki_sections.extend(all_subsections_from_title(title))
print(f"Found {len(wiki_sections)} sections in {len(titles)} pages.")

# This code defines a function called clean_section that takes
# a tuple containing a list of titles and a text string as input.
# The function removes any occurrences of <ref>xyz</ref> patterns
# from the text and removes leading and trailing whitespace.
# It then returns the updated titles and text as a tuple.
def clean_section(section: tuple[list[str], str]) -> tuple[list[str], str]:
    """
    Return a cleaned up section with:
        - <ref>xyz</ref> patterns removed
        - leading/trailing whitespace removed
    """
    titles, text = section
    text = re.sub(r"<ref.*?</ref>", "", text)
    text = text.strip()
    return (titles, text)


wiki_sections = [clean_section(ws) for ws in wiki_sections]

# This code defines a function called keep_section
# that takes a tuple as input. The tuple contains a list of titles
# and a text. The function checks if the length of the text is
# less than 16 characters. If it is, the function returns False,
# indicating that the section should not be kept. Otherwise,
# it returns True, indicating that the section should be kept.
def keep_section(section: tuple[list[str], str]) -> bool:
    """Return True if the section should be kept, False otherwise."""
    titles, text = section
    if len(text) < 16:
        return False
    else:
        return True


original_num_sections = len(wiki_sections)
wiki_sections = [ws for ws in wiki_sections if keep_section(ws)]
print(f"Filtered out {original_num_sections-len(wiki_sections)} sections, leaving {len(wiki_sections)} sections.")

# print example data
for ws in wiki_sections[:5]:
    print(ws[0])

GPT_MODEL = "gpt-3.5-turbo"  # only matters insofar as it selects which tokenizer to use

# This code defines a function called num_tokens that takes a
# string text and an optional string model as input. It uses the
# tiktoken library to encode the text using the specified model and
# then returns the number of tokens in the encoded text.
def num_tokens(text: str, model: str = GPT_MODEL) -> int:
    """Return the number of tokens in a string."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

# This code defines a function called halved_by_delimiter that splits
# a string into two parts based on a delimiter. It tries to balance
# the tokens on each side of the delimiter. If there is only one chunk
# (no delimiter found), it returns the original string and an empty
# string. If there are two chunks, it simply returns those chunks.
# Otherwise, it calculates the halfway point based on the number of
# tokens in the string and iterates over the chunks to find the best
# split point. It returns the left and right parts of the string split
# at the optimal split point.
def halved_by_delimiter(string: str, delimiter: str = "\n") -> list[str, str]:
    """Split a string in two, on a delimiter, trying to balance tokens on each side."""
    chunks = string.split(delimiter)
    if len(chunks) == 1:
        return [string, ""]  # no delimiter found
    elif len(chunks) == 2:
        return chunks  # no need to search for halfway point
    else:
        total_tokens = num_tokens(string)
        halfway = total_tokens // 2
        best_diff = halfway
        for i, chunk in enumerate(chunks):
            left = delimiter.join(chunks[: i + 1])
            left_tokens = num_tokens(left)
            diff = abs(halfway - left_tokens)
            if diff >= best_diff:
                break
            else:
                best_diff = diff
        left = delimiter.join(chunks[:i])
        right = delimiter.join(chunks[i:])
        return [left, right]

# This code defines a function called truncated_string
# that takes in a string to be truncated, a model for encoding,
# a maximum number of tokens (max_tokens), and an optional flag
# to print a warning. The function uses the tiktoken library to
# encode the string and then truncates it to max_tokens tokens.
# If the print_warning flag is set to True and the encoded string
# is longer than max_tokens, it prints a warning message. The
# function returns the truncated string.
def truncated_string(
    string: str,
    model: str,
    max_tokens: int,
    print_warning: bool = True,
) -> str:
    """Truncate a string to a maximum number of tokens."""
    encoding = tiktoken.encoding_for_model(model)
    encoded_string = encoding.encode(string)
    truncated_string = encoding.decode(encoded_string[:max_tokens])
    if print_warning and len(encoded_string) > max_tokens:
        print(f"Warning: Truncated string from {len(encoded_string)} tokens to {max_tokens} tokens.")
    return truncated_string

# This code defines a function split_strings_from_subsection
# that takes a subsection (a tuple of parent titles and text)
# and splits it into a list of subsections, each with no more
# than max_tokens tokens. It uses recursion to split the
# subsection into smaller halves until the maximum token limit
# is reached or until a maximum recursion depth is reached.
# If no split is found, it truncates the subsection.
def split_strings_from_subsection(
    subsection: tuple[list[str], str],
    max_tokens: int = 1000,
    model: str = GPT_MODEL,
    max_recursion: int = 5,
) -> list[str]:
    """
    Split a subsection into a list of subsections, each with no more than max_tokens.
    Each subsection is a tuple of parent titles [H1, H2, ...] and text (str).
    """
    titles, text = subsection
    string = "\n\n".join(titles + [text])
    num_tokens_in_string = num_tokens(string)
    # if length is fine, return string
    if num_tokens_in_string <= max_tokens:
        return [string]
    # if recursion hasn't found a split after X iterations, just truncate
    elif max_recursion == 0:
        return [truncated_string(string, model=model, max_tokens=max_tokens)]
    # otherwise, split in half and recurse
    else:
        titles, text = subsection
        for delimiter in ["\n\n", "\n", ". "]:
            left, right = halved_by_delimiter(text, delimiter=delimiter)
            if left == "" or right == "":
                # if either half is empty, retry with a more fine-grained delimiter
                continue
            else:
                # recurse on each half
                results = []
                for half in [left, right]:
                    half_subsection = (titles, half)
                    half_strings = split_strings_from_subsection(
                        half_subsection,
                        max_tokens=max_tokens,
                        model=model,
                        max_recursion=max_recursion - 1,
                    )
                    results.extend(half_strings)
                return results
    # otherwise no split was found, so just truncate (should be very rare)
    return [truncated_string(string, model=model, max_tokens=max_tokens)]

# split sections into chunks
MAX_TOKENS = 1600
wiki_strings = []
for section in wiki_sections:
    wiki_strings.extend(split_strings_from_subsection(section, max_tokens=MAX_TOKENS))


print(f"{len(wiki_sections)} wiki sections split into {len(wiki_strings)} strings.")

# print example data
print(wiki_strings[1])

# calculate embeddings
EMBEDDING_MODEL = "text-embedding-ada-002"  # OpenAI's best embeddings as of Apr 2023
BATCH_SIZE = 1000  # you can submit up to 2048 embedding inputs per request

embeddings = []
for batch_start in range(0, len(wiki_strings), BATCH_SIZE):
    batch_end = batch_start + BATCH_SIZE
    batch = wiki_strings[batch_start:batch_end]
    print(f"Batch {batch_start} to {batch_end-1}")
    response = openai.Embedding.create(model=EMBEDDING_MODEL, input=batch)
    for i, be in enumerate(response["data"]):
        assert i == be["index"]  # double check embeddings are in same order as input
    batch_embeddings = [e["embedding"] for e in response["data"]]
    embeddings.extend(batch_embeddings)

df = pd.DataFrame({"text": wiki_strings, "embedding": embeddings})

# save document chunks and embeddings

SAVE_PATH = "data/ose_monsters.csv"

df.to_csv(SAVE_PATH, index=False)