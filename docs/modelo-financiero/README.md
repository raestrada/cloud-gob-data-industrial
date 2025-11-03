# Modelo Financiero y Validación

Esta sección contiene todos los artefactos utilizados para construir y validar el caso de negocio financiero del proyecto.

### Documentos Principales

- **[Estructura de Costos Cloud](./estructura-costos-cloud.md):** Detalla los componentes de costo proyectados en la plataforma GCP.
- **[Modelo Financiero](./modelo-financiero.md):** Contiene la hoja de cálculo principal y el análisis TCO.

---

### Validación y Automatización de Cálculos

Para garantizar la precisión y la auditabilidad, todos los cálculos clave del caso de negocio (TCO, ROI, Ahorro, Costo/Unidad) están automatizados en un script de Python. Este script es la **fuente única de verdad** para todas las métricas financieras.

- **Script de Validación:** [calculos/validate_business_case.py](./calculos/validate_business_case.py)
- **Datos de Entrada:** [calculos/datos_reales.json](./calculos/datos_reales.json), [calculos/costos_cloud_proyectados.json](./calculos/costos_cloud_proyectados.json)

### Metodología del Período de Recuperación (Payback)

El cálculo del Período de Recuperación de la Inversión (Payback) utiliza un modelo matemático en dos fases que es más realista que un cálculo simple. Este enfoque considera la rampa de inversión y la materialización progresiva de los ahorros, resultando en un payback de **11 meses**.

La justificación completa y el desglose del cálculo se encuentran en el siguiente documento:

- **Documento de Metodología:** [calculos/PAYBACK_MODEL.md](./calculos/PAYBACK_MODEL.md)
