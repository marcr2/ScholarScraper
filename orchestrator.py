
from fetcher import SemanticScholarFetcher
from llm import processWSData, llmRead
from scorer import processLLMData
from visualizer import plotData
import time
import streamlit as st

def run_pipeline_with_progress(query, max_results, process_type, field, target_object, is_cancelled):
    # Step 1: Fetching
    yield "fetch", "Starting...", 0, "..."
    fetcher = SemanticScholarFetcher(query, max_results)
    results = []
    start_time = time.time()

    for i, paper in enumerate(fetcher.fetch()):
        if is_cancelled():
            return
        results.append(paper)
        percent = int((i + 1) / max_results * 100)
        elapsed = time.time() - start_time
        eta = int((elapsed / (i + 1)) * (max_results - (i + 1)))
        eta_str = f"{eta}s remaining" if eta > 0 else "almost done"
        yield "fetch", f"Fetched {i+1}/{max_results} articles...", percent, eta_str

    # ✅ Store fetched data in session state
    st.session_state.fetched_data = results
    yield "fetch", "Done", 100, "✔️"

    # Step 2: Preprocessing
    yield "process", "Reading and preparing data...", 0, "..."
    if is_cancelled(): return
    import_data = processWSData(process_type)
    yield "process", "Done", 100, "✔️"

    # Step 3: Categorization
    yield "categorize", "Running categorization...", 0, "..."
    if is_cancelled(): return
    processed_data = llmRead(import_data, field, target_object)
    yield "categorize", "Done", 100, "✔️"

    # Step 4: Scoring
    yield "score", "Calculating novelty scores...", 0, "..."
    if is_cancelled(): return
    scored_data = processLLMData(processed_data)
    yield "score", "Done", 100, "✔️"

    # Step 5: Plotting
    yield "plot", "Generating visualization...", 0, "..."
    if is_cancelled(): return
    fig = plotData(scored_data)
    yield "plot", "Done", 100, "✔️"

    # Final result
    yield "done", "Pipeline complete", 100, "✔️", scored_data, fig
