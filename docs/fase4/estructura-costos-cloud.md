# Estructura de Costos Proyectada (Cloud)
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 4.1 - Análisis Financiero
**Fecha**: 2025-11-01
**Responsable**: @finanzas
**Versión**: 1.0

---

## 1. Resumen Ejecutivo

Este documento proporciona un desglose detallado de la estructura de costos proyectada para la nueva arquitectura basada en Google Cloud Platform y GDC Edge. Su objetivo es ofrecer una visión clara de las nuevas categorías de gasto en un modelo de nube, separando los costos de inversión (CAPEX) de los costos operativos (OPEX).

-   **CAPEX Total Proyectado**: **$2,150,000**
-   **OPEX Anual Proyectado (Run Rate)**: **$2,214,872**

Esta estructura de costos servirá como base para el análisis de TCO y para la discusión sobre el alineamiento con el presupuesto del proyecto.

---

## 2. Desglose de CAPEX (Costos de Inversión)

El CAPEX representa los gastos iniciales y únicos necesarios para poner en marcha el proyecto.

| Componente | Monto (USD) | Fuente / Supuesto |
| :--- | :--- | :--- |
| Servicios de Migración y Capacitación | $1,700,000 | **[DATO VALIDADO]** Caso de Negocio, pág. 4 |
| Hardware para GDC Edge (3 plantas) | $450,000 | **[SUPUESTO]** Estimación de $150k por planta para el hardware base. |
| **TOTAL CAPEX** | **$2,150,000** | |

---

## 3. Desglose de OPEX Anual (Costos Operativos)

El OPEX representa los costos recurrentes anuales una vez que la plataforma esté operando en su estado final (steady state).

| Categoría | Costo Anual (USD) | Justificación y Cálculo |
| :--- | :--- | :--- |
| **Cómputo (GKE + GDC Edge)** | $489,148 | Basado en 1900 vCPU y 12.8TB RAM, con 20% de right-sizing y 40% de descuento CUD a 3 años. |
| **Almacenamiento** | $436,224 | Basado en 200TB de Block Storage y 500TB de Object Storage en GCP. |
| **Red (Interconnect)** | $72,000 | **[SUPUESTO]** Costo de Dual Interconnect 2x1Gbps ($6,000/mes). |
| **Servicios Gestionados** | | |
| - Confluent Platform | $200,000 | **[SUPUESTO]** Licenciamiento anual para 5 clústeres (2 Cloud, 3 Edge). |
| - Licenciamiento GDC Edge | $67,500 | **[SUPUESTO]** 15% del CAPEX del hardware como costo anual de licencia/soporte. |
| **Soporte y Personal** | | |
| - Soporte GCP Enterprise | $150,000 | **[DATO VALIDADO]** $12,500/mes. |
| - Equipo de Operaciones Cloud | $800,000 | **[SUPUESTO]** Reducción del equipo de 12 a 8 FTEs ($100k/FTE promedio). |
| **TOTAL OPEX ANUAL** | **$2,214,872** | |

---

## 4. Comparativa de Estructura OPEX (Anual)

| Categoría | On-Premise (Actual) | Cloud (Proyectado) | Cambio |
| :--- | :--- | :--- | :--- |
| Hardware, Energía y Mantenimiento | $1,980,000 | $0 | ▼ Elimina |
| Cómputo y Almacenamiento | (Incluido arriba) | $925,372 | ▲ Nueva Categoría |
| Licenciamiento (Software) | $1,515,000 | $267,500 | ▼ Reduce |
| Personal de Operaciones | $1,200,000 | $800,000 | ▼ Reduce |
| Red y Conectividad | $300,000 | $72,000 | ▼ Reduce |
| Soporte y Otros Servicios | $250,000 | $150,000 | ▼ Reduce |
| **TOTAL** | **$5,245,000** | **$2,214,872** | **-57.8%** |

Este desglose muestra un cambio fundamental del gasto, pasando de un modelo intensivo en CAPEX de hardware y licenciamiento perpetuo a un modelo basado en el consumo de servicios gestionados y una operación más ágil.
