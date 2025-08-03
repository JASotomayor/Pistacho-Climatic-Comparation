"""Generate climate datasets for all selected locations."""

import time
import os

import locations
from load_or_fetch import load_or_fetch, clean_unused_data


def main(force_download: bool = True):
    clean_unused_data()
    for site_name in locations.SELECTED_SITES:
        print(f"📥 Procesando: {site_name}")
        df_agro = load_or_fetch(site_name, force_download=force_download)
        csv_path = f"data/{site_name.replace(' ', '_')}.csv"
        pkl_path = f"data/{site_name.replace(' ', '_')}.pkl"
        print(f"💾 Archivos guardados: {csv_path} / {pkl_path}")
        time.sleep(2)


if __name__ == "__main__":
    force = os.environ.get("FORCE_DOWNLOAD", "1") == "1"
    main(force_download=force)
