# ScholarScraper

This project uses Semantic Scholar’s /paper/search endpoint to collect publications via keyword queries, extracting title, abstract, year, and citationCount to **identify under-researched topics**.

An NLP module will analyze abstracts to detect the primary object/research focus (e.g., specific materials, molecules, or phenomena). Low-citation papers, recent publications, and recurring but underexplored terms in abstracts highlight research gaps.

## Features

- **Keyword-based Search**: Utilize Semantic Scholar’s API to perform keyword-based searches, retrieving relevant publications efficiently.
- **Metadata Extraction**: Extract essential metadata such as title, abstract, year, and citation count to facilitate analysis.
- **NLP Analysis**: Implement natural language processing to analyze abstracts and identify primary research focuses and underexplored topics.
- **Citation Analysis**: Highlight low-citation and recent publications to pinpoint potential research gaps.
- **Efficient Data Handling**: Employ techniques like pagination, rate limiting, and early filtering to ensure compliance with API guidelines and optimize data processing.
- **Incremental Saving**: Save results incrementally to a CSV file to ensure data persistence and minimize redundancy.

These features collectively enable systematic identification of research gaps, supporting small research teams in their exploration of niche domains.

## Third Party API Guidelines enforcement

The project reduces payload size while retaining essential metadata for analysis by extracting only 6 fields and using 1 endpoint. This design targets small research teams analyzing niche domains, with an estimated monthly usage of 1,000–3,000 requests to accommodate iterative exploration of understudied topics.

The following techniques are used to maintain efficiency and compliance with API guidelines:

- Pagination is implemented by configuring offset and limit parameters to retrieve 100 papers per request, balancing batch size with responsiveness.

- Rate limits are strictly adhered to by enforcing a delay after each batch, aligning with Semantic Scholar’s allowance.

- Early filtering occurs during data parsing, where papers lacking abstracts are automatically skipped to streamline downstream processing and focus only on actionable data.

- Incremental saving appends results to a CSV file during each loop iteration, minimizing redundant data handling and ensuring progress persistence even if interruptions occur.

This structure prioritizes scalability, compliance, and resource efficiency while enabling systematic identification of research gaps through NLP-driven abstract analysis.

## Development Environment Setup

To set up the development environment, follow these steps:

1. **Create a virtual environment**:

    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment**:
    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

3. **Install the required packages**:

    ```bash
    pip install -r requirements.txt
    ```

By following these steps, you will have a virtual environment with all the necessary dependencies installed for the project.
