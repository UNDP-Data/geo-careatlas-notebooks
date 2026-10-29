import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    """
    This notebook provides users with in depth know how on cilmate modeling.
    """
    overview_text = mo.md(
    """
    # 🌍 Understanding the climate modeling approach

    <hr style="height: 3px; background-color: red; border: none; opacity: 0.5; margin-top: 25px;">



    When working with climate change, one is almost always interested in **climate variables** (precipitation, temperature, etc) in **future** (forecasts). This is because the forecasts encompass variations in the spatio-temporal distribution of the climate variables an dthese are directly responsible for affecting the climate, or the climate chnage impact upon our world.  

    When we want to understand how climate change will impact a specific local area (like crop yields in a specific region), we cannot just rely on broad global predictions. We need to translate massive global datasets into highly accurate, localized forecasts. 

    Here is a simple breakdown of how we achieve this, including the assumptions we make and the limitations of the data.

    ## The 3-Step Approach

    Think of this process like calibrating a slightly inaccurate thermometer. If you know your thermometer always reads 2 degrees too hot compared to a perfectly accurate lab thermometer, you can confidently subtract 2 degrees from all its future readings to get the real temperature. We do the exact same thing with climate models.

    **1. Establishing the Ground-Truth (The Baseline)**
    First, we need to know exactly what happened in the past. We gather high-quality, local historical weather data (like daily rainfall and temperature) over several decades. This is our absolute "ground-truth."

    **2. Pulling Global Climate Data**
    Next, we look at massive Global Climate Models (GCMs). We ask these models for two things for our specific geographic box:
    *   **Hindcasts (Past Predictions):** What the model *predicted* the weather was going to be during our historical baseline period.
    *   **Forecasts (Future Predictions):** What the model predicts the weather will be in the coming decades.

    **3. Calibration (Statistical Bias Correction)**
    Global models are incredible, but they often have local "blind spots" (e.g., a global model might consistently underestimate rainfall in a specific mountain valley). We mathematically compare the model's past predictions (Hindcasts) against what actually happened (our Baseline). This reveals the model's exact bias. We then mathematically apply this correction to the future Forecasts. The result is a calibrated, highly accurate local prediction.

    ---

    ## Key Assumptions

    For this methodology to work, we rely on a few core assumptions:
    *   **Consistent Biases (Stationarity):** We assume that the specific errors a global model made in the past (e.g., always running 1 degree too cold in a certain region) will remain the same in the future. We assume we can safely apply historical error corrections to future predictions.
    *   **Reliable Baselines:** We assume our historical ground-truth observations are highly accurate, geographically precise, and free of major sensor or measurement errors. 
    *   **Accurate Broad Trends:** We assume that while global climate models might get local daily specifics wrong, they are correctly capturing the massive, overarching physics of global climate change (like overall atmospheric warming trends).

    ## Limitations of the Model

    It is important to understand the boundaries of what this data can tell us:
    *   **The "Unprecedented" Factor:** Because we calibrate our future models based on historical patterns, completely unprecedented extreme weather events—things that have literally never happened in recorded history—are incredibly difficult to predict with pinpoint statistical accuracy.
    *   **Data Deserts (Garbage In, Garbage Out):** If a specific region lacks good historical weather sensors, our baseline is inherently weaker. A poor historical baseline means our future calibrated forecasts will also carry that uncertainty.
    *   **Compounding Uncertainty:** The further out into the future we look (e.g., predicting the year 2080 vs. 2026), the more uncertain the foundational global climate models become. This global uncertainty naturally trickles down into our local predictions.

    ---
    *Note: Because this data engineering requires massive computational power, we execute this pipeline directly within **InsightsHub**. The platform spins up isolated cloud resources on-demand, allowing us to process decades of daily climate grids without crashing our local machines.*
    """
    )

    raw_data_text = mo.md(
    f"""
    #1. {mo.icon('arcticons:weather-forecast')} Climate data

    ---

    When it comes to 


    """)












    tabs = mo.ui.tabs(
        {
            f"{mo.icon('pajamas:overview')} Overview": overview_text,
            "Data": raw_data_text
        }
    )
    tabs
    return


if __name__ == "__main__":
    app.run()
