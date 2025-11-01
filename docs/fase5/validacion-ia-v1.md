# Sesión de Validación del MVP de IA para FinOps v1
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 5.2 - Revisión Cruzada del MVP de IA
**Fecha**: 2025-11-01
**Participantes**: @data-scientist, @finanzas, @data-engineer, @devsecops

---

## 1. Objetivo de la Sesión

Validar el MVP de IA para FinOps (`mvp-ia-finops.md`) contra los requisitos específicos del Caso de Negocio PDF. El objetivo es evaluar si el MVP cumple con las expectativas y definir los siguientes pasos para su operacionalización.

---

## 2. Validación Cruzada contra Requisitos del Caso de Negocio

### 2.1. Requisito 1: Forecast de Costos

-   **Requisito PDF**: "Forecast de costos por proyecto/BU/onda usando el dataset provisto... puedes usar... regresión".
-   **Validación**: 
    -   ✅ Se utilizó el dataset provisto.
    -   ✅ Se usó un modelo de regresión.
    -   ⚠️ **GAP IDENTIFICADO**: El modelo actual es un agregado total, no está desglosado "por proyecto/BU/onda" como pide el requisito. Es una buena prueba de concepto, pero no es directamente accionable para el negocio.
-   **Discusión (`@finanzas`)**: Para que esto sea útil, necesitamos que el forecast se alinee con las ondas de migración. El costo no crecerá de forma lineal, sino en "escalones" a medida que migramos cada onda. 
-   **Acción para v2**: El `@data-scientist` deberá evolucionar el modelo para que acepte las "ondas de migración" como una feature, permitiendo un forecast más granular y realista.

### 2.2. Requisito 2: Detección de Anomalías

-   **Requisito PDF**: "Detección de anomalías (reglas + umbrales dinámicos...) y **flujo de respuesta (detección → owner → corrección)**".
-   **Validación**:
    -   ✅ Se implementó un modelo con umbrales dinámicos (basado en desviación estándar).
    -   ❌ **GAP IDENTIFICADO**: No se ha diseñado el "flujo de respuesta" automático.
-   **Discusión (`@data-engineer`)**: Un modelo que solo imprime en la consola no es útil. Propongo que, cuando el script detecte una anomalía, **publique un evento** en un tópico de Kafka dedicado: `cloud.finops.anomalies`. El evento debe contener todos los detalles de la anomalía y el `owner` inferido por el modelo NLP.
-   **Acción para v2**: El `@data-scientist` modificará el script para que publique eventos en Kafka. El `@devsecops` diseñará un `Cloud Function` que se active con ese tópico y envíe una alerta al `owner` (ej. email o ticket en Jira).

### 2.3. Requisito 3: Etiquetado NLP

-   **Requisito PDF**: "cómo inferir `owner/cost_center/criticality`... y **proceso de validación humana**."
-   **Validación**:
    -   ✅ Se implementó un modelo que infiere los 3 tags solicitados (`owner`, `cost_center`, `criticality`).
    -   ❌ **GAP IDENTIFICADO**: No se ha diseñado el "proceso de validación humana".
-   **Discusión (`@devsecops`)**: El etiquetado automático es clave, pero necesita un control. Propongo integrar esto en el pipeline de CI/CD de Harness. Si el modelo NLP infiere las etiquetas con alta confianza (ej. todas las etiquetas encontradas), el pipeline continúa. Si la confianza es baja (ej. `owner` es `unknown`), el pipeline de Harness debe **pausar y solicitar una aprobación manual** a un miembro del equipo FinOps antes de permitir el despliegue.
-   **Acción para v2**: El `@devsecops` diseñará esta etapa de aprobación manual en los pipelines de Harness. El `@data-scientist` refinará el modelo NLP para que devuelva un "score de confianza" junto con las etiquetas.

---

## 3. Conclusión de la Validación

El MVP **cumple con las expectativas iniciales** de demostrar la viabilidad de los tres conceptos. Ha utilizado correctamente los datos y los algoritmos propuestos son un excelente punto de partida.

Sin embargo, la validación contra los requisitos específicos del caso de negocio ha revelado que para que el MVP sea operacional y realmente aporte valor, se deben implementar los flujos de integración y los procesos de validación humana que se han omitido en esta primera versión.

Las acciones definidas para la "v2" de este MVP son claras y permitirán pasar de una prueba de concepto a una herramienta de FinOps funcional e integrada en nuestros procesos.

---

## 4. Próximos Pasos

-   **Data Scientist**: Refinar los modelos de IA para incorporar las mejoras discutidas (forecast por ondas, publicación de anomalías en Kafka, scores de confianza para NLP).
-   **DevSecOps y Data Engineer**: Diseñar los flujos de integración para operacionalizar los modelos (alertas desde Kafka, pausas de aprobación en Harness).
-   **Fase 5 Concluida**: Dado que el objetivo del MVP (demostrar viabilidad) se ha cumplido, se da por concluida la Fase 5. Los refinamientos se realizarán como parte del ciclo de mejora continua una vez que la plataforma esté operativa.