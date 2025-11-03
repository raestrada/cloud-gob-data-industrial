# Metodología de Cálculo del Período de Recuperación (Payback)

**Versión:** 1.0
**Fecha:** 2025-11-01
**Autor:** Líder de Arquitectura Cloud & FinOps

## 1. Resumen Ejecutivo

El cálculo del período de recuperación de la inversión (Payback) para este proyecto se ha refinado para reflejar con mayor precisión la realidad de una migración tecnológica de 18 meses. Un cálculo simple (Inversión Total / Ahorro Anual) es inadecuado porque asume que los ahorros se materializan instantáneamente.

Nuestro modelo avanzado, basado en el flujo de caja proyectado, establece un **período de payback de 11 meses**. Este modelo es más conservador y realista, proporcionando una base sólida para la toma de decisiones.

## 2. Deficiencia del Cálculo Simple

Un cálculo simple arrojaría un payback de ~8.8 meses. Este resultado es excesivamente optimista y engañoso por la siguiente razón:

- **Ignora la Curva J de Inversión:** No considera que durante los meses iniciales del proyecto, los flujos de caja son negativos debido a la inversión en hardware/software (CAPEX) y al solapamiento de costos operativos (pago de infraestructura on-premise y cloud simultáneamente).

## 3. Modelo de Payback en Dos Fases

Para corregir esto, hemos implementado un modelo que divide el proyecto en dos fases financieras distintas:

#### Fase 1: Inversión y Rampa (Meses 1-6)

Corresponde al primer semestre del proyecto, donde se realizan las inversiones más fuertes y los ahorros aún no son significativos.

- **Actividades:** Compra de hardware GDC Edge, licencias de software, configuración de la conectividad, ejecución del piloto y arranque de la Onda 1.
- **Flujo de Caja:** Fuertemente negativo.
- **Objetivo del Cálculo:** Determinar el **déficit máximo acumulado** al final de esta fase.

#### Fase 2: Recoupment (Recuperación) (A partir del Mes 7)

A partir del segundo semestre, la migración se acelera, el decomisionamiento de la infraestructura antigua genera ahorros recurrentes que superan los costos, y el flujo de caja mensual se vuelve positivo.

- **Actividades:** Migración de las Ondas 2 y 3, optimización de recursos en la nube.
- **Flujo de Caja:** Positivo y creciente.
- **Objetivo del Cálculo:** Determinar cuánto tiempo se necesita para que el flujo de caja positivo compense el déficit generado en la Fase 1.

## 4. Cálculo Matemático Detallado

| Paso | Descripción | Cálculo | Resultado |
| :--- | :--- | :--- | :--- |
| **1** | **Calcular Déficit en Fase 1 (Mes 6)** | | |
| | 50% del CAPEX Total (`$2.15M`) | `$2,150,000 * 0.5` | `$1,075,000` |
| | (+) Costo de OPEX solapado (estimado) | `Supuesto` | `$175,000` |
| | **Déficit Máximo Acumulado** | `$1,075,000 + $175,000` | **`$1,250,000`** |
| **2** | **Calcular Tasa de Ahorro Mensual** | | |
| | OPEX Mensual On-Prem | `$5,245,000 / 12` | `$437,083` |
| | (-) OPEX Mensual Cloud (Final) | `$2,302,180 / 12` | `$191,848` |
| | **Ahorro Mensual Neto** | `$437,083 - $191,848` | **`$245,235`** |
| **3** | **Calcular Tiempo de Recuperación** | | |
| | Meses para recuperar el déficit | `Déficit / Ahorro Mensual` | |
| | | `$1,250,000 / $245,235` | **`5.1 meses`** |
| **4** | **Calcular Payback Total** | | |
| | Período de Inversión (Fase 1) | `6 meses` | |
| | (+) Tiempo de Recuperación (Fase 2) | `5.1 meses` | |
| | **Período de Payback Final** | `6 + 5.1 meses` | **`11.1 meses`** |

## 5. Conclusión

El período de recuperación de la inversión, modelado de forma realista, es de **11 meses**. Este valor considera el tiempo necesario para realizar las inversiones iniciales y la rampa de generación de ahorros, ofreciendo una expectativa mucho más precisa para los stakeholders.

## 6. Implementación en Código

Para garantizar la consistencia y auditabilidad, este modelo matemático ha sido implementado en el script de validación del caso de negocio. La función `calculate_realistic_payback` dentro del siguiente archivo ejecuta este cálculo automáticamente:

- **Script:** `validate_business_case.py`
