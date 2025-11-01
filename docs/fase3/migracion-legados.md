# Estrategia de Migración de Sistemas Legados v1
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 3.3 - Diseño de Migración de Legados
**Fecha**: 2025-11-01
**Responsable**: @admin-legados
**Versión**: 1.0

---

## 1. Resumen Ejecutivo

Este documento detalla la estrategia para migrar y modernizar los 380 sistemas legados on-premise a la nueva arquitectura basada en Google Distributed Cloud (GDC) Edge y GCP. La estrategia se centra en un enfoque por ondas, minimizando el riesgo y asegurando la continuidad operativa.

Los puntos clave son:
1.  **Plataforma Edge (GDC Edge)**: Se define una configuración de referencia para el hardware de GDC Edge en cada planta, dimensionada para soportar las cargas de trabajo locales de GKE, incluyendo los conectores de Kafka y los ejecutables `.exe` containerizados.
2.  **Estrategia para SCADA**: Los sistemas SCADA **no se migran, se integran**. La lógica de control permanece en el borde, y los datos de telemetría se capturan a través de conectores Kafka Connect (OPC-UA, Modbus) que corren en GDC Edge.
3.  **Estrategia para SQL Server**: La opción preferente es la migración a **Cloud SQL para SQL Server** utilizando un proceso de **Change Data Capture (CDC)** con Debezium para una transición con mínimo downtime.
4.  **Estrategia para `.exe`**: El enfoque principal es la **containerización**, empaquetando los ejecutables y sus dependencias en contenedores de Windows para ser orquestados por GKE en GDC Edge.
5.  **Plan de Migración por Ondas**: Se propone un plan de 3 ondas a lo largo de 18 meses, comenzando con los sistemas de menor riesgo (SQL 2008-2012) y terminando con los sistemas críticos.

---

## 2. Configuración de Google Distributed Cloud (GDC) Edge

La infraestructura de GDC Edge es la base para la modernización on-premise. Soportará los componentes que requieren baja latencia y operación autónoma.

### 2.1. Dimensionamiento (Sizing)

Basado en el inventario de `~1,900 vCPU y ~12.8TB RAM` y la necesidad de resiliencia local, se propone la siguiente configuración **por cada una de las 3 plantas**:

-   **[SUPUESTO] Configuración de Referencia GDC Edge por Planta**:
    -   **Nodos**: 4 nodos de cómputo y 2 nodos de control para alta disponibilidad.
    -   **CPU por Nodo**: 2 x 32-core CPU.
    -   **RAM por Nodo**: 512 GB.
    -   **Almacenamiento por Nodo**: 8 x 3.84 TB NVMe SSD.
    -   **Red por Nodo**: 2 x 100 Gbps.

-   **Justificación del Sizing**:
    -   Esta configuración proporciona capacidad suficiente para ejecutar el clúster GKE local, el clúster Kafka-Edge, los conectores de Kafka Connect, los pipelines de ksqlDB (capa BRONZE) y las cargas de trabajo de los `.exe` containerizados, con un 30-40% de headroom para crecimiento y picos de carga.
    -   **Acción Requerida**: Este es un supuesto inicial. Se debe validar con un especialista de Google y un partner de hardware para confirmar que el modelo de servidor cumple los requisitos de GDC Edge.

### 2.2. Cargas de Trabajo en GDC Edge

-   **GKE en GDC Edge**: Será el orquestador para todas las cargas de trabajo en la planta.
-   **Confluent for Kubernetes**: Para desplegar y gestionar los clústeres Kafka-Edge.
-   **Kafka Connect**: Workers para los conectores Debezium (SQL) y OPC-UA/Modbus (SCADA).
-   **ksqlDB**: Para el procesamiento de streaming de la capa BRONZE.
-   **Contenedores Windows**: Para ejecutar las aplicaciones `.exe` migradas.

### 2.3. Riesgos y Dependencias de GDC Edge

-   **[RIESGO CRÍTICO] Tiempo de Entrega del Hardware**: El cronograma del proyecto depende del tiempo de adquisición e instalación del hardware de GDC Edge. Se debe contactar a Google en los próximos 7 días para obtener una estimación formal. Este es un posible bloqueador para el inicio de la Onda 1.
-   **[RIESGO OPERACIONAL] Mantenimiento y Capacitación**: El personal de OT local requiere capacitación para el mantenimiento físico básico de los nuevos servidores. Se debe definir un modelo de soporte claro con el proveedor del hardware y Google.

---

## 3. Estrategia de Migración por Sistema

### 3.1. Sistemas SCADA Antiguos

-   **Estrategia**: **Integración, no migración**.
-   **Detalle**: La lógica de control y las HMIs que requieren latencia <10ms permanecen en sus sistemas actuales. Nuestro objetivo es capturar sus datos.
-   **Implementación**: Se desplegarán conectores de Kafka Connect en GDC Edge.
    -   Para sistemas como GE iFIX que soportan **Modbus TCP**, se usará un conector Modbus Source.
    -   Para sistemas como Siemens WinCC y Allen-Bradley que usan **OPC-DA/DDE**, se instalará un software de **Gateway OPC** (ej. Kepware, Ignition) en una VM de Windows en GDC Edge. Este gateway expondrá los datos vía **OPC-UA**, un protocolo moderno que sí tiene un conector de Kafka Connect robusto.

### 3.2. Bases de Datos SQL Server

-   **Destino Recomendado**: **Cloud SQL para SQL Server**.
    -   **Justificación**: Es un servicio totalmente gestionado que reduce drásticamente la carga operativa de parches, backups, y alta disponibilidad. Su costo es predecible y se integra con el resto de GCP.
    -   **Alternativa**: Usar SQL Server en una VM de Compute Engine solo si una aplicación tiene dependencias a nivel de sistema operativo que Cloud SQL no soporta (caso muy excepcional).

-   **Estrategia de Replicación con Debezium (CDC)**:
    1.  **Instalación**: Desplegar el conector Debezium para SQL Server en los workers de Kafka Connect en GDC Edge.
    2.  **Snapshot Inicial**: Durante una ventana de mantenimiento planificada, el conector realizará un snapshot inicial consistente de la base de datos. Para bases de datos muy grandes, esto puede requerir varias horas.
    3.  **Streaming de Cambios**: Tras el snapshot, Debezium comenzará a leer el log de transacciones de la base de datos de origen y publicará cada cambio (INSERT, UPDATE, DELETE) como un evento en un tópico de Kafka.
    4.  **Cutover**: Una vez que la replicación esté estabilizada y los datos validados, se planificará una segunda ventana de mantenimiento para detener las aplicaciones, asegurar que todos los cambios se hayan replicado, y apuntar las aplicaciones a la nueva base de datos en Cloud SQL.

### 3.3. Procedimientos Almacenados con `.exe` locales

-   **Problema**: Los Stored Procedures que ejecutan `xp_cmdshell` para llamar a ejecutables locales son un bloqueador para la migración a Cloud SQL.
-   **Estrategia Principal**: **Containerización y Refactorización del Orquestador**.
    1.  **Containerizar el `.exe`**: Cada ejecutable se empaquetará en un contenedor de Windows Server. Este contenedor se desplegará en el clúster GKE de GDC Edge.
    2.  **Refactorizar el SP**: El Stored Procedure original será modificado. En lugar de llamar a `xp_cmdshell`, publicará un **evento** en un tópico de Kafka (ej. `edge.command.run_report_generator`).
    3.  **Orquestación por Eventos**: Un pequeño servicio o pipeline (ej. en KSQL o una Cloud Function) escuchará ese tópico de Kafka y, al recibir un evento, lanzará el contenedor correspondiente como un `Job` de Kubernetes.
-   **Ventajas**: Desacopla la base de datos de la ejecución de procesos, mejora la observabilidad y permite que los procesos se reintenten de forma resiliente.

---

## 4. Plan de Migración por Ondas

Se propone un plan de 3 ondas para distribuir el riesgo y el esfuerzo a lo largo de 18 meses.

-   **Onda 1 (Meses 1-6): Fundación y Bajo Riesgo**
    -   **Infraestructura**: Despliegue y configuración del hardware GDC Edge en las 3 plantas. Configuración de la red (Interconnect, PSC, Anthos Service Mesh).
    -   **Hito Go/No-Go: PoC de Debezium**: Antes de la migración masiva, ejecutar una Prueba de Concepto de CDC en un sistema SQL Server de producción no crítico pero representativo. Medir el impacto en el rendimiento (CPU, I/O) del servidor de origen. El resultado debe ser un impacto <5% para proceder.
    -   **Sistemas**: Migrar las **100 instancias de SQL Server 2008-2012** a Cloud SQL. Estas están fuera de soporte y su migración reduce un riesgo de seguridad importante.
    -   **Aplicaciones**: Containerizar y migrar los 10-15 ejecutables `.exe` más simples y de menor riesgo.
    -   **Hito de Salida**: Infraestructura base operativa. Sistemas legacy más vulnerables modernizados. Viabilidad de CDC validada.

-   **Onda 2 (Meses 7-12): Expansión y Datos No Críticos**
    -   **Sistemas**: Migrar la mayoría de las **90 aplicaciones IIS** que no son de misión crítica. Iniciar la replicación CDC con Debezium para las bases de datos SQL Server 2019 **no críticas**.
    -   **Integración**: Desplegar los conectores Kafka para los **30 SCADA modernos**.
    -   **Hito de Salida**: El 60% de las aplicaciones y fuentes de datos están en la nueva plataforma. El equipo gana experiencia antes de abordar los sistemas críticos.

-   **Onda 3 (Meses 13-18): Migración de Sistemas Críticos**
    -   **Sistemas**: Ejecutar el plan de cutover para las **120 instancias de SQL Server 2019 críticas**. Esto requerirá ventanas de mantenimiento dominicales coordinadas.
    -   **Integración**: Desplegar los gateways y conectores para los **40 SCADA antiguos**.
    -   **Aplicaciones**: Migrar las últimas aplicaciones IIS críticas que dependen de las bases de datos de SQL 2019.
    -   **Hito de Salida**: El 100% de los sistemas están migrados o integrados. La infraestructura on-premise tradicional puede ser decomisionada.

---

## 5. Runbooks de Escalación (Ejemplos)

-   **Runbook 1: Falla en Replicación CDC de Debezium**
    1.  **Detección**: Alerta de Grafana/Cloud Monitoring por lag de replicación > 15 minutos.
    2.  **Análisis (5 min)**: El Data Engineer revisa los logs del conector Debezium en GKE. ¿Hay errores de conexión? ¿Cambio de esquema no compatible?
    3.  **Acción Inmediata (10 min)**: Si es un error transitorio, reiniciar el conector (`kubectl rollout restart deployment/debezium-connector`).
    4.  **Escalación (15 min)**: Si el reinicio falla, pausar el conector. Notificar al equipo de aplicaciones que la réplica en la nube no está actualizada. La aplicación sigue funcionando contra la base de datos on-premise sin impacto.
    5.  **Resolución**: El DBA y el Data Engineer investigan la causa raíz (ej. tabla sin PK, cambio de esquema incompatible) y planifican una corrección.

-   **Runbook 2: Falla de un Nodo de GDC Edge**
    1.  **Detección**: Alerta de Anthos/Cloud Monitoring por nodo `NotReady`.
    2.  **Análisis (5 min)**: GKE en GDC Edge automáticamente reprograma los pods (Kafka, conectores) en los nodos restantes. No debería haber impacto en el servicio gracias a la configuración HA.
    3.  **Acción Inmediata (30 min)**: El equipo de OT local realiza una inspección física del servidor. ¿Hay alertas de hardware? ¿Problema de red?
    4.  **Escalación (1-2 horas)**: Si es una falla de hardware, se abre un ticket con el proveedor de hardware de GDC Edge para su reemplazo según el SLA contratado.
    5.  **Resolución**: Una vez reemplazado el hardware, el nodo se une de nuevo al clúster y Anthos lo re-provisiona automáticamente.