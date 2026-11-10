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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Data
    ---

    - Administrative boundaries

    Define our fundamental unit of analysis. Satellite pixels (like nightlights or radar) are aggregated within these shapes to calculate local economic averages. Furthermore, we use the geographic centroid of these polygons to measure the distance to UNDP intervention sites, which dictates whether an area is flagged as "Treated" or "Control.". While there are many public sources of administrative boundaries that one could use for this purpose, we choose the Comprehensive Global Administrative Zones (CGAZ) by geoBoundaries, a standardized dataset of political and dministrative boundaries. This dataset offers two major advantages:  polygon edges are simplified to reduce file sizes, and disputed territories are unified using standard definitions (U.S. Department of State) to prevent overlapping or missing data artifacts. This makes the dataset analysis ready.
    """)
    return


@app.cell
def _(mo):
    import os
    import geopandas as gpd
    from pyogrio import read_dataframe, write_dataframe
    import h3.api.basic_int as h3
    import leafmap

    def fetch_admin_boundaries(bbox: tuple = None, admin_level: int = 0, iso3_country_code:str = None, download_dir:str=None, h3id_precision: int = 7) -> gpd.GeoDataFrame:
        """
        Fetches administrative boundaries via VSI using FlatGeobuf spatial indexing.
        Filters invalid ISO codes, calculates centroids, and maps H3 indices.
        """

        os.makedirs(download_dir, exist_ok=True)
        dest_path = os.path.join(download_dir, f'admin{admin_level}.fgb')

        if os.path.exists(dest_path):
            print(f'Reading already downloaded local file {dest_path}')
            return read_dataframe(dest_path)


        # 1. Fetch via VSI utilizing the FlatGeobuf spatial index
        url = f"/vsicurl/https://undpngddlsgeohubdev01.blob.core.windows.net/admin/cgaz/geoBoundariesCGAZ_ADM{admin_level}.fgb"

        where_clause = f"iso3 = '{iso3_country_code}'" if iso3_country_code else None


        gdf = read_dataframe(url, bbox=bbox, where=where_clause)
        print(gdf.columns.tolist())

        if gdf.empty:
            raise ValueError(f"No features found in BBOX: {bbox}")

   
        # 3. Calculate H3 IDs 
        # GeoPandas handles centroids natively
        centroids = gdf.to_crs('EPSG:8857').geometry.centroid

        # Map H3 IDs using the centroid coordinates
        gdf["h3id"] = centroids.apply(
            lambda pt: h3.latlng_to_cell(lat=pt.y, lng=pt.x, res=h3id_precision) if not pt.is_empty else None
        )

        # 4. Standardize Name Column
        source_name_field = f"admin{admin_level}_name"
        if source_name_field in gdf.columns:
            gdf["name"] = gdf[source_name_field].fillna("")
        if dest_path is not None:
            write_dataframe(gdf,dest_path,promote_to_multi=True,)

        return gdf

    # we define Myanmar's boun ding box in geographic coordinates
    myanmar_bbox = west, south, east, north = 92.17, 9.53, 101.18, 28.55
    myanmar_iso3_country_code='MMR'
    download_dir = '/tmp/data'
    df = None
    with mo.status.spinner(title="Downloading admin data ...") as _spinner:
        df = fetch_admin_boundaries(admin_level=2, iso3_country_code=myanmar_iso3_country_code, download_dir=download_dir )
        _spinner.update(f'Downlaoded {len(df)} districts')
        _spinner.update("Done")


    m = leafmap.Map()
    m.add_gdf(df, layer_name='admin')
    m
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Nighttime lights

    Night time lights data
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Geospatial Analysis
    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Economic Analysis
    ---
    """)
    return


if __name__ == "__main__":
    app.run()
