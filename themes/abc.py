import marimo

__generated_with = "0.9.0"
app = marimo.App(width="medium")

@app.cell
import marimo as mo
return (mo,)

@app.cell
def _(mo):
    mo.md("# 🚀 New Notebook\nStart building your insights here.")
    return

if __name__ == "__main__":
    app.run()
