import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md("""
    # 🚀 New Notebook
    Start building your insights here.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The mode does compute the effct of d....
    """)
    return


if __name__ == "__main__":
    app.run()
