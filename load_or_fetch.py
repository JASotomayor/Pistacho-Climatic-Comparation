# load_or_fetch.py

import os
import pandas as pd

import config
import locations
import data_fetcher
import processor


def clean_unused_data():
    """Remove data files for locations not selected."""
    selected_prefixes = [site.replace(" ", "_") for site in locations.SELECTED_SITES]
    os.makedirs("data", exist_ok=True)
    for file in os.listdir("data"):
        if not any(file.startswith(prefix) for prefix in selected_prefixes):
            os.remove(os.path.join("data", file))
            print(f"🗑️ Archivo eliminado: {file}")


def load_or_fetch(location_name, force_download=False):
    """Load processed climate data for a location or fetch and process it."""
    filename = f"data/{location_name.replace(' ', '_')}.pkl"

    if os.path.exists(filename) and not force_download:
        print(f"📂 Cargando datos locales: {filename}")
        return pd.read_pickle(filename)

    print(f"🌐 Descargando datos para: {location_name}")
    info = locations.LOCATIONS[location_name]
    lat, lon = info["lat"], info["lon"]

    hourly = data_fetcher.fetch_hourly_era5(
        lat, lon, f"{config.START_YEAR}-01-01", f"{config.END_YEAR}-12-31"
    )
    df_hourly = processor.build_hourly_dataframe(hourly)
    df_daily = processor.aggregate_daily_from_hourly(df_hourly)
    df_agro = processor.add_agronomic_indicators(df_daily, lat)
    df_agro["location"] = location_name

    os.makedirs("data", exist_ok=True)
    df_agro.to_csv(filename.replace(".pkl", ".csv"))
    df_agro.to_pickle(filename)
    print(f"💾 Datos actualizados y guardados para {location_name}")

    return df_agro
