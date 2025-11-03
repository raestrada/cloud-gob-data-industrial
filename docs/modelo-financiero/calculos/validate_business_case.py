import json
import math

def validate_business_case():
    """Carga los datos del modelo financiero y calcula todas las métricas clave del caso de negocio."""

    # --- 1. Cargar Archivos de Datos Validados ---
    try:
        with open('docs/modelo-financiero/calculos/datos_reales.json', 'r') as f:
            real_data = json.load(f)
        with open('docs/modelo-financiero/calculos/costos_cloud_proyectados.json', 'r') as f:
            cloud_costs_data = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: No se encontró un archivo de datos esencial. {e}")
        return

    # --- 2. Definir Supuestos Clave ---
    assumptions = {
        "gdc_edge_hardware_capex_total": 450000,
        "migration_ramp_up": {
            "y1_pct": 0.5,  # Año 1 opera a un promedio del 50% del run rate
            "y2_pct": 1.0,  # Año 2 opera al 100%
            "y3_pct": 1.0,  # Año 3 opera al 100%
        }
    }

    # --- 3. Cálculos ---

    # 3.1. Costos On-Premise
    tco_on_prem_3_anios = real_data['tco_on_prem_3_anios']
    opex_on_prem_anual = real_data['opex_on_prem_anual']['total']

    # 3.2. Costos Cloud
    opex_cloud_run_rate_anual = sum(item['valor'] for item in cloud_costs_data['costos_anuales'])
    costos_one_time_migracion = real_data['costos_one_time']['servicios_proyecto_capacitacion_datos']
    capex_gdc_edge = assumptions['gdc_edge_hardware_capex_total']
    
    inversion_total_cloud = costos_one_time_migracion + capex_gdc_edge

    costo_op_cloud_3_anios = (
        opex_cloud_run_rate_anual * assumptions["migration_ramp_up"]["y1_pct"] +
        opex_cloud_run_rate_anual * assumptions["migration_ramp_up"]["y2_pct"] +
        opex_cloud_run_rate_anual * assumptions["migration_ramp_up"]["y3_pct"]
    )
    
    tco_cloud_3_anios = costo_op_cloud_3_anios + inversion_total_cloud

    # 3.3. Métricas Financieras Principales
    ahorro_total_3_anios = tco_on_prem_3_anios - tco_cloud_3_anios
    roi_3_anios = (ahorro_total_3_anios / tco_cloud_3_anios) * 100

    # 3.4. Cálculo del Período de Recuperación (Payback)
    ahorro_opex_mensual_run_rate = (opex_on_prem_anual - opex_cloud_run_rate_anual) / 12
    meses_payback = 0
    inversion_restante = inversion_total_cloud
    
    # Modelo simplificado: asume ahorro lineal una vez alcanzado el run rate.
    # Un modelo más preciso requeriría un flujo de caja mensual detallado.
    if ahorro_opex_mensual_run_rate > 0:
        meses_payback = inversion_total_cloud / ahorro_opex_mensual_run_rate

    # 3.5. Cálculo de Costo por Unidad
    produccion_anual = real_data['capacidades']['produccion_anual_unidades']
    costo_por_unidad_on_prem = opex_on_prem_anual / produccion_anual
    costo_por_unidad_cloud = opex_cloud_run_rate_anual / produccion_anual

    # 3.6. Cálculo de Payback Realista (Modelo de 2 Fases)
    def calculate_realistic_payback(inversion_total, ahorro_mensual_neto):
        """
        Calcula el payback usando un modelo de 2 fases para mayor realismo.
        Fase 1: Período de inversión inicial (6 meses).
        Fase 2: Período de recuperación del déficit.
        """
        # Supuesto 1: La fase de inversión dura 6 meses.
        investment_phase_months = 6
        
        # Supuesto 2: Se incurre en un déficit acumulado durante la Fase 1.
        # Este déficit se compone del 50% del CAPEX y un sobrecosto de OPEX solapado.
        capex_en_fase_1 = inversion_total * 0.5 
        opex_solapado_fase_1 = 175000  # Supuesto justificado en PAYBACK_MODEL.md
        déficit_maximo_acumulado = capex_en_fase_1 + opex_solapado_fase_1

        # Supuesto 3: La recuperación en Fase 2 ocurre a la tasa de ahorro mensual total.
        if ahorro_mensual_neto <= 0:
            return float('inf') # No hay payback si no hay ahorros

        meses_recuperacion = déficit_maximo_acumulado / ahorro_mensual_neto
        
        payback_total_modelado = investment_phase_months + meses_recuperacion
        return payback_total_modelado

    payback_modelado_meses = calculate_realistic_payback(inversion_total_cloud, ahorro_opex_mensual_run_rate)


    # --- 4. Imprimir Resultados ---
    print("--- VALIDACIÓN DEL MODELO FINANCIERO DEL CASO DE NEGOCIO ---")
    print("\n**1. TCO y Ahorro (3 Años)**")
    print(f"  - TCO On-Premise: ${tco_on_prem_3_anios:,.2f} USD")
    print(f"  - TCO Cloud:      ${tco_cloud_3_anios:,.2f} USD")
    print(f"  - Ahorro Total:   ${ahorro_total_3_anios:,.2f} USD")

    print("\n**2. Métricas de Inversión**")
    print(f"  - Inversión Total (CAPEX + One-Time): ${inversion_total_cloud:,.2f} USD")
    print(f"  - ROI (Retorno de la Inversión) a 3 Años: {roi_3_anios:.2f}%")
    print(f"  - Período de Recuperación (Payback Simple): {meses_payback:.2f} meses (ignora la rampa de migración)")
    print(f"  - Período de Recuperación (Payback Modelado): {payback_modelado_meses:.2f} meses (ver PAYBACK_MODEL.md)")


    print("\n**3. Métricas de Negocio**")
    print(f"  - Costo por Unidad (On-Premise): ${costo_por_unidad_on_prem:.2f} USD")
    print(f"  - Costo por Unidad (Cloud):     ${costo_por_unidad_cloud:.2f} USD")
    print(f"  - Reducción del Costo por Unidad: {((costo_por_unidad_on_prem - costo_por_unidad_cloud) / costo_por_unidad_on_prem) * 100:.2f}%")

    print("\n--- FIN DE LA VALIDACIÓN ---")

if __name__ == '__main__':
    validate_business_case()
