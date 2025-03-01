import plotly.express as px
import plotly.graph_objects as go
import webbrowser
import pandas as pd

def plotData(scored_data):
    fig = go.Figure(px.scatter(
        scored_data,
        x="pub_year",
        y="novelty score",
        color="object",
        hover_name="title",
        custom_data=["pub_id"]
    ))
    
    def on_point_click(trace, points, selector):
        if points.point_inds:
            idx = points.point_inds[0]
            pub_id = trace.customdata[idx][0]
            url = f"https://doi.org/{pub_id}"
            webbrowser.open(url)
    
    for trace in fig.data:
        trace.on_click(on_point_click)
    
    fig.update_layout(
        title="Novelty Score by Journal article ove Time",
        showlegend=True,
        legend=dict(
            title="Object",
            orientation="v",
            x=1.02,
            y=1
        )
    )
    fig.show()
