import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
import pandas as pd
import plotly.io as pio
pio.templates.default = "plotly"  # or "plotly_dark", "ggplot2", etc.

def plotData(scored_data):
    pio.templates.default = "plotly"  # <== Add this line
    fig = px.scatter(
        scored_data,
        x="pub_year",
        y="novelty score",
        color="object",
        hover_name="title",
        custom_data=["pub_id"],
        title="Novelty Score by Journal Article Over Time"
    )

    fig.update_layout(
        legend=dict(
            title="Object",
            orientation="v",
            x=1.02,
            y=1
        )
    )

    return fig