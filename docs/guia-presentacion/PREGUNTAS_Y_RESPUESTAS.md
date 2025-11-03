# Guía de Preguntas y Respuestas (P&R) para la Defensa del Proyecto

Este documento consolida las preguntas más probables que pueden surgir durante la presentación del proyecto, junto con respuestas sugeridas y bien fundamentadas. El objetivo es que el presentador pueda anticipar y responder con confianza, demostrando un dominio total del caso de negocio y la solución técnica.

---

## A. Preguntas Financieras (ROI, Costos, Presupuesto)

**P1: El ROI del 114% parece muy alto. ¿Es realista para un proyecto de este tipo?**

**Respuesta:** Sí, es un ROI alto pero completamente realista y defendible para este caso específico. La razón es que no estamos haciendo una simple migración, sino una transformación que resuelve problemas de negocio extremadamente costosos. Nuestro punto de partida es uno de alta ineficiencia y riesgo, lo que magnifica el retorno de la inversión.

**P2: ¿Existen otras experiencias en la industria que respalden un ROI tan alto?**

**Respuesta:** Sí. Un ROI superior al 100% es común en proyectos que, como el nuestro, logran tres cosas: 1) Eliminan pérdidas de negocio directas y cuantificables (como nuestras paradas de producción de $3.2M/año). 2) Descomisionan infraestructura legacy muy costosa y riesgosa (análogo a apagar un mainframe). 3) Evitan multas o incidentes de seguridad millonarios (como nuestro riesgo con las BD sin soporte). Nuestro proyecto encaja perfectamente en este perfil de 'transformación de alto impacto'.

**P3: El CAPEX inicial de $2.15M es considerable. ¿Por qué es tan alto y cómo se justifica?**

**Respuesta:** Es una inversión estratégica, no un gasto. Se justifica porque: 1) Es menos de la mitad de lo que costaría solo renovar el hardware on-premise ($5.9M). 2) Desbloquea un ahorro total de $8.4M a 3 años. 3) Se recupera en solo 11 meses gracias a los enormes ahorros operativos que genera. El componente principal es el hardware GDC Edge, que es la pieza clave para garantizar la autonomía y resiliencia de las plantas.

**P4: ¿Qué pasa si los costos de la nube son más altos de lo previsto? ¿Cómo evitamos el "bill shock"?**

**Respuesta:** Hemos abordado esto con un enfoque triple: 1) **Arquitectura Eficiente:** El procesamiento en el Edge reduce el tráfico de red, uno de los costos cloud más variables, en un 60-70%. 2) **Optimización Predictiva:** Usamos Cast.ai, que optimiza los costos de cómputo de forma proactiva, logrando ahorros de hasta un 40%. 3) **Gobierno FinOps:** Implementamos un modelo de gobierno con presupuestos, alertas y políticas OPA que previenen despliegues costosos antes de que ocurran. Nuestro modelo financiero ya incluye un escenario pesimista que sigue siendo muy favorable (ROI 84%).

**P5: El plan muestra un déficit de $150K en el CAPEX. ¿Cómo se planea manejar?**

**Respuesta:** Lo hemos identificado y es manejable. Tenemos dos vías principales para mitigarlo: 1) Negociación con Google: Como parte de una alianza estratégica, buscaremos créditos o descuentos en el hardware GDC Edge. 2) Optimización de Fases: Podemos re-fasar la compra de ciertos componentes no esenciales para la Onda 1, financiándolos con los ahorros operativos generados en los primeros meses.

---

## B. Preguntas Técnicas y de Arquitectura

**P6: ¿Cómo ayuda exactamente la arquitectura "Edge-First" si hay un corte de energía en la planta?**

**Respuesta:** Es una aclaración importante. El Edge no genera electricidad. Para eso, la planta ya cuenta con generadores de respaldo para su maquinaria crítica. Nuestra solución conecta la infraestructura de TI crítica (GDC Edge) a esos mismos generadores. El problema que resolvemos es la **parálisis por pérdida de conectividad**. Con GDC Edge, la planta opera de forma 100% autónoma. Si se cae la red de internet, la producción no se detiene, evitando las pérdidas de $3.2M. Los datos se sincronizan a la nube cuando la conexión se restablece.

**P7: ¿Por qué eligieron Google Cloud (GCP) sobre AWS o Azure?**

**Respuesta:** La decisión se basó en un factor clave para nuestro caso: la **solución integrada de Edge a Cloud**. Google Distributed Cloud (GDC) Edge, junto con Anthos para la gestión unificada, es la oferta más madura y cohesiva para operar un entorno híbrido como si fuera una única nube. Esto reduce drásticamente la complejidad operativa, que era un requisito fundamental.

**P8: Insisto, ¿por qué Confluent Kafka y no un servicio nativo como Google Pub/Sub que simplificaría el stack?**

**Respuesta:** Evaluamos Pub/Sub, pero Kafka fue superior para este caso por tres razones críticas: 1) **Conectores Legados:** El ecosistema de Kafka Connect, especialmente con Debezium para Change Data Capture, es vital para extraer datos de nuestros SQL Server y sistemas SCADA antiguos sin modificarlos. 2) **Garantías de Entrega:** Requerimos semántica `exactly-once` y orden estricto en particiones, algo que Kafka maneja de forma más robusta para casos de uso industriales. 3) **Replicación Inter-cluster:** Cluster Linking de Confluent es una tecnología probada para la replicación de baja latencia entre Edge y Cloud, superando a las alternativas.

**P9: Esta arquitectura parece muy compleja. ¿Tenemos el talento interno para gestionarla?**

**Respuesta:** Reconocemos la brecha de habilidades como uno de los riesgos principales del proyecto. Nuestro plan lo aborda directamente con un programa de capacitación de 6 meses para 12 FTEs y la contratación de 1 a 2 expertos externos en GCP/Anthos/Kafka. La inversión en nuestra gente es tan importante como la inversión en tecnología. Además, la estandarización en Kubernetes (Anthos) tanto en el Edge como en la Cloud simplifica la curva de aprendizaje.

**P10: ¿Cuál es el plan para los más de 200 Stored Procedures que llaman a ejecutables (.exe)?**

**Respuesta:** Este es un punto crítico de la deuda técnica. El plan es abordarlos con una estrategia de **replatform/refactor**. En la Onda 1, usaremos Debezium (CDC) para capturar los cambios en los datos a nivel de base de datos, **evitando por completo la ejecución de los SPs**. Esto nos da tiempo. En paralelo, durante las Ondas 2 y 3, los equipos de desarrollo analizarán la lógica de negocio de esos `.exe` y la re-implementarán como microservicios en GKE o Cloud Functions, eliminando la dependencia de forma definitiva.

---

## C. Preguntas Estratégicas y de Negocio

**P11: ¿Por qué debemos hacer esta inversión ahora? ¿No podemos esperar un año?**

**Respuesta:** No. Esperar un año significa: 1) Aceptar otro año de pérdidas potenciales de $3.2M por inactividad. 2) Mantener 100 bases de datos críticas en riesgo de un ciberataque sin parches de seguridad disponibles. 3) Perder $2.9M en ahorros operativos. El costo de no hacer nada es mucho mayor que el costo del proyecto.

**P12: Es un proyecto de 18 meses. ¿Cuándo veremos el primer retorno tangible?**

**Respuesta:** Veremos valor muy temprano. En los primeros 6 meses (Onda 1), migraremos las 100 bases de datos fuera de soporte, eliminando nuestro riesgo de seguridad más grande. A los 11 meses, el proyecto alcanza el payback y comienza a generar ahorros netos. El valor no llega al final, se entrega en cada ola.

**P13: ¿Qué pasa si las prioridades del negocio cambian y necesitamos acelerar la analítica?**

**Respuesta:** La arquitectura está diseñada para ser flexible. Como todos los datos fluirán a través de la plataforma de eventos Kafka desde el día uno, podemos adaptar las prioridades de los consumidores de datos. Si la analítica se vuelve prioritaria, podemos asignar más recursos al equipo de Data Science para que consuman los datos del Hub en la nube y generen modelos, sin detener el plan de migración de la infraestructura crítica.

**P14: ¿Por qué no simplemente arreglar los problemas on-premise? Sería más barato que ir a la nube.**

**Respuesta:** A corto plazo, podría parecer más barato, pero sería un error estratégico. Arreglar lo on-premise implicaría un gasto de casi $6M solo en hardware nuevo, sin resolver los problemas de fondo: la falta de agilidad, la dificultad para consolidar datos y la alta carga operativa. Sería gastar mucho dinero para quedarnos en el mismo lugar. La nube nos ofrece una solución a largo plazo que es más barata, más segura y nos prepara para el futuro de la industria 4.0.

---

## D. Preguntas sobre Riesgos y Ejecución

**P15: ¿Cuál es, en su opinión, el riesgo número uno del proyecto y qué lo mantiene despierto por la noche?**

**Respuesta:** El riesgo principal no es técnico, es organizacional: la **gestión del cambio y la adopción**. La tecnología funcionará, pero debemos asegurar que nuestros equipos de TI y Operaciones (OT) adopten las nuevas herramientas y procesos (GitOps, FinOps). Por eso, nuestro plan tiene un pilar fundamental en la capacitación, la comunicación y la creación de un Centro de Excelencia Cloud (CCoE) desde el primer día.

**P16: ¿Cuál es el plan de rollback si la migración de un sistema crítico falla durante el fin de semana?**

**Respuesta:** Tenemos un plan de rollback detallado para cada tipo de carga. Para los sistemas críticos de la Onda 3, el proceso es: 1) La base de datos on-premise se mantiene como réplica de solo lectura durante el cutover. 2) Si la aplicación en la nube presenta un error crítico, el proceso de rollback consiste en revertir la configuración del DNS/balanceador de carga para apuntar de nuevo al sistema on-premise. 3) El tiempo estimado para este rollback es inferior a 2 horas, manteniéndonos dentro de la ventana de mantenimiento dominical.

**P17: El plan depende de la entrega de hardware GDC Edge por parte de Google. ¿Qué pasa si se retrasan?**

**Respuesta:** Es un riesgo identificado (R-13). La mitigación es confirmar el cronograma de entrega con Google en los primeros 7 días del proyecto. Si hay un retraso, el plan es flexible. Podríamos iniciar la Onda 1 (migración de BD que no dependen del Edge) en paralelo mientras llega el hardware, ajustando el Gantt para no impactar la fecha final de entrega del proyecto.
