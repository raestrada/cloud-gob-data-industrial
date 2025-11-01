# Proyecto: Migración y Operación en Google Cloud con Gobierno FinOps e IA

---

## ⚠️ **IMPORTANTE: NATURALEZA DEL PROYECTO**

**🎯 ESTE ES UN EJERCICIO/DESAFÍO DE DISEÑO ARQUITECTÓNICO**

Este proyecto es un caso de estudio educativo para diseñar una solución completa de migración cloud industrial con gobierno FinOps e IA. Por lo tanto:

✅ **ESTÁ PERMITIDO Y NECESARIO usar SUPUESTOS**
- Los supuestos son necesarios para completar el diseño arquitectónico
- Deben ser **los mínimos indispensables** para resolver los entregables
- **OBLIGATORIO**: Marcar explícitamente como **[SUPUESTO]** en los documentos
- **OBLIGATORIO**: Justificar cada supuesto con razonamiento técnico/financiero

📋 **DISTINCIÓN CRÍTICA: Datos Reales vs Supuestos**
- **Datos Reales**: Provienen del PDF del caso de negocio en `docs/`
- **Supuestos**: Todo lo demás (costos estimados, throughput, latencias, etc.)
- **Formato requerido**:
  - `[DATO VALIDADO - Caso de Negocio pág. X]` para datos reales
  - `[SUPUESTO - justificación]` para estimaciones

🎯 **OBJETIVO DEL EJERCICIO**
- Completar los 5 entregables finales (PDFs) con rigor técnico
- Demostrar capacidad de diseño arquitectónico distribuido
- Aplicar mejores prácticas de FinOps, MLOps, GitOps, DevSecOps
- Ser **transparente** sobre qué es dato vs estimación

---

## Descripción del Proyecto

Caso de negocio para liderar la migración y operación de infraestructura industrial crítica hacia Google Cloud Platform (GCP) en un plazo de 12-18 meses, con un enfoque en resiliencia, RPO/RTO cercano a cero, arquitectura basada en eventos, y gobierno FinOps.

## Contexto del Negocio

### Alcance
- **Timeline**: 12-18 meses
- **Plantas**: Monterrey, Guadalajara, Tijuana + Corporativo
- **Cargas**: 420 VMs (~1,900 vCPU, ~12.8TB RAM)
- **Almacenamiento**: ~200TB block + ~500TB object (crecimiento 20% anual)
- **Producción anual**: 1,560,000 unidades
- **TCO on-prem (3 años)**: USD 15,735,000
- **OPEX on-prem anual**: USD 5,245,000

### Sistemas Críticos (RPO/RTO = 0)
- **SCADA antiguos**: 40 instancias (latencia ultra-baja requerida)
- **SQL Server 2019**: 120 instancias críticas (plantas + corporativo)

### Restricciones Técnicas
- Interconnect 1Gbps ya operativo (Monterrey ↔ GCP)
- Cloud VPN como respaldo
- Ventanas de mantenimiento: Domingos 2h por planta
- Freeze anual: 15-Nov al 5-Ene
- SLA objetivo: 99.95% global; 99.99% en críticos
- Procedimientos almacenados que invocan .exe locales

## Arquitectura Propuesta

### Principios Arquitectónicos

1. **Edge-First Architecture**: Procesamiento local máximo en planta (offline-capable), cloud para agregación multi-planta
2. **Event-Driven Architecture (EDA)**: Todo debe escribirse como eventos
3. **RPO/RTO ≈ 0 Local**: Resiliencia en edge, replicación asíncrona priorizada a cloud
4. **Stack Nativo GCP**: Google Distributed Cloud Edge (on-prem) + GKE (cloud) unificado
5. **Data Hub Distribuido**: Kafka Confluent con topología arbitraria via Cluster Linking
6. **Replicación Inteligente**: Priorización por criticidad (alarmas → alta, batch → media, logs → baja)
7. **Zero-Trust Nativo**: IAP + Identity Platform federado, sin IPs públicas (PSC + mTLS)
8. **Everything as Code**: GitOps con Anthos Config Management para toda la infraestructura

### Stack Tecnológico Principal

#### Plataforma de Eventos
- **Confluent Kafka** (managed service)
  - Cluster Linking para replicación multi-región sub-segundo
  - Kafka Connect con Debezium para CDC (Change Data Capture)
  - KSQL para stream processing
  - Tiered Storage para optimización de costos
  - Razón: No usar MirrorMaker 2 debido a RPO/RTO=0 requerido
  - Razón: No usar Pub/Sub o Spanner (menor latencia, exactly-once, mejor integración legados)

#### Orquestación y Compute
- **Google Distributed Cloud Edge (GDC Edge)**:
  - GKE Edge en plantas (on-premise, offline-capable)
  - Anthos para gestión unificada edge + cloud
  - Procesamiento local completo sin dependencia de conectividad
  - Sincronización asíncrona priorizada hacia GCP
- **GKE (Google Kubernetes Engine)**: Cloud workloads para analítica multi-planta
- **Dataproc on GKE (edge + cloud)**:
  - Spark/Flink managed desplegable en GKE cloud y GKE Edge
  - Procesamiento de ventanas temporales, batch, streaming
  - Optimización automática de recursos Dataproc + Cast.ai
  - Despliegue homogéneo edge ↔ cloud con misma API
  - Razón: Dataproc managed vs Spark standalone (menor operación, auto-scaling)
  - Razón: Cast.ai optimiza dinámicamente los workers K8s de Dataproc (~40% ahorro)
- **Cast.ai**: Optimización dinámica predictiva de recursos K8s (GKE + Dataproc)
- **Anthos Service Mesh**: mTLS, observabilidad, traffic management edge ↔ cloud
- Razón: GDC Edge permite resiliencia industrial real (operación local sin cloud)
- Razón: Stack 100% GCP nativo simplifica FinOps y operación
- Razón: Dataproc on GKE permite procesamiento edge + cloud unificado

#### Networking y Seguridad
- **Private Service Connect (PSC)**:
  - Conectividad privada edge ↔ cloud sin IPs públicas
  - Sin overlap de redes IP entre plantas y cloud
  - Comunicación segura via endpoints privados
- **Anthos Service Mesh**:
  - mTLS automático para todo el tráfico (edge ↔ cloud)
  - Control de tráfico L7 nativo (Traffic Director)
  - Observabilidad distribuida end-to-end
  - Políticas de seguridad granulares
- **Identity-Aware Proxy (IAP)**:
  - Zero-Trust para accesos humanos
  - Sin VPN tradicional
  - Federación con Identity Platform (SAML/OIDC)
  - Integración con AD corporativo/SSO
- **Interconnect 1Gbps**: Conectividad privada física Monterrey ↔ GCP
- **Cloud VPN HA**: Respaldo redundante para Interconnect
- **GCP Shared VPC**: Hub-and-spoke para organización multi-proyecto
- **VPC Service Controls**: Perímetros de seguridad para datos sensibles
- **Secret Manager + KMS/CMEK**: Secretos y encriptación en tránsito/reposo
- **Razón**: Stack 100% GCP nativo, sin dependencia multiproveedor
- **Razón**: Menor costo operativo, FinOps unificado, mismo proveedor

#### GitOps y CI/CD
- **Anthos Config Management**:
  - GitOps unificado para GDC Edge + GKE cloud
  - Policy Controller (OPA integrado)
  - Config Sync para despliegues declarativos
  - Gestión centralizada multi-cluster (edge + cloud)
- **Harness**:
  - Control de despliegues y CI/CD avanzado
  - Backstage como Internal Developer Portal (IDP)
  - Blue/Green y Canary deployments
  - Chaos Engineering para validación RPO/RTO
  - Métricas DORA y SPACE
  - FinOps predictivo integrado
- **Policy Controller (OPA nativo Anthos)**: Gobierno y compliance unificado
- **Terraform**: Automatización de infraestructura GCP
- **Razón**: Anthos unifica GitOps edge + cloud, elimina complejidad multi-plataforma

#### Data Platform
- **Arquitectura Medallion (extendida)**:
  - Tópico RAW: Captura inicial via Kafka Connect (edge + cloud)
  - Procesamiento edge: KSQL (transformaciones ligeras, filtrado, priorización)
  - Procesamiento cloud: Dataproc on GKE (agregaciones multi-planta, analítica compleja)
  - Capas adicionales: Anonimización, limpieza, deduplicación, agregaciones
  - Protección de BD transaccionales: Lectura una vez, consumo múltiple
- **Google Cloud Storage**: Persistencia final (hot/cold/archive tiers)
- **BigQuery**: MPP para analytics multi-planta
- **Looker**: Visualización y dashboards
- **Kafka Tiered Storage**: Reducción de costos almacenamiento histórico
- **Razón**: KSQL edge (ligero) + Dataproc cloud (pesado) = procesamiento distribuido inteligente

#### MLOps y AI
- **Vertex.ai**: MLOps nativo GCP (edge + cloud)
- **Vertex AI Workbench**: Entorno unificado desarrollo edge ↔ cloud
- **Cast.ai LLM/Data Cache**: Reducción costos transferencia y LLM
- **LangFuse + LangChain**: FinOps para LLM
- **Principio**: Todo alimentado por eventos, modelos desplegables en edge para inferencia local

#### Observabilidad
- **Cloud Operations Suite (anteriormente Stackdriver)**:
  - Cloud Monitoring: Métricas edge + cloud unificadas
  - Cloud Logging: Logs centralizados desde GDC Edge
  - Cloud Trace: Tracing distribuido via Anthos Service Mesh
  - Cloud Profiler: Performance profiling
- **Anthos Service Mesh Observability**: Tráfico L7, latencias, errores edge ↔ cloud
- **OpenTelemetry**: Instrumentación estándar para aplicaciones
- **Razón**: Stack 100% GCP nativo simplifica FinOps y operación vs multiproveedor

### Capas de Datos (Data Hub)

```
┌─────────────────── EDGE (GKE Edge + Kafka) ────────────────────┐
│                                                                 │
│  Fuentes Legadas → Kafka Connect/Debezium → Tópico RAW (edge)  │
│                                              ↓                  │
│                                    Procesamiento KSQL           │
│                                    (filtrado, priorización)     │
│                                              ↓                  │
└──────────────────────────────────────────────┼──────────────────┘
                                              ↓
                          [Cluster Linking - Solo datos críticos/agregados]
                                              ↓
┌─────────────────── CLOUD (GKE + Kafka) ────────────────────────┐
│                                                                 │
│                                    Tópico RAW (cloud)           │
│                                              ↓                  │
│                              Procesamiento Dataproc on GKE     │
│                              (agregaciones multi-planta)       │
│                                              ↓                  │
│         ┌────────────────────────────────────┼─────────────────┐│
│         ↓                      ↓                      ↓         ││
│   Anonimización           Limpieza            Deduplicación    ││
│         ↓                      ↓                      ↓         ││
│   Agregaciones          Enriquecimiento       Validación       ││
│         └────────────────────────────────────┼─────────────────┘│
│                                              ↓                  │
│                                    Tópicos Procesados           │
│                                              ↓                  │
│                                    Google Cloud Storage         │
│                                    (hot/cold/archive)           │
│                                              ↓                  │
│                                ┌─────────────┴──────────────┐  │
│                                ↓                            ↓  │
│                            BigQuery                    Lakehouse│
│                                ↓                            ↓  │
│                            Looker                      Vertex.ai│
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Ventajas Clave de la Arquitectura

1. **Resiliencia Industrial Real**: GDC Edge permite operación local sin dependencia de cloud
2. **RPO/RTO ≈ 0 Local**: Procesamiento edge completo, replicación asíncrona priorizada
3. **Stack 100% GCP Nativo**: Menor costo operativo, FinOps unificado, un solo proveedor
4. **Zero-Trust Nativo**: IAP + mTLS sin multiproveedor
5. **Replicación Inteligente**: Priorización por criticidad (alarmas → alta, batch → baja)
6. **Datos Sensibles On-Prem**: Solo agregados suben a cloud, cumplimiento y privacidad
7. **Recuperación avanzada Kafka**: Offset replay, exactly-once semantics
8. **Orden garantizado**: Kafka mantiene orden en particiones (crítico para señales industriales)
9. **Topología arbitraria**: Cluster Linking permite cualquier topología multi-región edge ↔ cloud
10. **Sin Overlap IPs**: Private Service Connect + mTLS elimina conflictos de red
11. **Gestión Unificada**: Anthos Config Management para edge + cloud desde un solo control plane
12. **Procesamiento Distribuido Inteligente**: KSQL edge (ligero) + Dataproc on GKE cloud (pesado)
13. **Costos Optimizados**: Cast.ai optimiza GKE + Dataproc workers, Kafka Tiered Storage, políticas OPA

## Razones para Decisiones Arquitectónicas

### ¿Por qué Confluent Kafka y no alternativas nativas de GCP?

1. **Pub/Sub**:
   - Mayor latencia que Cluster Linking
   - No garantiza exactly-once
   - Menor integración con BD legadas

2. **Spanner**:
   - No es plataforma de eventos
   - Mayor complejidad para streaming
   - Costos más altos

3. **Confluent Kafka**:
   - Latencia sub-segundo (Cluster Linking)
   - Exactly-once semantics
   - Kafka Connect + Debezium para sistemas legados (SCADA, SQL Server)
   - Arquitectura edge ↔ cloud: On-premise (Confluent en GDC Edge) = Cloud (Confluent managed GKE)
   - Partner de GCP: Facturación en cuenta GCP via Marketplace
   - Desplegable en GKE Edge y GKE cloud con misma API

### ¿Por qué no MirrorMaker 2?

- RPO/RTO=0 requiere latencias sub-segundo
- Cluster Linking ofrece mejor rendimiento y simplicidad operacional

### ¿Por qué no ETL tradicional o multi-región estándar?

- Implementación simple basada en eventos
- Carga operativa manejada por Confluent + GCP
- No requiere programación custom de resiliencia/recuperación

### ¿Por qué Google Distributed Cloud Edge + Stack 100% GCP Nativo?

**Decisión arquitectónica**: GDC Edge (on-premise) + GKE (cloud) + Anthos unificado

**Razones clave**:

1. **Resiliencia Industrial Real (Offline-Capable)**:
   - GDC Edge permite operación local **sin dependencia de cloud**
   - Plantas pueden continuar operando durante cortes de conectividad
   - RPO/RTO ≈ 0 local, procesamiento crítico no depende de latencia cloud
   - Ideal para entornos industriales con requisitos de disponibilidad extremos

2. **Stack 100% GCP Nativo (Un Solo Proveedor)**:
   - Google Distributed Cloud Edge + GKE + Anthos (ecosistema unificado)
   - Menor complejidad operativa: un solo vendor, un solo contrato
   - FinOps unificado: todo facturado en cuenta GCP Marketplace
   - Menor brecha de skills: mismo stack edge + cloud (Kubernetes/Anthos)

3. **Zero-Trust Nativo (IAP + Identity Platform)**:
   - Identity-Aware Proxy para accesos humanos sin VPN tradicional
   - Federación SAML/OIDC con AD corporativo/SSO nativa
   - Anthos Service Mesh con mTLS automático para todo el tráfico
   - Sin necesidad de soluciones de terceros (menor costo, menor complejidad)

4. **Conectividad Privada (PSC + Interconnect)**:
   - Private Service Connect (PSC) para conectividad edge ↔ cloud privada
   - Sin overlaps de IPs entre plantas y cloud
   - Sin exponer IPs públicas, comunicación 100% privada
   - Interconnect 1Gbps + Cloud VPN HA como respaldo redundante

5. **Procesamiento Edge-First Estratégico**:
   - Procesar **localmente lo máximo posible y razonable** en planta
   - Pre-procesamiento, filtrado, priorización en edge (KSQL)
   - Reducir volumen de datos hacia cloud (solo críticos/agregados)
   - Cloud para métricas multi-planta, analítica global, ML/AI
   - Datos sensibles permanecen on-prem (cumplimiento, privacidad)

6. **Replicación Asíncrona Priorizada**:
   - **Alta prioridad**: Alarmas/telemetría (Pub/Sub Lite → Pub/Sub)
   - **Media prioridad**: Batch/analítica (Dataflow programado)
   - **Baja prioridad**: Logs/históricos (Storage Transfer nocturno)
   - Optimiza uso de Interconnect 1Gbps con tráfico inteligente

7. **Gestión Unificada (Anthos Config Management)**:
   - GitOps único para GDC Edge + GKE cloud
   - Anthos Config Management: despliegues declarativos centralizados
   - Policy Controller (OPA integrado): gobierno unificado
   - Un solo control plane para toda la infraestructura

8. **Costos Optimizados y Predecibles**:
   - Sin licencias de terceros (todo incluido en GCP)
   - Facturación consolidada GCP Marketplace (Confluent, Dataproc)
   - Cast.ai optimiza dinámicamente GKE + Dataproc (~40% ahorro)
   - Modelo OPEX predictible, sin sorpresas de múltiples vendors

9. **Observabilidad Nativa Unificada**:
   - Cloud Operations Suite: métricas, logs, traces edge + cloud
   - Anthos Service Mesh observability: latencias L7 automáticas
   - OpenTelemetry: instrumentación estándar
   - Visibilidad end-to-end sin herramientas dispersas

**Trade-offs aceptados**:
- Dependencia de un solo proveedor (GCP) vs estrategia multi-cloud
- Requiere Interconnect funcional (✅ ya operativo según caso de negocio pág. 4)
- Menor flexibilidad para futuro multi-cloud (mitigado: Kubernetes/Anthos portabilidad)

### ¿Por qué Harness?

- Internal Developer Portal (Backstage)
- Control completo del ciclo de vida
- Blue/Green y Canary nativo
- Chaos Engineering para RPO/RTO
- Métricas DORA y SPACE
- FinOps predictivo integrado
- OPA para políticas

### ¿Por qué Cast.ai?

- Reducción hasta 40% en costos de compute (GKE + GDC Edge)
- Gestión dinámica predictiva inteligente de recursos K8s
- Optimización automática de nodos, right-sizing pods
- Compatible con GKE cloud y GKE Edge (mismo runtime Kubernetes)
- LLM/Data caching para reducir latencia y costos transferencia
- Alternativa vs autoscaling nativo GKE (más agresivo en ahorro)

### ¿Por qué Dataproc on GKE vs Databricks?

**Decisión**: Usar **Dataproc on GKE** (edge + cloud) en lugar de Databricks

**Razones clave**:

1. **Despliegue Edge + Cloud Unificado**:
   - Dataproc on GKE funciona tanto en GKE cloud como en GKE Edge (on-premise)
   - Databricks no soporta despliegue on-premise nativo en GKE Edge
   - Arquitectura homogénea: mismo stack Spark en plantas y cloud

2. **Optimización Cast.ai**:
   - Dataproc on GKE permite que Cast.ai optimice dinámicamente los workers K8s (~40% ahorro)
   - Databricks tiene autoscaling propio, pero sin integración Cast.ai
   - Gestión unificada de recursos K8s (GKE + Dataproc) en un solo plano

3. **FinOps Unificado**:
   - Dataproc facturado en cuenta GCP Marketplace (consolidado)
   - Databricks requiere contrato/facturación separada (multiproveedor)
   - Menor complejidad TCO: todo en una factura GCP

4. **Costos Menores**:
   - Dataproc on GKE: Pago por uso Spark managed + compute GKE
   - Databricks: Premium sobre Spark + markup significativo (~2-3× sobre Dataproc)
   - Para workloads batch/streaming estándar, Dataproc suficiente

5. **Gestión Anthos Unificada**:
   - Dataproc on GKE gestionado via Anthos Config Management
   - GitOps unificado para toda la plataforma (edge + cloud)
   - Databricks requiere plane de control separado

**Trade-off aceptado**:
- Databricks tiene mejor UX para Data Scientists (notebooks colaborativos, Delta Lake optimizado)
- Mitigación: Vertex AI Workbench + BigQuery para analítica colaborativa
- Para procesamiento streaming/batch industrial, Dataproc on GKE suficiente

**Cuándo considerar Databricks** (futuro):
- Si se requiere Delta Lake con optimizaciones avanzadas (ZORDER, OPTIMIZE, etc.)
- Si equipos de DS necesitan notebooks colaborativos avanzados (no cubierto por Vertex AI Workbench)
- Si se migra a ML/AI intensivo que justifique el costo premium

## Modelo de Gobierno

### Políticas OPA

1. **Presupuestos y Cuotas** (definir desde día 1):
   - VMs, disco, memoria
   - Logs, métricas
   - LLM tokens/llamadas
   - Egreso de red

2. **Aprobaciones explícitas**: Equipos deben pedir exceder cuotas

3. **Validación pre-despliegue**: OPA valida recursos antes de cualquier deploy

4. **Gobernanza Harness**: Control centralizado de políticas

### Estándares de Eventos

**Principio fundamental**: TODO se debe escribir como eventos en tópicos RAW

1. **Definir estándar de evento** desde el inicio
2. **No pensar si se compartirá**: Escribir todo
3. **Responsabilidad del consumidor**: Filtrar y transformar según necesidad
4. **Habilita arquitectura evolutiva**: Migración gradual sin romper flujos
5. **Change Data Capture**: Convertir legados a eventos para mantener o migrar sin impacto

### FinOps

#### KPIs Objetivo
- Forecast accuracy ≥ 90% mensual
- Cobertura CUD/RI ≥ 60% a 12 meses
- Right-sizing ratio ≥ 20% primeros 90 días
- Idle/Orphan rate < 3%
- Label compliance ≥ 95%
- Variance vs presupuesto ≤ ±5%
- Costo unitario: USD/unidad producida

#### MVP IA para FinOps
- **Forecast**: Descomposición estacional/regresión por proyecto/BU/onda
- **Anomalías**: Reglas + umbrales dinámicos (±2σ o +8% sobre forecast)
- **NLP Etiquetado**: Inferir owner/cost_center/criticality en gastos huérfanos

#### Facturación Consolidada GCP
- Confluent: Via GCP Marketplace (orden de compra)
- Grafana: Via GCP Marketplace (orden de compra)
- Conversación con Account Managers de GCP
- Soluciona "problema" de tecnologías fuera de GCP

## Estructura de Equipos

### Roles Especializados

1. **Arquitecto de Plataforma**: Diseño arquitectura distribuida, Kafka Confluent, Anthos, GDC Edge, Dataproc on GKE
2. **Arquitecto de Datos**: Data hub, capas medallion, lakehouse, BigQuery, edge ↔ cloud sync, Dataproc
3. **Administradores Sistemas Legados/On-Premise**: Integración SCADA, SQL Server, GDC Edge deployment
4. **Experto en Redes**: Private Service Connect, Interconnect, VPN HA, Anthos Service Mesh
5. **DevSecOps**: GitOps con Anthos Config Management, Harness, Policy Controller, IAP
6. **Data Engineer**: Pipelines KSQL edge, Dataproc on GKE cloud, Kafka Connect, Debezium, priorización
7. **Data Scientist**: MLOps, Vertex.ai, FinOps LLM, modelos forecast/anomalías, Dataproc notebooks
8. **Finanzas**: TCO, CAPEX/OPEX, CUD/RI, unit economics, sensibilidades, FinOps unificado GCP

### Metodología de Trabajo

1. **Colaboración en ciclos**: Cada tarea requiere discusión y retroalimentación del equipo
2. **Validación cruzada**: Un rol revisa y cuestiona decisiones de otros
3. **Decisiones consensuadas**: Trade-offs se discuten entre todos los roles
4. **Presentación al CEO**: Equipo completo participa

## Entregables del Proyecto

### 1. Memo Ejecutivo (2-3 págs)
- Decisión recomendada (regiones, patrón DR, edge OT)
- Decisiones C-level requeridas
- CAPEX/OPEX por ondas y payback
- Sensibilidades (±10-20%)
- Riesgos top-5 y trade-offs

### 2. Caso de Negocio (10-15 págs)
- Principios de arquitectura
- Modelo financiero 3 años
- FinOps y gobierno de costos
- Modelo operativo y liderazgo (RACI)
- Gestión del cambio

### 3. MVP de IA para FinOps
- Forecast de costos
- Detección de anomalías
- NLP de etiquetado
- Dataset provisto en caso de negocio

### 4. Plan Maestro (Gantt, 12-18 meses)
- Fases, hitos Go/No-Go
- Rollback procedures
- Dependencias con ventanas y freeze

### 5. Deck Ejecutivo (5-8 slides)
- Para CIO/CTO/CFO/CEO
- Situación, propuesta, roadmap, TCO/ROI
- Riesgos y próximos pasos

### 6. Diagramas Mermaid
- Arquitectura de alto nivel
- Flujo de datos (data hub)
- Topología de red
- GitOps workflow
- FinOps governance

## Fases del Proyecto (Plantilla Gantt)

| ID | Fase | Inicio | Fin | Duración | Dependencias | Hito |
|----|------|--------|-----|----------|--------------|------|
| 1 | Movilización & CCoE | 2025-11-24 | 2026-01-31 | 69 días | — | Charter aprobado |
| 2 | Conectividad & Seguridad | 2025-12-02 | 2026-02-28 | 89 días | 1 | SEG listo |
| 3 | Datos – OLA/CDC | 2026-01-05 | 2026-04-30 | 116 días | 1-2 | DQ ≥ 98% |
| 4 | Piloto (10-15 apps) | 2026-02-10 | 2026-05-31 | 111 días | 1-3 | Piloto OK |
| 5 | Onda 1 (≈30%) | 2026-04-15 | 2026-08-31 | 139 días | 4 | Go-Live O1 |
| 6 | Onda 2 (≈60%) | 2026-07-01 | 2026-12-20 | 173 días | 5 | Go-Live O2 |
| 7 | Críticos (≈10%) | 2026-10-01 | 2027-02-28 | 151 días | 6 | Go-Live críticos |
| 8 | Cierre & Optimización | 2027-01-05 | 2027-03-31 | 85 días | 7 | BAU |

## Escenarios de Liderazgo

### Escenario 1: Sobre-ejecución Q2 (+15% vs presupuesto)
- Ajuste CUD/RI
- Right-sizing
- Lifecycle storage
- Apagar entornos no-prod
- Re-faseo de ondas
- Comunicación CFO/BU

### Escenario 2: Degradación OT por latencia
- Activar operación local-first (edge)
- Protocolo de roll-back
- Coordinación con Operaciones
- Plan de remediación

### Escenario 3: Cambio de prioridades del negocio
- Adelantar Analytics/IoT
- No romper RPO/RTO de críticos
- Mantener variance ≤ ±5%
- Explicar decisiones y trade-offs

## Matriz de Riesgos (Mínimo 12)

1. Latencia OT/SCADA (mitigado con GDC Edge local-first)
2. Viabilidad RPO/RTO=0 inter-región edge ↔ cloud
3. .exe locales en procedimientos almacenados
4. Brecha de skills GCP/Anthos/FinOps
5. Ventanas de planta/freeze
6. Etiquetado/Reserved Instances/CUD
7. Seguridad/compliance
8. Licenciamiento GCP Distributed Cloud Edge
9. Cortes de energía en Monterrey (mitigado con operación offline-capable)
10. Dependencias ocultas
11. Shadow-IT
12. Dependencia de un solo proveedor (GCP) vs multi-cloud
13. Adopción Anthos Config Management por equipos on-prem
14. Interconnect como punto único de falla (mitigado con VPN HA)

## Supuestos Clave

1. **GDC Edge disponibilidad**: Google Distributed Cloud Edge está disponible en México/plantas (validar con GCP Account Team)
2. **Confluent en GKE Edge**: Confluent Kafka desplegable en GKE Edge con mismo desempeño que GKE cloud
3. **Dataproc on GKE Edge**: Dataproc soporta despliegue en GKE Edge para procesamiento local (validar con GCP)
4. **Facturación GCP consolidada**: Confluent + Dataproc facturados via GCP Marketplace (confirmado partner GCP)
5. **Skills internos**: Se requiere upskilling significativo en Anthos, Kafka, Dataproc, Kubernetes, FinOps
6. **Conectores propietarios**: Proveedores de SCADA pueden tener conectores para enviar CDC a Kafka (investigar)
7. **Dataproc Personal Cluster**: Viabilidad de replicar arquitectura Dataproc en laptops para dev/test local
8. **Cast.ai savings**: 40% de reducción es alcanzable según benchmarks (aplicable a GKE + Dataproc workers)
9. **Policy Controller enforcement**: Todas las políticas OPA pueden ser enforzadas pre-despliegue via Anthos
10. **Interconnect capacidad**: 1Gbps suficiente para workloads edge → cloud priorizados, requiere monitoreo
11. **Change Data Capture**: Todos los sistemas legacy soportan CDC via Kafka Connect/Debezium
12. **Operación offline edge**: GDC Edge + Dataproc pueden operar 100% offline sin conectividad cloud durante cortes
13. **PSC latencia**: Private Service Connect no añade latencia significativa vs Interconnect directo (<1ms overhead)
14. **Anthos licensing**: Costos de licenciamiento Anthos para edge + cloud son viables vs VMware/Cloudflare eliminados
15. **Dataproc vs Databricks**: Para workloads batch/streaming estándar industriales, Dataproc on GKE suficiente (no requiere Databricks premium)

## Tecnologías Complementarias

### Entorno de Desarrollo Local
- **Redpanda**: Kafka-compatible ligero para laptops (simula Confluent local)
- **Dataproc Personal Cluster**: Cluster Dataproc mínimo para desarrollo/testing local
- **Kind (Kubernetes in Docker)**: Simula GKE Edge/cloud localmente
- **Skaffold**: Desarrollo local con hot-reload para GKE + Dataproc
- **Config Sync (local mode)**: Prueba GitOps Anthos localmente
- **Docker Compose**: Orquestación básica para pruebas rápidas (Kafka + Spark standalone mínimo)
- **Razón**: Dataproc Personal Cluster permite probar jobs Spark localmente con API idéntica a producción

### Conectores Kafka
- **Debezium**: CDC para SQL Server, PostgreSQL, MySQL, MongoDB, etc.
- **JDBC Source/Sink**: Conectividad BD genérica
- **Investigar**: Conectores propietarios SCADA (OPC-UA, Modbus, etc.)

## Nomenclatura de Entrega

- `Memo_Ejecutivo_LiderCloudFinOps_<Apellido>.pdf`
- `Caso_Negocio_LiderCloudFinOps_<Apellido>.pdf`
- `MVP_IA_FinOps_<Apellido>.pdf`
- `Plan_Gantt_<Apellido>.xlsx` o `.md`
- `Deck_Ejecutivo_<Apellido>.pdf`

## Referencias Técnicas

### Precios Base GCP (Price Pack)
- Compute on-demand: USD 24/vCPU-mes, USD 3/GB-RAM-mes
- SQL administrado: 1.6× costo compute equivalente
- Block storage: 0.12/GB-mes
- Object Standard: 0.023/GB-mes
- Snapshots: 0.05/GB-mes
- Interconnect: USD 3,000/mes (2 puertos)
- Egress Internet: 0.05/GB (primeros 30 TB/mes)
- Soporte GCP: USD 12,500/mes
- Operación Cloud (equipo base): USD 75,000/mes
- One-time: USD 1,700,000

### Inventario de Cargas
| Categoría | Monterrey | Guadalajara | Tijuana | Total |
|-----------|-----------|-------------|---------|-------|
| SCADA modernos | 10 | 10 | 10 | 30 |
| SCADA antiguos (críticos) | 10 | 10 | 20 | 40 |
| SQL Server 2008-2012 (Plantas) | 10 | 10 | 20 | 40 |
| SQL Server 2019 (Plantas, críticos) | 10 | 10 | 20 | 40 |
| SQL Server 2008-2012 (Corp.) | 20 | 20 | 20 | 60 |
| SQL Server 2019 (Corp., críticos) | 20 | 20 | 40 | 80 |
| Aplicaciones IIS (Plantas) | 20 | 20 | 20 | 60 |
| Aplicaciones IIS (Corp.) | 30 | 0 | 0 | 30 |
| **Total** | **130** | **100** | **150** | **380** |

### Producción por Planta
| Planta | Producción mensual | Producción anual |
|--------|-------------------|------------------|
| Monterrey | 60,000 unid. | 720,000 unid. |
| Guadalajara | 40,000 unid. | 480,000 unid. |
| Tijuana | 30,000 unid. | 360,000 unid. |
| **Total** | **130,000 unid.** | **1,560,000 unid.** |

## Próximos Pasos

1. **Kickoff con sub-agentes**: Cada rol especializado analiza el caso desde su perspectiva
2. **Sesiones de diseño colaborativo**: Discusión y retroalimentación cruzada
3. **Generación de artefactos**: Documentación, diagramas Mermaid, modelos financieros
4. **Revisión y refinamiento**: Iteración basada en feedback del equipo
5. **Consolidación final**: Generación de PDFs para entrega

---

**Versión**: 1.0
**Fecha**: 2025-10-31
**Autor**: Equipo de Arquitectura Cloud & FinOps
