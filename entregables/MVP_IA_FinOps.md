# MVP de IA para FinOps v1
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 5.1 - Diseño de MVP de IA para FinOps
**Fecha**: 2025-11-01
**Responsable**: @data-scientist
**Versión**: 1.0

---

## 1. Resumen Ejecutivo

Este documento presenta una Prueba de Concepto (MVP) que demuestra la viabilidad y el valor de aplicar técnicas de Inteligencia Artificial a la gestión FinOps del proyecto. Se han desarrollado tres modelos simples pero efectivos:

1.  **Forecast de Costos**: Un modelo de regresión lineal que proyecta el costo del mes siguiente, estimando **$345,861 USD** para el Mes 13.
2.  **Detección de Anomalías**: Un modelo estadístico que ha identificado correctamente los meses **M1 y M2** como anomalías, debido a sus costos significativamente más bajos que la media, lo que permite una investigación temprana de posibles desviaciones.
3.  **Etiquetado NLP**: Un sistema basado en reglas que infiere con éxito etiquetas de `owner`, `cost_center` y `criticality` a partir de los nombres de los recursos, sentando las bases para una gobernanza de costos automatizada.

El MVP confirma que incluso con modelos sencillos, podemos aportar inteligencia y automatización al proceso de FinOps. Se propone una arquitectura MLOps en Vertex AI para operacionalizar estos modelos.

---

## 2. Metodología

El MVP se desarrolló utilizando Python 3.12 y la librería `pandas` en un entorno virtual aislado para garantizar la reproducibilidad. Los cálculos se basan en el set de datos de costos históricos proporcionado en el caso de negocio. Tanto el código como los datos se incluyen en este documento para una total transparencia.

---

## 3. Modelo 1: Forecast de Costos

-   **Algoritmo**: Se utilizó una **Regresión Lineal simple** (`y = mx + c`), donde `x` es el número del mes y `y` es el costo total. Para un MVP, este modelo es ideal por su simplicidad, interpretabilidad y bajo costo computacional. Modela la tendencia general de crecimiento de los costos durante la migración.
-   **Resultados**: El modelo calculó una tendencia lineal de crecimiento de costos de aproximadamente **$8,421 USD por mes**.
    -   **Costo Proyectado para M13**: **$345,861.33 USD**

---

## 4. Modelo 2: Detección de Anomalías

-   **Algoritmo**: Se implementó un modelo estadístico basado en la **desviación estándar (σ)**. Se calcula la media y la desviación estándar de los 12 meses de datos. Cualquier mes cuyo costo total caiga fuera del umbral de **±1.5σ** desde la media es marcado como una anomalía.
-   **Resultados**:
    -   Media de Costos (12M): $291,121.58 USD
    -   Desviación Estándar (σ): $35,985.47 USD
    -   Límite Superior de Normalidad: $345,099.78 USD
    -   Límite Inferior de Normalidad: $237,143.38 USD
    -   **Anomalías Detectadas**: 
        -   **M1 ($218,300)**: Marcado como anomalía por estar por debajo del límite inferior.
        -   **M2 ($234,600)**: Marcado como anomalía por estar por debajo del límite inferior.
-   **Interpretación**: El modelo identifica correctamente que los primeros dos meses tuvieron costos inusualmente bajos en comparación con el resto del año, lo cual es esperado al inicio de un proyecto y valida la sensibilidad del modelo.

---

## 5. Modelo 3: Etiquetado NLP de Recursos

-   **Algoritmo**: Se utilizó un enfoque simple y robusto basado en **Reglas y Expresiones Regulares (RegEx)**. Se define una función que analiza el nombre de un recurso en busca de palabras clave (ej. `prod`, `billing`, `dev`) para inferir su criticidad, dueño y centro de costo.
-   **Resultados**: El modelo fue probado con una lista de nombres de recursos hipotéticos:

    | Recurso | Etiquetas Inferidas |
    | :--- | :--- |
    | `vm-prod-billing-api-01` | `{'owner': 'equipo-finanzas', 'cost_center': 'FIN-101', 'criticality': 'high'}` |
    | `gcs-bucket-analytics-landing-zone` | `{'owner': 'equipo-datos', 'cost_center': 'DATA-205', 'criticality': 'low'}` |
    | `gke-dev-test-cluster-temp` | `{'owner': 'unknown', 'cost_center': 'unknown', 'criticality': 'low'}` |
    | `vm-unassigned-temp-instance` | `{'owner': 'unknown', 'cost_center': 'unknown', 'criticality': 'low'}` |

-   **Interpretación**: El modelo asigna correctamente las etiquetas cuando la nomenclatura es consistente y asigna valores por defecto (`unknown`) cuando no encuentra pistas, permitiendo una posterior revisión manual.

---

## 6. Arquitectura MLOps en Vertex AI

Para operacionalizar y escalar estos modelos, se propone la siguiente arquitectura MLOps sobre Vertex AI, que permite el re-entrenamiento y la ejecución automática de los modelos de FinOps.

```mermaid
graph TD
    A[Cloud Scheduler<br/>(Ejecuta cada 24h)] --> B(Cloud Function)
    B -- Inicia Pipeline --> C[Vertex AI Pipelines]
    
    subgraph C
        C1[Carga de Datos<br/>(desde BigQuery)] --> C2[Validación de Datos]
        C2 --> C3[Entrenamiento de Modelos<br/>(Forecast, Anomaly)]
        C3 --> C4[Evaluación de Modelos]
        C4 -- Si el modelo es bueno --> C5[Registro en Model Registry]
    end

    C5 --> D{Despliegue}
    D --> D1[Batch Predictions<br/>(Genera Reporte Diario)]
    D --> D2[Online Endpoint<br/>(Para consultas en tiempo real)]
```

-   **Flujo**: Un `Cloud Scheduler` ejecuta una `Cloud Function` diariamente, la cual dispara un `Vertex AI Pipeline`. Este pipeline carga los últimos datos de costos desde BigQuery, entrena los modelos, los evalúa y, si superan un umbral de calidad, los registra y despliega para generar reportes diarios de anomalías y forecasts actualizados.

---

## 7. Código Fuente del MVP

A continuación se presenta el script completo `finops_mvp.py` utilizado para este análisis.

```python
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
    x = df['mes_num']
    y = df['total']
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
        if re.search(r'prod|critical|crit', resource_name, re.IGNORECASE):
            tags["criticality"] = "high"
        elif re.search(r'staging|uat', resource_name, re.IGNORECASE):
            tags["criticality"] = "medium"
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
```

---

## 8. Conclusión y Próximos Pasos

-   **Conclusión**: El MVP demuestra que es factible y de alto valor implementar modelos de IA para mejorar la gobernanza financiera. Los modelos, aunque simples, proporcionan información accionable para controlar costos, detectar problemas y automatizar el etiquetado.
-   **Próximos Pasos**:
    -   **Evolucionar Modelos**: Mejorar el modelo de forecast (ej. a ARIMA o Prophet) y el de NLP (ej. a un clasificador de texto simple) para mayor precisión.
    -   **Integración**: Integrar el etiquetado NLP como un webhook en el pipeline de CI/CD de Harness para validar las etiquetas antes del despliegue.
    -   **Operacionalización**: Implementar la arquitectura MLOps en Vertex AI para automatizar el re-entrenamiento y la ejecución de estos modelos.
