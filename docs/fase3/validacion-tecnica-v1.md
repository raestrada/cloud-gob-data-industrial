# Sesión de Validación Técnica v1
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 3.4 - Revisión Cruzada de Diseño Detallado
**Fecha**: 2025-11-01
**Participantes**: @data-engineer, @devsecops, @admin-legados, @arquitecto-plataforma

---

## 1. Objetivo de la Sesión

Validar la viabilidad técnica de los planes de implementación detallados en la Fase 3. El objetivo es identificar riesgos prácticos, dependencias críticas y posibles bloqueadores antes de la ejecución.

Se han revisado los siguientes documentos:
- `pipelines-datos.md`
- `devsecops-gobierno.md`
- `migracion-legados.md`

---

## 2. Puntos de Discusión y Cuestionamientos

### 2.1. Feedback de @devsecops

-   **Punto Fuerte**: El plan de migración por ondas es claro y reduce el riesgo. La estrategia de containerización de los `.exe` es viable.
-   **Cuestionamiento a @data-engineer**: El diseño de pipelines propone usar **ksqlDB** en el borde y **Spark** en la nube. Esto implica dos runtimes y lenguajes diferentes. **¿Cómo vamos a unificar el CI/CD para ambos en Harness?** ¿Necesitaremos runners de CI/CD distintos en el GDC Edge y en la nube? Esto podría complicar la gestión de los pipelines y la experiencia del desarrollador.

### 2.2. Feedback de @admin-legados

-   **Punto Fuerte**: El modelo de gobierno con OPA es potente y el plan de seguridad es exhaustivo.
-   **Cuestionamiento a @data-engineer**: La estrategia de migración de SQL Server depende 100% de **Debezium CDC**. Nuestros servidores SQL on-premise ya están bajo una carga considerable. **¿Qué garantías tenemos de que habilitar CDC y el proceso de snapshotting inicial no impactarán el rendimiento de la producción?** Un impacto negativo aquí es un riesgo de negocio inaceptable. Propongo un PoC en un sistema de producción no crítico pero representativo antes de una aprobación completa.

### 2.3. Feedback de @arquitecto-plataforma

-   **Punto Fuerte**: El plan de migración por ondas está bien estructurado. La estrategia para los `.exe` es sólida.
-   **Cuestionamiento a @admin-legados**: El dimensionamiento del hardware de **GDC Edge** es un buen punto de partida, pero está marcado como un [SUPUESTO]. **¿Cuál es el tiempo de entrega (lead time) real para la adquisición e instalación de este hardware por parte de Google?** Si es de 3 a 6 meses, podría retrasar el inicio de la Onda 1. Esta es una dependencia crítica en nuestro cronograma.

### 2.4. Feedback de @data-engineer

-   **Punto Fuerte**: El modelo de seguridad con IAP y el Secrets Store CSI Driver es robusto y la forma correcta de gestionar secretos.
-   **Cuestionamiento a @devsecops**: Mi diseño de pipelines depende del acceso a secretos (credenciales de Kafka, BDs) a través del **Secrets Store CSI Driver**. **¿Hemos validado que este driver es estable y está oficialmente soportado en GDC Edge?** Además, ¿cuál es la estrategia para la rotación de secretos? Un pipeline de streaming no puede ser simplemente "reiniciado" para tomar un nuevo secreto sin riesgo de perder datos o estado.

---

## 3. Decisiones y Acciones a Tomar

1.  **CI/CD para ksqlDB y Spark (Acción para @devsecops)**: Se decide estandarizar los pipelines de Harness. Se creará una plantilla de CI/CD que pueda manejar ambos tipos de artefactos. Para ksqlDB, el pipeline simplemente versionará y aplicará los scripts SQL en un repositorio Git. Para Spark, el pipeline compilará el código, lo empaquetará en un contenedor y actualizará el manifiesto del Job de Kubernetes. Se documentará esto en `devsecops-gobierno.md`.

2.  **Riesgo de Rendimiento de CDC (Acción para @admin-legados y @data-engineer)**: Se acepta el riesgo. Se añade como requisito **obligatorio** un **PoC de Debezium en un sistema de producción no crítico** durante la Fase de Fundación (Onda 1). Se medirán la latencia, el uso de CPU y el I/O en el servidor SQL de origen. El resultado será un hito Go/No-Go para la migración masiva de SQL.

3.  **Lead Time de GDC Edge (Acción para @arquitecto-plataforma y Finanzas)**: Este es un riesgo crítico para el cronograma. Se debe contactar al equipo de cuentas de Google **en los próximos 7 días** para obtener una estimación formal del tiempo de entrega. El Plan Gantt (Fase 7) deberá reflejar esta dependencia.

4.  **Soporte de CSI Driver en GDC Edge (Acción para @devsecops)**: Se debe validar la compatibilidad y el soporte del Secrets Store CSI Driver con la versión de GDC Edge que se planea desplegar. Para la rotación de secretos, se diseñará un patrón donde los pipelines de streaming puedan recargar su configuración de forma periódica sin necesidad de un reinicio completo, utilizando un sidecar que monte los secretos actualizados.

---

## 4. Conclusión de la Sesión

La validación técnica ha sido exitosa, revelando 4 puntos clave que requieren acción o validación antes de la ejecución. Estos puntos no representan bloqueadores, pero sí dependencias importantes que deben ser gestionadas. Los diseños de la Fase 3 son técnicamente viables y coherentes entre sí. El siguiente paso es que los responsables de cada documento apliquen los refinamientos discutidos.