'Feature Tour notebook of Asia Pacific.'

import marimo

__generated_with = "0.20.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.md('# Feature Tour')
    return


if __name__ == "__main__":
    app.run()
