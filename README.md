# text-to-json-demo

Using help from OpenAI, we can make an embedding out of any wiki (such as SRD wikis) or document (such as PDFs)

## How to run

1. Install python (3.9 is what I used) and pip.
1. Install all of the required libraries (pip install -r requirements.txt)
1. Rename secretkey.py.example to secretkey.py and add your OpenAI API key to it
1. Rename templates.py.example to templates.py and change the example to whatever suits your usecase
1. If you would like to use pdf_to_embeddings.py, you need to put at least one pdf in the directory /pdfs/

### Which scripts to use?

* pdf_to_embeddings.py - extracts text from a pdf and saves each page's embeddings to a CSV file
* wiki_to_embeddings.py - extracts text from a wiki and saves each page's embeddings to a CSV file
* ask.py - uses GPT-3.5 to ask a question and returns the answer


## The problem

Data in games takes many forms. For example: statistics for an enemy character's powers/vitality, text displayed as the spoken dialogue of a specific character.

A dataset requires human data entry, or a human editor to tranform it. To make it usable in a piece of software that requires a specific form or syntax of the data, it may need to be cleaned up and transformed.

Often, the dataset is syntactially dirty (inconsistent, extra whitespace, garbage characters). Sometimes the dataset is in a valid format and needs to be converted, which requires expensive developer time that is hard to justify.

## SOTA solution for data transformation

**Data transformation** is a non-generative use of AI. It is generally a three part process:

1. **Data chunking and embedding creation:** The dataset is broken down into smaller pieces according to simple rules, although it often already comes in small pieces. Embeddings are numerical representations of the data, which are important for downstream tasks. We save the embeddings in a database.
1. **Data Retrieval:** We create queries for the model to answer, usually thousands of queries. These queries also get embeddings, and we compare the queries' embeddings to the embeddings in the database to get the most-similar data to each query. We add each query and its associated data to a prompt.
1. **Syntactic transformation:** In our prompt, we task the LLM to transform the data. We give it everything it needs, including a template of how the data will be transformed. The LLM will then apply the transformation to the data, and the completion should look like the original data but in a different format.

## Additional factors

- Fine tuning: There's a small chance the performance of the model can be improved by fine tuning. We give the model at least 100 examples of the data and how we want it to be transformed. The model will learn the transformation from these examples. This method saves a lot of tokens.
- Data augmentation: We can add more data to the dataset to improve the accuracy of the model. This is only going to work if we actually train our own model (not necessary for this project). Augmented data may have the same examples of monsters and items as the original data, but with different formats.

### Import



## Glossary of terms

### Flattened list

A flattened list is a list that has been "flattened" to remove any nested structure. In this case, it refers to a list of subsections where each subsection is represented as a tuple.

### Wiki code

Wiki code refers to the markup language used to format and structure content on a wiki platform, such as Wikipedia. It includes special syntax for headings, links, formatting, and more.

### Tuple

A tuple is an ordered, immutable collection of elements. In this case, each subsection is represented as a tuple, with the first element being a list of parent subtitles and the second element being the text of the subsection.

### Heading

A heading refers to a title or subtitle that is used to organize content within a document or section. In this code, headings are extracted from the Wiki code to identify different subsections.

### Sections to ignore

This refers to a set of sections that should be excluded or not processed when extracting subsections. It allows the function to filter out specific sections based on their titles.

### Parent titles

Parent titles refer to the titles of the sections that are higher in the hierarchy compared to the current section. They are used to keep track of the nested structure of subsections.

### Full text

Full text refers to the complete text content of the given section, including all its subsections and their children.

### Subsection

A subsection is a smaller section within a larger section. In this code, it represents a nested section within the main section.

### Levels

Levels refer to the depth or hierarchy of a section within a structure. In this code, the get_sections method is used with a specific level to retrieve subsections at a particular depth.
