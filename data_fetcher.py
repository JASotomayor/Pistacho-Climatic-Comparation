# data_fetcher.py

import requests
import time


def fetch_hourly_era5(lat, lon, start_date, end_date, variables=None, retries=3):
    """Descarga datos horarios de ERA5 vía Open-Meteo."""
    if variables is None:
        variables = [
            "temperature_2m", "relativehumidity_2m",
            "windspeed_10m", "shortwave_radiation", "precipitation",
        ]

    var_str = ",".join(variables)
    url = (
        "https://archive-api.open-meteo.com/v1/era5?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        f"&hourly={var_str}"
        "&timezone=UTC"
    )

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("hourly", {})
            else:
                print(f"[{attempt}] ❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            print(f"[{attempt}] ⚠️ Error de conexión: {e}")

        time.sleep(2 ** attempt)  # Espera exponencial entre reintentos

    raise RuntimeError(
        f"❌ Fallo al descargar datos tras {retries} intentos para {lat}, {lon}"
    )
