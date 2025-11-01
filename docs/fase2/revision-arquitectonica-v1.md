# Sesión de Revisión Arquitectónica v1
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 2.4 - Revisión Cruzada de Arquitectura
**Fecha**: 2025-11-01
**Participantes**: @arquitecto-plataforma, @arquitecto-datos, @experto-redes, @admin-legados

---

## 1. Objetivo de la Sesión

Validar de forma cruzada los diseños de alto nivel para la plataforma, datos y red. El objetivo es identificar inconsistencias, riesgos y puntos de mejora antes de proceder al diseño detallado en la Fase 3. Se han revisado los siguientes documentos:
- `arquitectura-plataforma.md`
- `arquitectura-datos.md`
- `arquitectura-redes.md`

---

## 2. Puntos de Discusión y Cuestionamientos

### 2.1. Feedback de @arquitecto-datos

-   **Punto Fuerte**: La arquitectura de plataforma con GDC Edge y clústeres Kafka locales se alinea perfectamente con la necesidad de procesar las capas RAW y BRONZE en el borde. Permite la autonomía y optimiza el ancho de banda.
-   **Cuestionamiento a @arquitecto-plataforma**: La topología de 5 clústeres Kafka (3 en el borde, 2 en la nube) es potente pero parece costosa y compleja de gestionar. **¿Se ha evaluado un modelo intermedio?** Por ejemplo, empezar con un único clúster edge en Monterrey y que las otras dos plantas apunten a él a través de la WAN, antes de desplegar GDC Edge en las 3 plantas. Esto podría reducir el CAPEX inicial.

### 2.2. Feedback de @experto-redes

-   **Punto Fuerte**: El modelo de conectividad 100% privado con PSC y Anthos Service Mesh es robusto y muy seguro. La estrategia de IAP para el acceso de usuarios es la correcta y simplifica la gestión.
-   **Cuestionamiento a @arquitecto-plataforma y @arquitecto-datos**: Mi análisis de conectividad (`conectividad-actual.md`) muestra picos de replicación de Kafka de hasta 2.2 Gbps. Nuestro nuevo Dual Interconnect de 2 Gbps está en el límite. Aunque se menciona QoS y compresión, **¿deberíamos ser más explícitos sobre las políticas de throttling en Kafka?** Sugiero definir desde ahora que los tópicos no críticos (ej. logs, telemetría de baja prioridad) tendrán un límite de ancho de banda estricto en Cluster Linking para no impactar la replicación de datos críticos de CDC y SCADA.

### 2.3. Feedback de @admin-legados

-   **Punto Fuerte**: La estrategia "Edge-First" con GDC Edge es la única que garantiza la operación ininterrumpida de los SCADA antiguos. Resuelve el requisito de latencia <10ms de forma definitiva.
-   **Cuestionamiento a @arquitecto-plataforma**: La solución GDC Edge es ideal, pero implica nuevo hardware de Google en nuestras plantas. **¿Quién es el responsable del ciclo de vida de este hardware?** ¿El personal de OT local necesita capacitación para su mantenimiento básico (ej. cableado, reinicios físicos)? ¿Hemos validado los requisitos de energía, refrigeración y espacio físico en los racks de las plantas para estos nuevos servidores?

### 2.4. Feedback de @arquitecto-plataforma

-   **Punto Fuerte**: El diseño de datos con capas Medallion distribuidas (RAW/BRONZE en edge) es inteligente y aprovecha al máximo la capacidad de cómputo local de GDC Edge.
-   **Cuestionamiento a @arquitecto-datos**: Proponer el procesamiento de la capa BRONZE en el borde es bueno para optimizar el ancho de banda, pero introduce complejidad operativa. **¿Cuál es el plan para desplegar, monitorear y depurar estos pipelines de streaming (KSQL/Spark) que ahora corren en dos entornos distintos (edge y cloud)?** Necesitamos asegurar que la gestión sea consistente y no se convierta en un dolor de cabeza operacional.

---

## 3. Decisiones y Acciones a Tomar

Tras la discusión, el equipo ha llegado a las siguientes decisiones y acciones para refinar los diseños en la versión 2.

1.  **Topología de Clústeres Kafka (Acción para @arquitecto-plataforma)**: Se mantiene el diseño de 3 clústeres edge. La justificación es que la autonomía operativa de CADA planta es un requisito no negociable. Un modelo con un solo edge centralizado en Monterrey crearía una dependencia inter-planta que va en contra del principio de resiliencia. Se añadirá esta justificación explícita en `arquitectura-plataforma-v2.md`.

2.  **Gestión de Ancho de Banda (Acción para @experto-redes y @arquitecto-datos)**: Se acepta el riesgo del pico de 2.2 Gbps. En `arquitectura-redes-v2.md`, se añadirá una sección de **Políticas de QoS y Throttling**, especificando que el tráfico de replicación se dividirá en 3 clases de servicio. En `arquitectura-datos-v2.md`, se añadirán ejemplos de tópicos de baja prioridad que serán limitados.

3.  **Operaciones de GDC Edge (Acción para @admin-legados)**: Se añade un nuevo **riesgo** al proyecto: "Gestión del Ciclo de Vida y Operación del Hardware GDC Edge". En `migracion-legados.md` (Fase 3), se deberá incluir un plan de capacitación para el personal de OT y un checklist de requisitos físicos para la instalación de GDC Edge.

4.  **Gestión de Pipelines Distribuidos (Acción para @data-engineer y @devsecops)**: Se acepta el reto. En `pipelines-datos.md` (Fase 3), el Data Engineer deberá diseñar los pipelines con la observabilidad en mente (métricas y logs estandarizados). En `devsecops-gobierno.md`, el DevSecOps deberá asegurar que la pipeline de GitOps con Harness pueda desplegar y gestionar las aplicaciones de streaming de forma coherente en los clústeres del borde y la nube.

---

## 4. Conclusión de la Sesión

La revisión ha sido exitosa. Se han identificado 4 áreas clave de mejora que serán abordadas en la siguiente iteración de los documentos de diseño y en los planes de la Fase 3. La arquitectura general basada en GDC Edge se mantiene como la solución más robusta y adecuada. El siguiente paso es que los arquitectos refinen sus respectivos documentos a una versión 2.