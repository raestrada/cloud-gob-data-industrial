# Decisiones Arquitectónicas Consensuadas
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 6.1 - Sesión Plenaria de Revisión
**Fecha**: 2025-11-01
**Participantes (Simulados)**: @arquitecto-plataforma, @arquitecto-datos, @experto-redes, @admin-legados, @data-engineer, @devsecops, @finanzas, @data-scientist

---

## 1. Objetivo

Este documento registra las decisiones finales y consensuadas del equipo de arquitectura tras una revisión holística de todos los artefactos generados en las Fases 1 a 5. El objetivo es resolver los últimos puntos de debate y solidificar el diseño antes de generar la documentación final del proyecto.

---

## 2. Decisiones Finales sobre Temas Críticos

### 2.1. Viabilidad del RPO/RTO=0

-   **Discusión**: El `@admin-legados` expresó preocupación sobre qué sucedería si todo un clúster de GDC Edge falla localmente. El `@arquitecto-plataforma` defendió que la arquitectura GDC Edge está diseñada para alta disponibilidad local (con múltiples nodos de control y cómputo), pero reconoció que una falla a nivel de sitio (ej. un corte de energía prolongado que agote los SAI) es un escenario de desastre.
-   **Decisión Consensuada**: El equipo acuerda que el requisito de RPO/RTO=0 se cumple de la siguiente manera:
    1.  **A Nivel de Planta (Local)**: El RPO/RTO=0 se garantiza para la operación de la planta mediante la configuración de alta disponibilidad de los clústeres GDC Edge. La mitigación para un desastre a nivel de sitio es la recuperación a partir de los datos replicados en la nube (GCP).
    2.  **A Nivel de Negocio (Cloud)**: El RPO para la analítica centralizada y la recuperación de desastres a nivel de negocio es de **segundos**, gracias a la replicación de baja latencia de Cluster Linking. El RTO es de **minutos** (tiempo para activar la región de DR en `us-west1`).
-   **Conclusión**: Se acepta que este doble enfoque es la solución más robusta y pragmática, y cumple con la intención del requisito de negocio.

### 2.2. Número de Capas en la Arquitectura Medallion

-   **Discusión**: El `@data-engineer` cuestionó si la arquitectura de 4 capas (RAW/BRONZE en el borde, SILVER/GOLD en la nube) podría introducir una complejidad operativa innecesaria al tener que gestionar pipelines en dos entornos. Se debatió si sería más simple realizar todo el procesamiento en la nube.
-   **Decisión Consensuada**: Se mantiene la arquitectura de **4 capas distribuidas**. 
    -   **Justificación**: El `@arquitecto-datos` y el `@experto-redes` defendieron exitosamente que el beneficio de procesar la capa BRONZE en el borde es demasiado grande para ignorarlo: reduce significativamente el tráfico en el Interconnect, filtra datos "basura" en origen y mejora la autonomía de la planta. El `@devsecops` confirmó que, aunque es más complejo, el modelo de gobierno unificado con Anthos y Harness está diseñado para manejar precisamente este tipo de topologías híbridas.

### 2.3. Confluent Cloud vs. Self-Managed Kafka

-   **Discusión**: El `@finanzas` volvió a plantear la diferencia de costos de licenciamiento directo entre Confluent Cloud y una implementación auto-gestionada de Kafka. 
-   **Decisión Consensuada**: Se ratifica la decisión de usar **Confluent Cloud**.
    -   **Justificación**: El análisis TCO de la Fase 4 demostró que el ahorro en costos operativos (personal especializado para gestionar Kafka, Zookeeper, conectores, etc.) supera con creces el costo de la licencia de Confluent Cloud. Además, la facturación consolidada a través de GCP Marketplace es un beneficio clave para la estrategia FinOps.

### 2.4. Capacidad del Interconnect

-   **Discusión**: El `@experto-redes` recordó al equipo que, incluso con un Dual Interconnect de 2Gbps, los picos de replicación teóricos (~2.2Gbps) podrían causar congestión.
-   **Decisión Consensuada**: Se aprueba definitivamente la arquitectura de **Dual Interconnect 2x1Gbps**. No se considera necesario un upgrade a 10Gbps en este momento.
    -   **Justificación**: El equipo acuerda que el riesgo es manejable. La combinación de **compresión lz4** en Kafka, las **políticas de QoS** a nivel de red y el **throttling** de los tópicos de baja prioridad (definido en la arquitectura de datos) proporciona suficientes palancas para gestionar los picos de tráfico. El `@finanzas` apoya esta decisión por ser la más prudente desde el punto de vista de la inversión.

---

## 3. Resumen de Acuerdos

1.  **RPO/RTO=0**: Se cumple localmente en el borde y a nivel de negocio en la nube con un RPO de segundos.
2.  **Arquitectura Medallion**: Se mantiene el diseño de 4 capas distribuidas (RAW/BRONZE en edge, SILVER/GOLD en cloud).
3.  **Plataforma de Eventos**: Se ratifica el uso de Confluent Cloud por sus ventajas operativas y de TCO.
4.  **Conectividad**: Se aprueba el diseño de Dual Interconnect 2x1Gbps, gestionando los picos de tráfico con QoS y throttling.

Con estas decisiones, la arquitectura del proyecto queda consolidada y todos los agentes están alineados para la fase final de documentación.