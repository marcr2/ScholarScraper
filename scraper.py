import requests
import time
import pandas as pd
from tqdm import tqdm
import json

def processSearch(publication): # collect data from fetched publication
  title = publication["title"]
  abstract = publication["abstract"]
  authors = publication["authors"]
  pub_id = publication["paperId"]
  num_citations = publication["citationCount"]
  pub_year = publication["year"]
  processed_pub = [title, authors, num_citations, pub_year, pub_id, abstract]
  return processed_pub

def fetch_semantic_scholar_abstracts(query, max_results):
    base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
    headers = {"Accept": "application/json"}
    rows = []
    final_list = pd.DataFrame(rows, columns=["title", "authors", "num_citations", "pub_year", "pub_id", "abstract"])
    offset = 0
    limit = 100
    papers_added = 0
    max_retries = 5
    retry_wait_time = 60  # wait time in seconds before retrying
    with tqdm(
        total=max_results,
        desc="Fetching papers",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
        colour="WHITE"
    ) as pbar:
        while len(final_list) < max_results: # send request for publications
            retries = 0
            while retries < max_retries:
                params = {
                    "query": query,
                    "offset": offset,
                    "limit": limit,
                    "fields": "title,authors,year,citationCount,paperId,abstract"
                }
                response = requests.get(base_url, headers=headers, params=params)
                if response.status_code == 200:
                    break
                else:
                    print(f"Error: {response.status_code} - {response.text}. Retrying in {retry_wait_time} seconds...")
                    retries += 1
                    time.sleep(retry_wait_time)
            if retries == max_retries:
                print("Max retries reached. Exiting.")
                break
            data = response.json()
            if not data.get("data"):
                break
            for paper in data["data"]: # processes response and adds to pandas dataframe
                if paper.get("abstract"):
                    processed_result = processSearch(paper)
                    final_list.loc[len(final_list)] = processed_result
                    papers_added += 1
                    final_list.to_csv('output.csv', index=False)
            pbar.update(papers_added)
            papers_added = 0
            offset += len(data["data"])
            if len(final_list) < max_results: # only waits if needed
                time.sleep(300)  # rate limit is 100 requests per 5 minutes
            else:
                print(f"Caught {len(final_list)} articles!")
                break