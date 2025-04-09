import time
import pandas as pd
import requests
import json
from tqdm import tqdm

with open('keys.json', 'r') as f:
    keys = json.load(f)

semantics_scholar_api_key = keys['semantics_scholar_api_key']

class SemanticScholarFetcher:
    def __init__(self, query, max_results, output_path="output.csv"):
        self.query = query
        self.max_results = max_results
        self.output_path = output_path
        self.base_url = "https://api.semanticscholar.org/graph/v1/paper/search"
        self.headers = {"x-api-key": semantics_scholar_api_key}
        self.results = pd.DataFrame(columns=[
            "title", "authors", "num_citations", "pub_year", "pub_id", "abstract"
        ])

    def _extract_publication_details(self, publication):
        return [
            publication.get("title"),
            publication.get("authors"),
            publication.get("citationCount"),
            publication.get("year"),
            publication.get("paperId"),
            publication.get("abstract")
        ]

    def fetch(self, progress_callback=None):
        offset = 0
        limit = 10
        max_retries = 5
        retry_wait_time = 62
        articles_fetched = 0

        with tqdm(
            total=self.max_results,
            desc="Fetching papers",
            bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
            colour="WHITE",
        ) as pbar:
            while articles_fetched < self.max_results and offset < 1000:
                retries = 0
                while retries < max_retries:
                    params = {
                        "query": self.query,
                        "offset": offset,
                        "limit": limit,
                        "fields": "title,authors,year,citationCount,paperId,abstract",
                    }
                    try:
                        response = requests.get(
                            self.base_url,
                            headers=self.headers,
                            params=params,
                            timeout=30
                        )
                        if response.status_code == 200:
                            break
                    except Exception as e:
                        print(f"Request exception: {e}")

                    retries += 1
                    print(f"Retrying in {retry_wait_time} seconds...")
                    time.sleep(retry_wait_time)

                if retries == max_retries or not response or response.status_code != 200:
                    print("Max retries reached or invalid response.")
                    break

                data = response.json()
                papers = data.get("data", [])
                if not papers:
                    print("No papers returned. Exiting.")
                    break

                for paper in papers:
                    if articles_fetched >= self.max_results:
                        break
                    self.results.loc[len(self.results)] = self._extract_publication_details(paper)
                    articles_fetched += 1
                    if progress_callback:
                        progress_callback(articles_fetched, self.max_results)
                    pbar.update(1)

                offset += len(papers)
                time.sleep(10)  # Respect rate limits

        print(f"Fetched {len(self.results)} articles.")
        self.results.to_csv(self.output_path, index=False)
        return self.results
