import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📈 Early Economic Impact Recovery

    ## Background
    ---

    ### 1. Context
    Every year, billions of dollars are spent on humanitarian assistance and early recovery following natural disasters and conflicts. Yet, because crises often destroy local statistical systems and make on-the-ground surveys dangerous or impossible, rigorous evidence on what these programs actually achieve remains incredibly sparse. Humanitarian actors, governments, and private investors need to know: <span style="padding:0px; background-color:#f0f0f0; color:red">*Did this intervention actually accelerate recovery? And what was the economic value of bringing that recovery forward?*</span>. <p>To bridge this evidence gap, we can look to space. Satellite Earth observation—specifically nighttime luminosity (nightlights) and radar backscatter—allows us to track human activity and physical reconstruction independently, safely, and consistently every single month. By combining satellite data with the exact GPS locations of recovery projects, we can estimate how quickly local economies bounce back.</p>

    ### 2. The Approach

    ### 3. Core Assumptions

    ### 4. Weaknesses and Limitations
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


if __name__ == "__main__":
    app.run()
