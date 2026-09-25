'Overview notebook of test.'

import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # Overview
    """)
    return


@app.function
def load_data():
    print("Create data")


@app.cell
def _():
    load_data()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
