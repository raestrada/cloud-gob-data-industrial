# Caso de Negocio: Migración a Plataforma Cloud Híbrida GCP

**Proyecto**: Migración Industrial a GCP con Arquitectura Event-Driven
**Fecha**: 2025-11-01
**Versión**: 1.0

---

### 1. Resumen Ejecutivo

**La Situación Actual**: Nuestra infraestructura on-premise, con un TCO a 3 años de **$15.7M**, enfrenta riesgos críticos de obsolescencia (100 servidores SQL fuera de soporte), resiliencia (cortes de energía en plantas) y una estructura de costos fijos (87% del OPEX) que impide la agilidad.

**La Solución Propuesta**: Se propone una migración en 18 meses a una arquitectura "Edge-First" nativa de Google Cloud. La operación crítica se ejecutará en **Google Distributed Cloud (GDC) Edge** en cada planta, garantizando autonomía y resiliencia local (RPO/RTO=0). Los datos se consolidarán en un **Data Hub en GCP** mediante una plataforma de eventos con Confluent Kafka, habilitando la analítica avanzada y la recuperación ante desastres a nivel de negocio.

**El Impacto Financiero**: La inversión es financieramente muy atractiva. Proyectamos una **reducción del TCO del 49.6%**, generando un **ahorro de $7.8M** a 3 años. Con un **ROI del 98%** y un **período de payback de ~12 meses**, el proyecto se financia a sí mismo rápidamente y reduce el costo de TI por unidad producida en más de un 50%.

**La Decisión Requerida**: Se solicita la aprobación del proyecto y de una inversión inicial (CAPEX) de **$2.15M** (con un déficit de $150k sobre el presupuesto inicial, para el cual se proponen soluciones) para iniciar la transformación, mitigar los riesgos actuales y posicionar a la compañía para una futura innovación basada en datos.

---

### 2. Situación Actual y Desafíos

- **Infraestructura Envejecida**: El 35% de las bases de datos (100 instancias SQL 2008/2012) están fuera de soporte, representando un riesgo de seguridad inaceptable.
- **Baja Resiliencia**: Los centros de datos sub-Tier 3, particularmente en Tijuana, sufren de cortes de energía que impactan la producción, con un costo por incidente estimado en más de $800,000.
- **Falta de Agilidad**: El 87% de los costos de TI son fijos, lo que dificulta escalar o reducir la capacidad según la demanda del negocio.
- **Deuda Técnica**: Se estima que existen más de 200 Stored Procedures que invocan ejecutables `.exe` locales, una práctica que impide la modernización y la portabilidad.
- **Silos de Datos**: No existe una plataforma central de datos, lo que dificulta la analítica multi-planta y la toma de decisiones basada en datos globales.

---

### 3. Principios de la Arquitectura Propuesta

La solución se basa en los siguientes principios de diseño:

1.  **Operación Autónoma en el Borde (Edge-First)**: Cada planta opera de forma autónoma en GDC Edge, eliminando la dependencia de la conectividad a la nube para la producción.
2.  **Plano de Control Unificado**: Anthos gestiona de forma consistente todos los clústeres de Kubernetes (GKE), tanto en el borde como en la nube.
3.  **Conectividad Privada por Defecto**: No se exponen IPs públicas. La comunicación se realiza a través de Private Service Connect y Anthos Service Mesh (mTLS).
4.  **Aislamiento de Red por VPC**: Cada servicio se despliega en su propia VPC, eliminando la necesidad de gestión de direccionamiento IP (IPAM).
5.  **Arquitectura Orientada a Eventos (EDA)**: Kafka actúa como el sistema nervioso central, desacoplando sistemas y habilitando la agilidad.

---

### 4. Arquitectura de Plataforma, Datos y Red

-   **Plataforma**: Se despliega una topología Hub-and-Spoke con 3 clústeres **GKE en GDC Edge** (uno por planta) y 2 clústeres de **Confluent Cloud** en GCP para el Hub central y el DR.
-   **Datos**: Se implementa una **arquitectura Medallion de 4 capas** distribuida. Las capas RAW y BRONZE (limpieza técnica) se procesan en el borde para optimizar el ancho de banda. Las capas SILVER (lógica de negocio) y GOLD (agregados) se procesan en la nube. Los datos se almacenan en un **Lakehouse (GCS)** y un **Data Warehouse (BigQuery)**.
-   **Red**: La conectividad se basa en un **Dual Interconnect de 2x1Gbps**. El acceso a servicios se abstrae a través de una jerarquía de comunicación: **Kafka (asíncrono) > Anthos Service Mesh (síncrono) > PSC > Apigee**.
-   **Seguridad**: El acceso de usuarios se gestiona con **Identity-Aware Proxy (IAP)**, proveyendo un modelo Zero-Trust sin necesidad de VPNs.

---

### 5. Modelo Financiero a 3 Años

| Métrica | On-Premise (Actual) | Cloud (Proyectado) | Resultado |
| :--- | :--- | :--- | :--- |
| **TCO a 3 Años** | $15,735,000 | **$7,937,180** | ▼ **Ahorro de $7.8M (49.6%)** |
| **OPEX Anual (Run Rate)** | $5,245,000 | **$2,214,872** | ▼ **Ahorro de $3.0M (57.8%)** |
| **CAPEX Requerido** | $1,830,000 (para crecimiento) | **$2,150,000** (para migración) | - |

-   **Análisis vs. Objetivos**:
    -   **ROI**: **98.24%** (Objetivo: >15%)
    -   **Payback**: **~12 meses** (Objetivo: <24 meses)
    -   **CAPEX**: **Excede el presupuesto en $150k**. Se recomienda ajustar el supuesto de costo de hardware de GDC Edge y validarlo con Google de forma prioritaria.

---

### 6. Modelo Operativo y Gobierno (GitOps + OPA)

-   **Todo como Código**: Toda la configuración de la plataforma (infraestructura, políticas, aplicaciones) se gestionará en repositorios Git.
-   **GitOps**: Anthos Config Management sincronizará el estado de los clústeres con los repositorios Git.
-   **Gobierno por Políticas**: Se usará Open Policy Agent (OPA) en un modelo de **defensa en profundidad**:
    1.  **Harness (Pipeline)**: Validará los manifiestos antes del despliegue (Shift-Left).
    2.  **Anthos Policy Controller (Clúster)**: Bloqueará en runtime cualquier configuración no permitida.
-   **FinOps**: Se implementará un plan de 30-60-90 días para establecer visibilidad (etiquetado, dashboards), optimización (right-sizing) y automatización (políticas de costos con OPA).

---

### 7. Matriz de Riesgos Principales

| ID | Riesgo | Impacto | Mitigación Clave |
| :--- | :--- | :--- | :--- |
| **R-10** | El costo real del hardware GDC Edge excede el supuesto. | Alto | Obtener una cotización formal de Google en los primeros 30 días. |
| **R-04** | Brecha de habilidades en el equipo para adoptar GCP/Anthos. | Alto | Iniciar plan de capacitación y certificación agresivo, apoyado por expertos externos. |
| **R-05** | Picos de tráfico saturan el Interconnect de 2Gbps. | Alto | Implementar QoS y throttling en Kafka para priorizar tráfico crítico. |
| **R-02** | La viabilidad del RPO de segundos para DR no es suficiente. | Alto | Aceptar este RPO para DR a nivel de negocio, ya que el RPO=0 se garantiza localmente. |
| **R-03** | Algunos ejecutables `.exe` no pueden ser containerizados. | Medio | Mantener una pequeña granja de VMs Windows como último recurso y exponerlos vía API. |

---

### 8. Próximos Pasos (Plan 30-60-90 Días)

-   **Próximos 30 Días**:
    -   **Obtener Aprobación del Proyecto** por parte del Comité Ejecutivo.
    -   **Validar Supuestos Críticos**: Contactar a Google para cotización y cronograma de GDC Edge.
    -   **Iniciar Onda 1**: Comenzar el PoC de Debezium en un sistema no crítico y arrancar el plan de capacitación.
-   **Próximos 60 Días**:
    -   **Desplegar Infraestructura Base**: Configurar la red en GCP y comenzar la instalación del hardware GDC Edge.
    -   **Comenzar Migración**: Iniciar la migración de las 100 instancias de SQL Server 2008-2012.
-   **Próximos 90 Días**:
    -   **Implementar Gobierno FinOps**: Desplegar políticas OPA para etiquetado y configurar dashboards de costos.
    -   **Primeros Resultados**: Tener los primeros sistemas legacy corriendo en Cloud SQL y los primeros `.exe` containerizados en GDC Edge.
