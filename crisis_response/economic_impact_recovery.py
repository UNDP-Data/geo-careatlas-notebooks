import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    "This notebook addresses the problem of post crisis economic impact recovery"
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 📈 Early Economic Impact Recovery

    ## 1. Background
    ---

    ### 1.1 Context
    Every year, billions of dollars are spent on humanitarian assistance and early recovery following natural disasters and conflicts. Yet, because crises often destroy local statistical systems and make on-the-ground surveys dangerous or impossible, rigorous evidence on what these programs actually achieve remains incredibly sparse. Humanitarian actors, governments, and private investors need to know: <span style="padding:0px; background-color:#f0f0f0; color:red">*Did this intervention actually accelerate recovery? And what was the economic value of bringing that recovery forward?*</span>. <p>To bridge this evidence gap, we can look to space. Satellite Earth observation—specifically nighttime luminosity (nightlights) as well as surface reflections recorded under all weather conditions—allows us to track human activity and physical reconstruction independently, safely, and consistently every single month. By combining satellite data with the exact GPS locations of recovery projects, it is possible to estimate how quickly local economies bounce back.</p>

    ### 1.2 The Approach

    This notebook provides a generic, scalable pipeline to evaluate the impact of early recovery programs. It operates in three distinct stages:
    1.2.1 **Data Fetch & Preparation (The I/O Layer):** We ingest cloud-optimized administrative boundaries, project coordinates, and monthly satellite observations (like NASA's VIIRS nighttime lights).

    1.2.2 **Geospatial Analysis (The Transformation Layer):** We create spatial "donut" buffers around the project sites. For example, we might define areas within 3 km of a project as "Treated" (they received help) and areas 3 to 8 km away as "Control" (they did not, but share similar local geography).

    1.2.3 **Economic Analysis (The Modeling Layer):** We use a statistical method called Difference-in-Differences (DiD) to compare the recovery speeds of the Treated and Control areas over time. Because satellite radiance data often contains near-zero values in crisis zones, we use a robust statistical model (Poisson Pseudo-Maximum-Likelihood, or PPML) to accurately measure the percentage change in recovery. Finally, we convert this percentage into an estimated dollar value using established economic formulas mapping nightlights to GDP.

    ### 1.3 Core Assumptions
    To interpret the results correctly, we rely on a few critical assumptions:
    - **Parallel Trends:** We assume that, in the absence of the recovery project, the Treated and Control areas would have recovered at the same rate. We verify this by testing their trajectories before the intervention began.
    - **Constant Elasticity:** To convert light into money, we assume a standard global elasticity rate (typically 0.3) where a 10% increase in nightlights roughly translates to a 3% increase in GDP. This is an indicative scenario, not a perfectly calibrated local financial return.
    - **Baseline Accuracy:** We assume that historical, pre-shock data for population and GDP accurately represent the scale of the local economy, though crises often trigger significant displacement.

    ### 1.4 Weaknesses and Limitations

    - **Correlation vs. Causation:** In crisis environments, many agencies operate simultaneously. While spatial buffering isolates local effects, it is difficult to prove that a recovery spike was caused solely by one specific organization's project.
    - **Spillover Effects:** Humanitarian aid delivered to a "Treated" zone might economically benefit the nearby "Control" zone through shared markets, which can dilute the measured difference between the two.
    - **Sensor Limitations:** Nighttime lights are an excellent proxy for economic activity, but they can be distorted by seasonal factors (like snow or harvest cycles), cloud cover, or heavily damaged electrical grids. Physical reconstruction (like clearing debris) can sometimes happen months before the electricity comes back on.
    """)
    return


if __name__ == "__main__":
    app.run()
