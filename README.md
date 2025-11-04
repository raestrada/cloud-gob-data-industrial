# Desafío de Arquitectura Cloud & FinOps

Este repositorio contiene la solución al desafío de diseño de arquitectura cloud con gobierno FinOps e IA para un caso de negocio industrial. El objetivo es liderar la migración y operación de infraestructura crítica a Google Cloud Platform (GCP) en un plazo de 12-18 meses.

## Entregables

A continuación se presentan los entregables clave del proyecto, diseñados para abordar los requisitos del caso de negocio:

- **[Memo Ejecutivo](./entregables/Memo_Ejecutivo_LiderCloudFinOps_ESTRADA.md)**: Resume la decisión recomendada, las decisiones de alto nivel requeridas, el análisis de CAPEX/OPEX, las sensibilidades financieras y los principales riesgos y trade-offs.

- **[Caso de Negocio](./entregables/Caso_Negocio_LiderCloudFinOps_ESTRADA.md)**: Detalla los principios de arquitectura, el modelo financiero a 3 años, el modelo de gobierno FinOps, el modelo operativo (RACI) y la estrategia de gestión del cambio.

- **[MVP de IA para FinOps](./entregables/MVP_IA_FinOps_ESTRADA.md)**: Presenta un prototipo funcional para el pronóstico de costos, la detección de anomalías y el etiquetado de recursos mediante NLP, incluyendo el dataset utilizado.

- **[Plan Maestro (Gantt)](./entregables/Plan_Gantt_ESTRADA.md)**: Define las fases del proyecto, los hitos Go/No-Go, los procedimientos de rollback y las dependencias críticas, considerando las ventanas de mantenimiento y los periodos de congelación.

- **[Deck Ejecutivo](./entregables/presentacion_ejecutiva/index.html)**: Proporciona una presentación de alto nivel para la alta dirección (CIO/CTO/CFO/CEO) que resume la situación actual, la propuesta de valor, el roadmap, el análisis TCO/ROI, los riesgos y los próximos pasos.

## Presentaciones Adicionales

Además de los entregables principales, se han preparado dos presentaciones adicionales para proporcionar una visión más profunda de la solución:

- **[Presentación Técnica](./entregables/presentacion_tecnica/index.html)**: Ofrece una inmersión profunda en la arquitectura técnica, el flujo de datos, la topología de red, el workflow de GitOps y el modelo de gobierno FinOps.

- **[Presentación del MVP](./entregables/presentacion_mvp/index.html)**: Muestra el prototipo de IA para FinOps en acción, demostrando sus capacidades de pronóstico, detección de anomalías y etiquetado.

## Documentación Relevante

La siguiente documentación proporciona el contexto y los detalles de la arquitectura y la planificación del proyecto:

- **[Índice de Documentación](./docs/README.md)**: Índice principal de toda la documentación del proyecto.

- **[Caso de Negocio (PDF)](./docs/Caso%20de%20negocio%20-%20Lider%20de%20Arquitectura%20Cloud%20&%20Finops.pdf)**: El documento original del caso de negocio que describe los requisitos y restricciones del proyecto.

- **[Arquitectura](./docs/arquitectura/)**: Contiene los documentos que describen la arquitectura de la plataforma, los datos, la red y la revisión arquitectónica.

- **[Baseline del Inventario](./docs/baseline-inventario/)**: Proporciona información sobre el estado actual de la infraestructura, incluyendo el baseline financiero, la conectividad y el inventario de sistemas legados.

- **[Migración y DevOps](./docs/migracion-devops/)**: Describe el enfoque de DevSecOps, la estrategia de migración de sistemas legados y los pipelines de datos.

## Modelo Financiero y Validación

El corazón del caso de negocio reside en un modelo financiero robusto y auditable. Esta sección contiene el análisis TCO, el cálculo de ROI y un modelo de payback refinado que justifica la viabilidad del proyecto.

Todos los cálculos están automatizados en un script de Python para garantizar la transparencia y la consistencia.

- **[Explorar el Modelo Financiero](./docs/modelo-financiero/README.md)**
- **[Análisis Financiero Completo](./docs/modelo-financiero/ANALISIS_FINANCIERO_COMPLETO.md)**: Documento consolidado que extiende el modelo de payback con la explicación de todos los cálculos financieros y los valores obtenidos.

---

## MVP de IA para FinOps

Como parte de la Fase 5 del proyecto, se desarrolló un **MVP (Minimum Viable Product)** para demostrar la viabilidad y el valor de negocio de aplicar IA a los procesos de FinOps. El MVP se compone de tres casos de uso funcionales implementados en Jupyter Notebooks.

Los resultados y la documentación completa del MVP se encuentran en el [entregable correspondiente](entregables/MVP_IA_FinOps_ESTRADA.md).

### Notebooks del MVP

Puede explorar y ejecutar los notebooks directamente:

- **[00_data_generation.ipynb](MVP/notebooks/00_data_generation.ipynb)**: Script para generar el dataset sintético a partir del CSV histórico, validando la estrategia *Event-First*.
- **[01_forecast_costos.ipynb](MVP/notebooks/01_forecast_costos.ipynb)**: Implementa y compara tres modelos de Machine Learning para predecir los costos mensuales con un MAPE < 10%.
- **[02_deteccion_anomalias.ipynb](MVP/notebooks/02_deteccion_anomalias.ipynb)**: Utiliza Isolation Forest para detectar anomalías en los costos en tiempo real con un F1-Score > 85%.
- **[03_nlp_etiquetado.ipynb](MVP/notebooks/03_nlp_etiquetado.ipynb)**: Demuestra cómo usar NLP para inferir y asignar etiquetas faltantes a recursos "huérfanos", con el objetivo de alcanzar un 100% de compliance.

