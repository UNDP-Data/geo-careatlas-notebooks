import marimo

__generated_with = "0.25.1"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # 🚀 This notebook is a test
    """)
    return


if __name__ == "__main__":
    app.run()
