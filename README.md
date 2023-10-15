# wiki-to-embedding

Using help from OpenAI, we can make an embedding out of any wiki (such as SRD wikis)

## How it works

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
