from fetcher import fetch_semantic_scholar_abstracts
from llm import processWSData, llmRead
from scorer import processLLMData
from visualizer import plotData

query = input("What is your query? ")
max_results = int(input("How many articles would you like to fetch? "))
processType = input("Will you be using LLM or NLP? ")
field = input(
    "What field is your research in? (Ie. molecular biology, machine learning)"
)
target_object = input(
    "What would you like to group by? (Ie. treatment option, deep learning algorithm) "
)

fetch_semantic_scholar_abstracts(query, max_results)  # scrape articles
import_data = processWSData(processType)  # set up for LLM/NLP
processed_data = llmRead(
    import_data, field, target_object
)  # categorize articles using LLM
scored_data = processLLMData(processed_data)
print(scored_data.head())
plotData(scored_data)  # visualize data
