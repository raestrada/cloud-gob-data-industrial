# Diagramas Consolidados de Arquitectura
**Proyecto**: Migración Industrial a Google Cloud Platform
**Fase**: 6.2 - Consolidación de Diagramas
**Fecha**: 2025-11-01
**Responsable**: @arquitecto-plataforma

---

## 1. Arquitectura de Alto Nivel (End-to-End)

Este diagrama muestra la visión completa de la plataforma, desde el borde on-premise hasta la nube, incluyendo el plano de control unificado con Anthos.

```mermaid
graph TD
    subgraph "On-Premise (Spokes)"
        subgraph "Planta (Google Distributed Cloud Edge)"
            SOURCES["Fuentes Legadas<br/>(SCADA, SQL Server)"]
            KAFKA_EDGE["Cluster Kafka Edge<br/>(GKE on GDC Edge)"]
            SOURCES --> KAFKA_EDGE
        end
    end

    subgraph "Google Cloud Platform (Hub)"
        direction LR
        subgraph "Región Primaria: us-central1"
            KAFKA_HUB["Cluster Kafka Hub<br/>(Confluent Cloud)"]
            GKE_PROD["Cargas de Trabajo Cloud<br/>(GKE, Dataproc, Apps)"]
            PERSISTENCE["Capa de Persistencia<br/>(BigQuery, GCS)"]
            KAFKA_HUB --> GKE_PROD --> PERSISTENCE
        end
        subgraph "Región DR: us-west1"
            KAFKA_DR["Cluster Kafka DR<br/>(Confluent Cloud)"]
        end
        KAFKA_HUB -- "Replicación DR" --> KAFKA_DR
    end

    CONTROL_PLANE["Plano de Control<br/>(Anthos)"]

    KAFKA_EDGE -- "Conectividad Privada<br/>(Interconnect, PSC, mTLS)" --> KAFKA_HUB
    CONTROL_PLANE -- "Gestiona" --> KAFKA_EDGE
    CONTROL_PLANE -- "Gestiona" --> GKE_PROD
```

---

## 2. Topología Kafka y Replicación

Este diagrama detalla la topología de 5 clústeres de Kafka y cómo se utiliza Cluster Linking para la replicación desde el borde a la nube y para la recuperación ante desastres.

```mermaid
graph TD
    subgraph "GCP Cloud"
        direction LR
        KAFKA_HUB["<b>kafka-hub-central1</b><br/>(us-central1)"]
        KAFKA_DR["<b>kafka-dr-west1</b><br/>(us-west1)"]
        KAFKA_HUB -- "Cluster Linking (DR)" --> KAFKA_DR
    end

    subgraph "Plantas On-Premise (GDC Edge)"
        KAFKA_MTY["<b>kafka-edge-mty</b>"]
        KAFKA_GDL["<b>kafka-edge-gdl</b>"]
        KAFKA_TIJ["<b>kafka-edge-tij</b>"]
    end

    KAFKA_MTY -- "Cluster Linking" --> KAFKA_HUB
    KAFKA_GDL -- "Cluster Linking" --> KAFKA_HUB
    KAFKA_TIJ -- "Cluster Linking" --> KAFKA_HUB
```

---

## 3. Flujo de Datos (Arquitectura Medallion)

Este diagrama muestra el flujo de datos a través de las 4 capas de la arquitectura Medallion, desde la ingesta en crudo en el borde hasta las agregaciones de negocio en la nube.

```mermaid
graph TD
    subgraph "EDGE (Plantas - GDC Edge)"
        direction LR
        A[Fuentes: SCADA, SQL Server] --> B(Kafka Connect)
        B --> C{Cluster Kafka Local}
        subgraph "Procesamiento Edge"
            C -- Ingesta 1:1 --> D[Tópico RAW]
            D -- Limpieza Técnica --> E[Tópico BRONZE]
        end
    end

    subgraph "CLOUD (GCP)"
        direction LR
        G{Cluster Kafka Hub}
        subgraph "Procesamiento Cloud"
            G -- Enriquecimiento --> H[Tópico SILVER]
            H -- Agregación de Negocio --> I[Tópico GOLD]
        end
        subgraph "Capa de Persistencia"
            I --> J(Kafka Connect Sink)
            J --> K[GCS Data Lakehouse]
            J --> L[BigQuery DW]
        end
    end

    E -- "Cluster Linking (Solo Tópicos Bronze)" --> G
```

---

## 4. Arquitectura de Red y Seguridad (Zero-Trust)

Este diagrama detalla el flujo de comunicación privada para servicios (PSC) y para usuarios (IAP), mostrando el modelo de seguridad Zero-Trust.

```mermaid
graph LR
    subgraph "Internet"
        USER["Usuario Remoto"]
    end

    subgraph "Google Cloud Platform"
        IAP["Identity-Aware Proxy (IAP)"]
        LB["Cloud Load Balancer"]
        PSC_ENDPOINT["PSC Endpoint"]
        APP["Aplicación Web<br/>(en GKE)"]
        
        subgraph "VPC de Confluent"
            KAFKA_SERVICE["Servicio Kafka"]
        end
    end

    subgraph "Planta On-Premise (GDC Edge)"
        KAFKA_CLIENT["Cliente Kafka<br/>(Cluster Linking)"]
    end

    USER -- 1. Petición --> IAP
    IAP -- 2. Auth & AuthZ --> LB
    LB -- 3. Proxy --> APP

    KAFKA_CLIENT -- "Tráfico mTLS sobre Interconnect" --> PSC_ENDPOINT
    PSC_ENDPOINT -- "Conexión Privada" --> KAFKA_SERVICE
```

---

## 5. Flujo de Trabajo GitOps

Este diagrama ilustra el flujo de CI/CD "Todo como Código", mostrando los dos puntos de validación de políticas con OPA.

```mermaid
graph TD
    A[Desarrollador] -- "1. git commit" --> B{Repositorio Git}
    B -- "2. Webhook" --> C[Pipeline CI/CD en Harness]
    
    subgraph C
        direction LR
        C1[Build & Test]
        C1 --> C2(<b>Gate 1: Harness OPA</b><br/>Validación Shift-Left)
    end

    C2 -- "Actualiza Manifiesto" --> B
    
    subgraph "Plataforma Kubernetes (GDC Edge + GCP)"
        D[Anthos Config Mgmt] -- "Sincroniza" --> E[API Server]
        G[<b>Gate 2: Anthos Policy Controller</b><br/>Validación en Runtime] -- "Valida" --> E
    end

    B -- "Fuente de Verdad" --> D
```

---

## 6. Arquitectura MLOps

Este diagrama muestra el ciclo de vida para el re-entrenamiento y despliegue automático de los modelos de IA para FinOps usando Vertex AI.

```mermaid
graph TD
    A[Cloud Scheduler] --> B(Cloud Function)
    B -- "Dispara Pipeline" --> C[Vertex AI Pipelines]
    
    subgraph C
        C1[Cargar Datos<br/>(desde BigQuery)] --> C2[Entrenar Modelo]
        C2 --> C3[Evaluar Modelo]
        C3 -- Si es bueno --> C4[Registrar en Model Registry]
    end

    C4 --> D[Desplegar en Endpoint]
```

---

## 7. Dashboard de FinOps (Conceptual)

Este diagrama conceptual muestra las fuentes de datos y los KPIs clave que se visualizarían en el dashboard de FinOps en Looker.

```mermaid
graph TD
    subgraph "Fuentes de Datos"
        A[BigQuery<br/>(Datos de Facturación GCP)]
        B[KubeCost<br/>(Costos por Pod/Namespace)]
        C[Hojas de Cálculo<br/>(Presupuestos, Metas)]
    end

    subgraph "Dashboard FinOps en Looker"
        D[KPIs Clave]
        D1["TCO (Cloud vs On-Prem)"]
        D2["ROI y Payback"]
        D3["Costo por Unidad Producida"]
        D4["Forecast vs. Real"]
        D5["Anomalías de Costo"]
        D6["Cumplimiento de Etiquetado"]
    end

    A --> D
    B --> D
    C --> D
```
