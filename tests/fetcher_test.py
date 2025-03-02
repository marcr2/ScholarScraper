import pytest

from fetcher import processSearch


def test_processSearch():
    publication = {
        "title": "Sample Title",
        "abstract": "Sample Abstract",
        "authors": ["Author1", "Author2"],
        "paperId": "12345",
        "citationCount": 10,
        "year": 2021,
    }
    expected_result = [
        "Sample Title",
        ["Author1", "Author2"],
        10,
        2021,
        "12345",
        "Sample Abstract",
    ]
    assert processSearch(publication) == expected_result


def test_processSearch_missing_fields():
    publication = {
        "title": "Sample Title",
        "abstract": "Sample Abstract",
        "authors": ["Author1", "Author2"],
        "paperId": "12345",
        "citationCount": 10,
        "year": 2021,
    }
    del publication["abstract"]
    with pytest.raises(KeyError):
        processSearch(publication)
