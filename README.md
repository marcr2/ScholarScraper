This project uses Semantic Scholar’s /paper/search endpoint to collect publications via keyword queries, extracting title, abstract, year, and citationCount to identify under-researched topics. An NLP module will analyze abstracts to detect the primary object/research focus (e.g., specific materials, molecules, or phenomena). Low-citation papers, recent publications, and recurring but underexplored terms in abstracts highlight research gaps.

The project reduces payload size while retaining essential metadata for analysis by extracting only 6 fields and using 1 endpoint. This design targets small research teams analyzing niche domains, with an estimated monthly usage of 1,000–3,000 requests to accommodate iterative exploration of understudied topics.

The following techniques are used to maintain efficiency and compliance with API guidelines:

- Pagination is implemented by configuring offset and limit parameters to retrieve 100 papers per request, balancing batch size with responsiveness.

- Rate limits are strictly adhered to by enforcing a delay after each batch, aligning with Semantic Scholar’s allowance.

- Early filtering occurs during data parsing, where papers lacking abstracts are automatically skipped to streamline downstream processing and focus only on actionable data.

- Incremental saving appends results to a CSV file during each loop iteration, minimizing redundant data handling and ensuring progress persistence even if interruptions occur.

This structure prioritizes scalability, compliance, and resource efficiency while enabling systematic identification of research gaps through NLP-driven abstract analysis.
