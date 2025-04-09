
import streamlit as st
from orchestrator import run_pipeline_with_progress
from visualizer import plotData
import pandas as pd
import io
from datetime import datetime
import time
from streamlit import rerun

st.title("Novel Research Analysis Tool")

# Inputs
query = st.text_input("Enter your query")
max_results = st.number_input("Number of articles", min_value=10, max_value=1000, value=100)
process_type = st.radio("Choose processing type", options=["LLM", "NLP"])
field = st.text_input("Research field")
target_object = st.text_input("Group by")

# Initialize session state
if "step_generator" not in st.session_state:
    st.session_state.step_generator = None
if "step_data" not in st.session_state:
    st.session_state.step_data = {}
if "running" not in st.session_state:
    st.session_state.running = False
if "cancel" not in st.session_state:
    st.session_state.cancel = False
if "last_step" not in st.session_state:
    st.session_state.last_step = None

def is_cancelled():
    return st.session_state.cancel

# Start analysis
if not st.session_state.running:
    if st.button("Run Analysis"):
        st.session_state.running = True
        st.session_state.cancel = False
        st.session_state.step_generator = run_pipeline_with_progress(
            query, max_results, process_type, field, target_object, is_cancelled
        )

# Cancel button
if st.session_state.running:
    st.button("❌ Cancel", on_click=lambda: st.session_state.update({"cancel": True, "running": False}))

# Stage containers
steps = {
    "fetch": st.expander("📥 Fetching articles", expanded=True),
    "process": st.expander("🧹 Processing data", expanded=False),
    "categorize": st.expander("🧠 Categorizing abstracts", expanded=False),
    "score": st.expander("📊 Calculating scores", expanded=False),
    "plot": st.expander("📈 Creating visualization", expanded=False),
}
status = {k: steps[k].empty() for k in steps}
bars = {k: steps[k].progress(0) for k in steps}
eta_label = {k: steps[k].empty() for k in steps}

# Step advancement
def advance_pipeline():
    try:
        update = next(st.session_state.step_generator)
        st.session_state.last_step = update
    except StopIteration:
        st.session_state.running = False
        st.session_state.step_generator = None
        st.session_state.last_step = None

# Auto-advance on rerun
if st.session_state.running and st.session_state.step_generator:
    advance_pipeline()
    time.sleep(0.3)  # slight delay to simulate pipeline pacing
    st.rerun()

# Render UI from last step
if st.session_state.last_step:
    step = st.session_state.last_step[0]
    msg = st.session_state.last_step[1]
    pct = st.session_state.last_step[2]
    eta = st.session_state.last_step[3]
    bars[step].progress(pct)
    status[step].write(msg)
    eta_label[step].markdown(f"🕒 {eta}")
    if len(st.session_state.last_step) == 5:
        scored_data = st.session_state.last_step[4]
        fig = st.session_state.last_step[5]

        st.session_state.scored_data = scored_data
        st.session_state.fig = fig
        st.session_state.running = False

        safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '_', '-')).replace(" ", "_")[:50]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        st.session_state.csv_filename = f"{safe_query}_{timestamp}.csv"
        st.session_state.xlsx_filename = f"{safe_query}_{timestamp}.xlsx"
        st.session_state.plot_filename = f"{safe_query}_{timestamp}_plot.html"

        html_buffer = io.StringIO()
        fig.write_html(html_buffer, include_plotlyjs="cdn")
        st.session_state.html_data = html_buffer.getvalue().encode("utf-8")

# Results
if st.session_state.get("scored_data") is not None:
    st.markdown("### 📊 Datatable Preview")
    st.dataframe(st.session_state.scored_data.head())
    st.plotly_chart(st.session_state.fig, use_container_width=True)

    csv_data = st.session_state.scored_data.to_csv(index=False).encode("utf-8")
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        st.session_state.scored_data.to_excel(writer, index=False, sheet_name="Results")

    st.markdown("### 📥 Download Results")
    st.download_button("Download CSV", csv_data, st.session_state.csv_filename, mime="text/csv")
    st.download_button("Download Excel", excel_buffer.getvalue(), st.session_state.xlsx_filename,
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.download_button("Download Plot (HTML)", st.session_state.html_data, st.session_state.plot_filename,
                       mime="text/html")

# Show fetch count if stored
if st.session_state.get("fetched_data") is not None:
    st.caption(f"Fetched {len(st.session_state.fetched_data)} raw articles.")
