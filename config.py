# config.py

# Período de análisis
START_YEAR = 2000
END_YEAR = 2024

# Umbrales climáticos
CHILL_THRESHOLD = 7.0           # Horas frío < 7°C
HEAT_STRESS_THRESHOLD = 35.0    # Estrés térmico ≥ 35°C
FROST_THRESHOLD = 0.0           # Evento de helada ≤ 0°C
GDD_BASE = 7.0                  # Temperatura base para GDD (Growing Degree Days)

# Constantes FAO-56 para ETo
ALBEDO = 0.23                   # Reflectancia del suelo
SIGMA = 4.903e-9                # Constante de Stefan-Boltzmann (MJ·K⁻⁴·m⁻²·día⁻¹)
GSC = 0.0820                    # Constante solar (MJ·m⁻²·min⁻¹)
Z = 10                          # Altura del viento (m)

# Tabla de Weinberger para frío estimado
WEIM_T = [13.2, 12.3, 11.4, 10.6, 9.8, 8.3, 7.6, 6.9, 6.3]
WEIM_HF = [450, 550, 650, 750, 850, 950, 1050, 1150, 1350]
