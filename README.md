# Pistacho-Climatic-Comparation

This project downloads hourly ERA5 reanalysis data from Open-Meteo for a set of pistachio growing locations and aggregates it into agronomic indicators.

## Usage

1. Install dependencies:
   ```bash
   pip install pandas numpy requests
   ```

2. Generate datasets for all configured locations:
   ```bash
   python generate_data.py
   ```
   Set `FORCE_DOWNLOAD=0` to reuse existing cached datasets.

Processed files are saved under the `data/` directory in both CSV and pickle formats.
