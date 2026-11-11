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
    ---


    ## 1. Background


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
    download_dir = '/data/'
    df = None
    with mo.status.spinner(title="Downloading admin data ...") as _spinner:
        df = fetch_admin_boundaries(admin_level=2, iso3_country_code=myanmar_iso3_country_code, download_dir=download_dir )
        _spinner.update(f'Downlaoded {len(df)} districts')
        _spinner.update("Done")


    m = leafmap.Map()
    m.add_gdf(df, layer_name='admin')
    m
    return download_dir, myanmar_bbox, os


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - Nighttime lights

    Nighttime lights (NTL) data measures how bright the Earth is in the dark using satellite sensors, Suomi NPP (SNPP), NOAA-20, and NOAA-21 a trio of weather and environmental satellites flying in the same polar orbit, spaced out like buses on a route so they scan every spot on Earth at roughly 1:30 AM and 1:30 PM local time. A polar orbit is a satellite path that loops vertically from the North Pole to the South Pole while the Earth spins sideways underneath it, allowing a single satellite to scan the entire planet like peeling an orange in vertical strips. As the satellites enter the range of Ground Satellite Processing Stations located close to poles the images are downlaoded and forwarded as well as processed further into products at the vendors data centeres. For the purpose of this study we will use monthly aggregates directky from NASA Eartaccess platform. This data is processed and disseminated in Hierchical Data Format (.h5) files representiong 10x10 degrees tiles on the ground.
    """)
    return


@app.cell
def _(myanmar_bbox, os):
    import earthaccess
    import xarray as xr
    import dask
    import h5netcdf
    import h5py
    import pandas as pd
    import rioxarray as rxr
    from dask.diagnostics import ProgressBar
    from urllib.parse import urlparse
    import rasterio

    def search_monthly_ntl(bbox: tuple, start_date: str, end_date: str) -> list:
        """
        Searches NASA's STAC/CMR API for VNP46A3 (Monthly Nighttime Lights) granules.

        Parameters:
        -----------
        bbox : tuple
            (min_longitude, min_latitude, max_longitude, max_latitude)
        start_date : str
            Start of the study period (e.g., "2023-01-01")
        end_date : str
            End of the study period (e.g., "2023-12-31")

        Returns:
        --------
        list
            A list of earthaccess granule objects representing the remote files.
        """
    
        # 2. Query the STAC/CMR endpoint
        granules = earthaccess.search_data(
            short_name="VNP46A3",
            bounding_box=bbox,
            temporal=(start_date, end_date)
        )

        print(f"Found {len(granules)} monthly NTL granules for the specified parameters.")

        return granules

    def download_and_assemble_ntl(
        granules: list, 
        download_dir: str, 
        # CHANGED: The correct variable name for VNP46A3 (Monthly)
        subdataset: str = "NearNadir_Composite_Snow_Free"
    ) -> xr.Dataset:
        """
        Downloads STAC granules concurrently
        """
        os.makedirs(download_dir, exist_ok=True)

        granules_to_download = list()
        downloaded_files = list()
        for g in granules:
            link = g.data_links()[0]
            plink = urlparse(link)
            *_, file_name = str(plink.path).split('/')
            local_file = os.path.join(download_dir, file_name)
            if os.path.exists(local_file):
                with rasterio.open(local_file) as _:
                    downloaded_files.append(local_file)
                    continue
            granules_to_download.append(g)
    
        if granules_to_download:
            print(f"Downloading {len(granules_to_download)} granules to {download_dir}...")
            # 1. Authenticate with NASA Earthdata
            # 'netrc' strategy automatically looks for credentials in your system's ~/.netrc file.
            # If it fails, you can fall back to earthaccess.login(strategy="interactive")
            # try:
            #     earthaccess.login(strategy="netrc")
            # except Exception:
            #     earthaccess.login(strategy="interactive")

            local_paths = earthaccess.download(granules, local_path=download_dir, show_progress=True)
            valid_paths = [p for p in local_paths if p is not None and os.path.exists(p)]
            valid_paths+=downloaded_files
        else:
            valid_paths = downloaded_files
        print(f"Successfully secured {len(valid_paths)} local files.")
        return valid_paths


    # ==========================================
    # Example Usage:
    # ==========================================

    ntl_granules = search_monthly_ntl(
        bbox=myanmar_bbox, 
        start_date="2023-01-01", 
        end_date="2024-01-01"
    )

    ntl_dataset = download_and_assemble_ntl(ntl_granules, download_dir='/data/ntl')
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    - UNDP project sites
    """)
    return


@app.cell
def _(download_dir, os, pd):
    import requests
    import time
    from datetime import datetime
    from typing import Union

    # ─── API Configuration ───
    SUMMARY_API = "https://api.open.undp.org/api/project_summary_{year}.json"
    PROJECT_DETAIL_API = "https://api.open.undp.org/api/projects/{project_id}.json"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    API_DELAY = 0.2  # Slightly increased to avoid rate limits

    def scrape_undp_api_test(operating_unit, years, download_dir:str=None, verbose=True)-> Union[pd.DataFrame, None]:
        """
        Adjusted standalone scraper to test UNDP API extraction.
        """
        os.makedirs(download_dir, exist_ok=True)

        file_name = f'UNDP_projects_{operating_unit}.csv'

        file_path = os.path.join(download_dir, file_name)
        # if os.path.exists(file_path):
        #     print(f'Reading already downloaded local file {file_path}')
        #     return pd.read_csv(file_path)


        all_projects = {}

        if verbose:
            print(f"Scraping UNDP API for unit: {operating_unit}")
            print(f"Years: {years}\n" + "-"*40)

        for year in years:
            if verbose:
                print(f"→ Scanning {year}...", end=" ", flush=True)
    
            try:
                resp = requests.get(SUMMARY_API.format(year=year), headers=HEADERS, timeout=30)
                if resp.status_code != 200:
                    if verbose: print(f"HTTP {resp.status_code}")
                    continue
        
                # Protection against HTML error pages masquerading as 200 OK
                try:
                    data = resp.json()
                except ValueError:
                    if verbose: print("Invalid JSON response")
                    continue
            
                # Handle both list and dict structures just in case the API changes
                if isinstance(data, dict):
                    data = data.get('data', [])
            
                target = [p for p in data if p.get('operating_unit') == operating_unit]
        
                if verbose:
                    print(f"found {len(target)} projects.", end=" ", flush=True)
        
                new_count = 0
                for proj in target:
                    p_id = proj.get('project_id') or proj.get('id')
                    if not p_id or p_id in all_projects:
                        continue
            
                    time.sleep(API_DELAY)
                    try:
                        d_resp = requests.get(
                            PROJECT_DETAIL_API.format(project_id=p_id),
                            headers=HEADERS, timeout=15
                        )
                        if d_resp.status_code != 200: continue
                
                        details = d_resp.json()
                
                        title = details.get('title') or details.get('project_title') or "No Title"
                        subnational = details.get('subnational', [])
                        lats, lons = [], []
                        for sout in subnational:
                            if 'lat' in sout and 'lon' in sout:
                                lons.append(sout['lon'])
                                lats.append(sout['lat'])
                        lat = set(lats)
                        lon = set(lons)
                        print(p_id, lon, lat)
                        #continue
                    
                
                        # Robust description extraction
                        desc_parts = [details.get('description', '') or details.get('project_descr', '')]
                        for out in details.get('outputs', []):
                            t, d = out.get('title', ''), out.get('descr', '')
                            if t or d:
                                desc_parts.append(f"[Output: {t} - {d}]")
                        
                        full_text = " || ".join([str(d) for d in desc_parts if d]).strip()
                
                        start, end = details.get('start', ''), details.get('end', '')
                
                        # Umbrella check
                        is_umbrella = False
                        if start:
                            try:
                                days = (datetime.now() - datetime.strptime(start, '%Y-%m-%d')).days
                                if days > 1825:  # > 5 years
                                    is_umbrella = True
                            except (ValueError, TypeError):
                                pass
                
                        all_projects[p_id] = {
                            'project_id': p_id,
                            'title': title,
                            'start_date': start,
                            'end_date': end,
                            'total_budget': details.get('budget', 0),
                            'is_likely_umbrella': is_umbrella,
                            'url': f"https://open.undp.org/projects/{p_id}",
                            'description': full_text,
                        }
                        new_count += 1
                
                    except Exception as e:
                        if verbose: print(f"\n    Error fetching {p_id}: {e}")
        
                if verbose:
                    print(f"({new_count} newly added)")
    
            except requests.exceptions.Timeout:
                if verbose: print("TIMEOUT")
            except Exception as e:
                if verbose: print(f"ERROR: {e}")

        if all_projects:
            df = pd.DataFrame(list(all_projects.values()))
            df['start_date'] = pd.to_datetime(df['start_date'], errors='coerce')
            df['total_budget'] = pd.to_numeric(df['total_budget'], errors='coerce')
            df.to_csv(file_path)
            return df



    # ==========================================
    # TEST EXECUTION FOR MYANMAR (MMR)
    # ==========================================
    # We use recent years to keep the test fast
    test_years = [2024, 2025, 2026]
    mmr_projects_df = scrape_undp_api_test(operating_unit="MMR", years=test_years, download_dir=download_dir)

    # Display the results in Marimo
    mmr_projects_df.head()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Geospatial Analysis
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Economic Analysis
    """)
    return


if __name__ == "__main__":
    app.run()
