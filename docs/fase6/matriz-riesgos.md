# Matriz de Riesgos Consolidada
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 6.3 - Consolidación de Riesgos
**Fecha**: 2025-11-01
**Responsables**: @todos-los-agentes

---

## 1. Introducción

Esta matriz de riesgos consolida los principales riesgos técnicos, financieros y operacionales identificados a lo largo de las fases de diseño del proyecto. Cada riesgo ha sido evaluado en términos de probabilidad e impacto, y se ha asignado un plan de mitigación y un agente responsable de su seguimiento.

**Leyenda**:
-   **Probabilidad**: Baja, Media, Alta
-   **Impacto**: Bajo, Medio, Alto, Crítico

---

## 2. Matriz de Riesgos del Proyecto

| ID | Descripción del Riesgo | Probabilidad | Impacto | Plan de Mitigación | Owner (Agente) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **R-01** | **[Técnico]** La latencia de la red OT local excede los <10ms requeridos por los SCADA antiguos, incluso con GDC Edge. | Baja | Crítico | **Mitigación**: Realizar pruebas de certificación de latencia en el hardware GDC Edge antes de la migración de sistemas críticos. Asegurar que la red local de la planta esté optimizada. | @admin-legados |
| **R-02** | **[Técnico]** La replicación inter-regional de Cluster Linking (RPO de segundos) no es suficiente para un escenario de desastre mayor. | Baja | Alto | **Mitigación**: Aceptar este RPO para la recuperación ante desastres a nivel de negocio. El RPO=0 se garantiza para la operación local, que es el requisito primario. | @arquitecto-plataforma |
| **R-03** | **[Técnico]** Algunos ejecutables `.exe` llamados por Stored Procedures son "in-containerizables" debido a dependencias complejas (ej. hardware, UI). | Media | Medio | **Mitigación**: Para estos casos, mantener una pequeña granja de VMs con Windows Server on-premise como último recurso y exponer su funcionalidad a través de una API. | @admin-legados |
| **R-04** | **[Organizacional]** La brecha de habilidades (skills gap) en el equipo para manejar tecnologías como GCP, Anthos y Kafka retrasa la adopción. | Alta | Alto | **Mitigación**: Iniciar un plan de capacitación y certificación desde el Mes 1. Contratar 1-2 expertos externos para acompañar al equipo durante la Onda 1. | @devsecops |
| **R-05** | **[Técnico]** Picos de tráfico de replicación saturan el Dual Interconnect de 2Gbps, causando lag y afectando el RPO. | Media | Alto | **Mitigación**: Implementar QoS a nivel de red para priorizar tópicos críticos. Aplicar throttling en los conectores y productores de Kafka para datos de baja prioridad (logs, métricas). | @experto-redes |
| **R-06** | **[Financiero]** Se compran CUDs/RIs de 3 años de forma agresiva y luego el right-sizing reduce la necesidad, generando desperdicio. | Media | Medio | **Mitigación**: Adoptar un enfoque de compra de CUDs por fases. Iniciar con una cobertura del 30% y aumentarla gradualmente a medida que las cargas de trabajo se estabilizan. | @finanzas |
| **R-07** | **[Financiero]** El modelo de forecast de costos, al ser lineal, no es preciso y genera variaciones >5% contra el presupuesto. | Alta | Bajo | **Mitigación**: Evolucionar el modelo de IA para que incluya las ondas de migración como una variable (regresión por pasos). Re-entrenar el modelo mensualmente. | @data-scientist |
| **R-08** | **[Técnico]** Los pipelines de Spark en la nube no pueden procesar el volumen de datos de la capa BRONZE en tiempo real, generando lag. | Media | Medio | **Mitigación**: Implementar auto-escalado en los clusters de Dataproc/GKE. Monitorear el "consumer lag" de Kafka como un KPI crítico y configurar alertas. | @data-engineer |
| **R-09** | **[Técnico]** La configuración de Anthos Service Mesh resulta ser demasiado compleja y causa problemas de red difíciles de depurar. | Media | Alto | **Mitigación**: Iniciar con una configuración de ASM mínima (solo mTLS). Introducir políticas de tráfico avanzadas de forma gradual. Realizar talleres prácticos con el equipo de redes. | @experto-redes |
| **R-10** | **[Financiero]** El costo real de Confluent Cloud o GDC Edge excede significativamente los supuestos del modelo TCO. | Media | Alto | **Mitigación**: Obtener cotizaciones formales de Google y Confluent lo antes posible (primeros 30 días). Marcar estos supuestos como de alto riesgo en el caso de negocio. | @finanzas |
| **R-11** | **[Operacional]** Una prueba de Chaos Engineering mal planificada causa una interrupción real en un servicio de producción. | Baja | Alto | **Mitigación**: Realizar todas las pruebas de caos primero en el entorno de Staging. En producción, ejecutarlas solo durante las ventanas de mantenimiento planificadas. | @devsecops |
| **R-12** | **[Técnico]** La calidad de los datos en la capa GOLD es inferior al 98% requerido, debido a errores no detectados en las capas anteriores. | Media | Alto | **Mitigación**: Implementar un framework de Data Quality como `Great Expectations` dentro de los pipelines de Spark, con reglas que validen los datos antes de escribirlos en la capa SILVER y GOLD. | @arquitecto-datos |
| **R-13** | **[Proyecto]** El tiempo de entrega e instalación del hardware de GDC Edge retrasa el inicio de la Onda 1 en más de 3 meses. | Media | Alto | **Mitigación**: Contactar al equipo de cuentas de Google de forma inmediata para obtener un cronograma estimado. Iniciar el proceso de compra tan pronto como se apruebe el presupuesto. | @admin-legados |
