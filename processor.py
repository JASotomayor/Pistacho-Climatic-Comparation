# processor.py

import pandas as pd
import numpy as np
import config


def build_hourly_dataframe(hourly_data):
    df = pd.DataFrame({
        "datetime": pd.to_datetime(hourly_data.get("time", [])),
        "T": hourly_data.get("temperature_2m"),
        "RH": hourly_data.get("relativehumidity_2m"),
        "u10": hourly_data.get("windspeed_10m"),
        "Rs_W_m2": hourly_data.get("shortwave_radiation"),
        "precip_mm": hourly_data.get("precipitation"),
    })
    df = df.set_index("datetime").sort_index()
    return df


def aggregate_daily_from_hourly(df_hourly):
    df = df_hourly.copy()
    df["doy"] = df.index.dayofyear
    df["T_mean"] = df["T"]
    df["T_max"] = df["T"]
    df["T_min"] = df["T"]
    df["RH_mean"] = df["RH"]
    df["u2"] = df["u10"] * 0.748  # Corrección por altura (10m -> 2m)
    df["Rs"] = df["Rs_W_m2"] * 0.0864  # W/m² -> MJ/m²/día

    df_daily = df.resample("D").agg({
        "T_mean": "mean",
        "T_max": "max",
        "T_min": "min",
        "RH_mean": "mean",
        "u2": "mean",
        "Rs": "mean",
        "precip_mm": "sum",
        "doy": "first",
    })

    return df_daily


# Curva fenológica para pistacho

def kc_pistachio(doy):
    if doy <= 30:
        return 0.4
    elif doy <= 120:
        return 0.4 + (0.9 - 0.4) * (doy - 30) / 90
    elif doy <= 250:
        return 0.9
    elif doy <= 300:
        return 0.9 - (0.9 - 0.7) * (doy - 250) / 50
    elif doy <= 330:
        return 0.7
    else:
        return 0.4


# Fórmula FAO-56 para ETo diario

def eto_fao56(row, lat):
    from math import radians, sin, cos, tan, acos, exp, sqrt, pi

    T = row["T_mean"]
    RH = row["RH_mean"]
    u2 = row["u2"]
    Rs = row["Rs"]
    doy = row["doy"]

    delta = 0.409 * sin(2 * pi * doy / 365 - 1.39)
    phi = radians(lat)
    dr = 1 + 0.033 * cos(2 * pi * doy / 365)
    omega = acos(-tan(phi) * tan(delta))
    Ra = (24 * 60 / pi) * config.GSC * dr * (
        omega * sin(phi) * sin(delta) + cos(phi) * cos(delta) * sin(omega)
    )
    Rso = (0.75 + 2e-5 * 0) * Ra
    es = 0.6108 * exp((17.27 * T) / (T + 237.3))
    ea = es * (RH / 100)
    Rns = (1 - config.ALBEDO) * Rs
    Tk = T + 273.16
    fcd = 1.35 * min(1, Rs / Rso) - 0.35
    Rnl = config.SIGMA * (Tk ** 4) * (0.34 - 0.14 * sqrt(ea)) * fcd
    Rn = Rns - Rnl
    delta_svp = (4098 * es) / ((T + 237.3) ** 2)
    gamma = 0.665e-3 * 101.3
    eto = (
        0.408 * delta_svp * Rn + gamma * (900 / (T + 273)) * u2 * (es - ea)
    ) / (delta_svp + gamma * (1 + 0.34 * u2))
    return max(0, eto)


def add_agronomic_indicators(df_daily, lat):
    df = df_daily.copy()
    df["ETo"] = df.apply(lambda r: eto_fao56(r, lat), axis=1)
    df["Kc"] = df["doy"].apply(kc_pistachio)
    df["ETc"] = df["ETo"] * df["Kc"]
    df["GDD"] = np.maximum(df["T_mean"] - config.GDD_BASE, 0)
    df["heat_stress"] = (df["T_max"] >= config.HEAT_STRESS_THRESHOLD).astype(int)
    df["frost_event"] = (df["T_min"] <= config.FROST_THRESHOLD).astype(int)
    df["irrigation_need_mm"] = df["ETc"] - df["precip_mm"]
    return df
