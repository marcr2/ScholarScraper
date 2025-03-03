from fetcher import SemanticScholarFetcher


def test_extract_publication_details():
    fetcher = SemanticScholarFetcher(query="test", max_results=10)
    publication = {
        "title": "Sample Title",
        "abstract": "Sample Abstract",
        "authors": ["Author1", "Author2"],
        "paperId": "12345",
        "citationCount": 10,
        "year": 2021,
    }
    expected_details = [
        "Sample Title",
        ["Author1", "Author2"],
        10,
        2021,
        "12345",
        "Sample Abstract",
    ]
    assert fetcher._extract_publication_details(publication) == expected_details
