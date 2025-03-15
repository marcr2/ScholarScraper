import time
import pandas as pd
import requests
from tqdm import tqdm
import json
with open('keys.json', 'r') as f:
    keys = json.load(f)
semantics_scholar_api_key = keys['semantics_scholar_api_key']

class SemanticScholarFetcher:
    def __init__(self, query, max_results, output_path="output.csv"):
        # Initialize fetcher configuration
        self.query = query
        self.max_results = max_results
        self.output_path = output_path
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.headers = {"x-api-key": semantics_scholar_api_key}
        self.results = pd.DataFrame(
            [],
            columns=[
                "title",
                "authors",
                "num_citations",
                "pub_year",
                "pub_id",
                "abstract",
            ],
        )

    def _extract_publication_details(self, publication):
        # Process publication data
        title = publication["title"]
        abstract = publication["abstract"]
        authors = publication["authors"]
        pub_id = publication["paperId"]
        num_citations = publication["citationCount"]
        pub_year = publication["year"]
        return [title, authors, num_citations, pub_year, pub_id, abstract]

    def fetch(self):
        offset = 0
        limit = 10
        max_retries = 5
        retry_wait_time = 62

        with tqdm(
            total=self.max_results,
            desc="Fetching papers",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            colour="WHITE",
        ) as pbar:
            while len(self.results) < self.max_results:
                retries = 0
                response = None
                while retries < max_retries:
                    params = {
                        "query": self.query,
                        "offset": offset,
                        "limit": limit,
                        "fields": "title,authors,year,citationCount,paperId,abstract",
                    }
                    response = requests.get(self.base_url, headers=self.headers, params=params, timeout=30)
                    if response.status_code == 200:
                        break
                    else:
                        print(
                            f"Error: {response.status_code} - {response.text}. Retrying in {retry_wait_time} seconds..."
                        )
                        retries += 1
                        time.sleep(retry_wait_time)
                if retries == max_retries or not response:
                    print("Max retries reached or no response. Exiting.")
                    break
                data = response.json()
                if not data.get("data"):
                    break
                papers_added = 0
                for paper in data["data"]:
                    processed_result = self._extract_publication_details(paper)
                    self.results.loc[len(self.results)] = processed_result
                    papers_added += 1
                    self.results.to_csv(self.output_path, index=False)
                pbar.update(papers_added)
                offset += len(data["data"])
                if len(self.results) < self.max_results:
                    time.sleep(10)  # Respect API rate limits
                elif len(self.results) == self.max_results:
                    print(f"Finished fetching. Caught {len(self.results)} articles!")
                    break
                elif offset >= 1000:
                    print(f"Reached maximum offset of 1000. Exiting with {len(self.results)}.")
                    break
                else:
                    print(f"Caught {len(self.results)} articles!")
                    break
        return self.results
