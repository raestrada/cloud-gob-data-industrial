import json
import pandas as pd
import numpy as np
import re

def run_finops_mvp():
    """
    Ejecuta una prueba de concepto de IA para FinOps, incluyendo:
    1. Forecast de costos simple.
    2. Detección de anomalías basada en desviación estándar.
    3. Etiquetado NLP basado en reglas.
    """

    # --- 1. Cargar Datos ---
    with open('docs/fase5/mvp_finops/costos_historicos.json', 'r') as f:
        data = json.load(f)
    
    df = pd.DataFrame(data['serie_historica_costos'])
    df['mes_num'] = df['mes'].str.replace('M', '').astype(int)

    print("--- MVP de IA para FinOps ---")
    print("\n**1. Forecast de Costos para el Mes 13**")

    # --- 2. Modelo de Forecast (Regresión Lineal Simple) ---
    # y = mx + c
    x = df['mes_num']
    y = df['total']
    
    # Usando numpy para calcular la regresión
    m, c = np.polyfit(x, y, 1)
    
    forecast_m13 = m * 13 + c

    print(f"  - Modelo: Regresión Lineal (y = {m:.2f}x + {c:.2f})")
    print(f"  - Costo Proyectado para M13: ${forecast_m13:,.2f} USD")

    print("\n**2. Detección de Anomalías**")

    # --- 3. Modelo de Detección de Anomalías (Desviación Estándar) ---
    mean_cost = df['total'].mean()
    std_cost = df['total'].std()
    anomaly_threshold_factor = 1.5
    
    upper_bound = mean_cost + (std_cost * anomaly_threshold_factor)
    lower_bound = mean_cost - (std_cost * anomaly_threshold_factor)

    df['anomalia'] = (df['total'] > upper_bound) | (df['total'] < lower_bound)
    anomalies = df[df['anomalia'] == True]

    print(f"  - Método: Costo se desvía > {anomaly_threshold_factor}σ de la media (${mean_cost:,.2f} USD)")
    print(f"  - Límite Superior: ${upper_bound:,.2f} USD")
    print(f"  - Límite Inferior: ${lower_bound:,.2f} USD")

    if not anomalies.empty:
        print("  - ¡Anomalías Detectadas!")
        for index, row in anomalies.iterrows():
            print(f"    - Mes: {row['mes']}, Costo: ${row['total']:,} USD (Anomalía)")
    else:
        print("  - No se detectaron anomalías con el umbral actual.")

    print("\n**3. Etiquetado NLP (Basado en Reglas)**")

    # --- 4. Modelo de Etiquetado NLP (RegEx) ---
    def infer_tags_from_name(resource_name):
        tags = {"owner": "unknown", "cost_center": "unknown", "criticality": "low"}
        
        # Inferir criticidad
        if re.search(r'prod|critical|crit', resource_name, re.IGNORECASE):
            tags["criticality"] = "high"
        elif re.search(r'staging|uat', resource_name, re.IGNORECASE):
            tags["criticality"] = "medium"
        elif re.search(r'dev|test', resource_name, re.IGNORECASE):
            tags["criticality"] = "low"

        # Inferir owner/equipo
        if re.search(r'billing|finanzas', resource_name, re.IGNORECASE):
            tags["owner"] = "equipo-finanzas"
            tags["cost_center"] = "FIN-101"
        elif re.search(r'datateam|analytics', resource_name, re.IGNORECASE):
            tags["owner"] = "equipo-datos"
            tags["cost_center"] = "DATA-205"
        elif re.search(r'scada|ot', resource_name, re.IGNORECASE):
            tags["owner"] = "equipo-ot"
            tags["cost_center"] = "OT-300"
            
        return tags

    test_resources = [
        "vm-prod-billing-api-01",
        "gcs-bucket-analytics-landing-zone",
        "gke-dev-test-cluster-temp",
        "vm-unassigned-temp-instance"
    ]

    print("  - Método: Extracción de etiquetas con RegEx a partir del nombre del recurso.")
    for resource in test_resources:
        inferred = infer_tags_from_name(resource)
        print(f"    - Recurso: '{resource}' -> Etiquetas Inferidas: {inferred}")

    print("\n--- FIN DEL MVP ---")

if __name__ == '__main__':
    run_finops_mvp()
