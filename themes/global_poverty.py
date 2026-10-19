"""
 This notebok allows exploring global poverty patterns at various spatial scales
"""

import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium", auto_download=["html"])


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    So far not much is done here
    """)
    return


@app.cell
def menu():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    from vega_datasets import data
    import altair as alt
    import pandas as pd

    return alt, data


@app.cell
def _(alt, data):
    def create_heatmap():

        # Load and prepare data
        source = data.seattle_weather()
        # Create heatmap
        chart = alt.Chart(source).mark_rect().encode(
            x=alt.X('date:O', timeUnit='month', title='Month'),
            y=alt.Y('date:O', timeUnit='day', title='Day'),
            color=alt.Color('temp_max:Q', title='Maximum Temperature (°C)'),
            tooltip=[
                alt.Tooltip('monthdate(date):T', title='Date'),
                alt.Tooltip('temp_max:Q', title='Max Temperature')
            ]
        ).properties(
            width=300,
            height=200,
            title='Seattle Weather Heat Map'
        ).interactive()

        return chart

    create_heatmap()
    return


@app.cell
def _(mo):
    metric = mo.ui.dropdown(
        options=["Population", "Facilities", "Coverage"],
        value="Population",
        label="Metric",
    )
    threshold = mo.ui.slider(start=0, stop=100, value=30, label="Threshold")
    mo.vstack([metric, threshold])
    return


@app.cell
def _():
    import os
    for k, v in os.environ.items():
        print(f'{k}={v}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a demo cell to demononstrate Marimo MD
    ##. A subtittle

    # Title


    ### Underlined subtitle
    ----
    """)
    return


if __name__ == "__main__":
    app.run()
