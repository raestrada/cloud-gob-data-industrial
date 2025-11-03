import json

def calculate_tco():
    # --- 1. Cargar Archivos de Datos ---
    with open('docs/modelo-financiero/calculos/datos_reales.json', 'r') as f:
        real_data = json.load(f)
    with open('docs/modelo-financiero/calculos/costos_cloud_proyectados.json', 'r') as f:
        cloud_costs_data = json.load(f)

    # --- 2. Definir Supuestos (solo para la rampa de migración) ---
    assumptions = {
        "gdc_edge_hardware_capex_total": 450000, # CAPEX inicial para GDC Edge en 3 plantas ($150k por planta).
        "migration_ramp_up": {
            "months_0_6": {"cloud_resources_pct": 0.30, "on_prem_staff_pct": 0.90},
            "months_7_12": {"cloud_resources_pct": 0.70, "on_prem_staff_pct": 0.60},
            "months_13_18": {"cloud_resources_pct": 1.00, "on_prem_staff_pct": 0.30},
            "months_19_36": {"cloud_resources_pct": 1.00, "on_prem_staff_pct": 0.10}
        }
    }

    # --- 3. Cálculos ---

    # 3.1. Sumar Costos Cloud Anuales desde el archivo JSON
    total_run_rate_cloud_anual = sum(item['valor'] for item in cloud_costs_data['costos_anuales'])

    # 3.2. Cálculo del TCO a 3 años
    # TCO Cloud
    costo_cloud_anio_1 = (total_run_rate_cloud_anual * (assumptions['migration_ramp_up']['months_0_6']['cloud_resources_pct'] * 0.5 + 
                                                     assumptions['migration_ramp_up']['months_7_12']['cloud_resources_pct'] * 0.5))
    costo_cloud_anio_2 = (total_run_rate_cloud_anual * (assumptions['migration_ramp_up']['months_13_18']['cloud_resources_pct'] * 0.5 + 
                                                     assumptions['migration_ramp_up']['months_19_36']['cloud_resources_pct'] * 0.5))
    costo_cloud_anio_3 = total_run_rate_cloud_anual * assumptions['migration_ramp_up']['months_19_36']['cloud_resources_pct']
    
    costo_operativo_cloud_3_anios = costo_cloud_anio_1 + costo_cloud_anio_2 + costo_cloud_anio_3
    
    tco_cloud_3_anios = (
        costo_operativo_cloud_3_anios + 
        real_data['costos_one_time']['servicios_proyecto_capacitacion_datos'] + 
        assumptions['gdc_edge_hardware_capex_total']
    )

    # 3.3. Resultados Financieros
    tco_on_prem_original = real_data['tco_on_prem_3_anios']
    ahorro_total_3_anios = tco_on_prem_original - tco_cloud_3_anios
    roi_3_anios = (ahorro_total_3_anios / tco_cloud_3_anios) * 100

    # --- 4. Imprimir Resultados ---
    print("--- ANÁLISIS FINANCIERO PRELIMINAR (TCO a 3 Años) ---")
    print("\n")
    print("**A. TCO On-Premise (Línea Base)**")
    print(f"  - TCO a 3 Años (Caso de Negocio): ${tco_on_prem_original:,} USD")
    print("\n")
    print("**B. TCO Proyectado en GCP (con GDC Edge)**")
    print(f"  - Costo Operativo Cloud (3 años): ${costo_operativo_cloud_3_anios:,.2f} USD")
    print(f"  - Costos de Migración (One-Time): ${real_data['costos_one_time']['servicios_proyecto_capacitacion_datos']:,} USD")
    print(f"  - CAPEX en GDC Edge Hardware: ${assumptions['gdc_edge_hardware_capex_total']:,} USD")
    print("  --------------------------------------------------")
    print(f"  - **TCO Cloud Total a 3 Años:** ${tco_cloud_3_anios:,.2f} USD")
    print("\n")
    print("**C. Resultados y Ahorro**")
    print(f"  - Ahorro Total Proyectado (3 años): ${ahorro_total_3_anios:,.2f} USD")
    print(f"  - **ROI a 3 Años:** {roi_3_anios:.2f}%")
    print("\n")
    print("--- FIN DEL ANÁLISIS ---")
    print("\nNOTA: Este es un cálculo preliminar basado en los datos y supuestos definidos.")

if __name__ == '__main__':
    calculate_tco()
