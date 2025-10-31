# Proyecto: Migración y Operación en Google Cloud con Gobierno FinOps e IA

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

1. **Event-Driven Architecture (EDA)**: Todo debe escribirse como eventos
2. **RPO/RTO ≈ 0**: Usando Kafka Cluster Linking con latencia sub-segundo
3. **Arquitectura Simétrica**: Mismo stack on-premise (VMware Tanzu) y cloud (GKE)
4. **Data Hub Distribuido**: Kafka con topología arbitraria via Cluster Linking
5. **Arquitectura Evolutiva**: Migración gradual basada en eventos
6. **Everything as Code**: GitOps para toda la infraestructura y aplicaciones

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
- **GKE (Google Kubernetes Engine)**: Cloud workloads
- **VMware Tanzu**: On-premise workloads (administrado por Confluent + VMware)
- **Cast.ai**: Optimización dinámica predictiva de recursos (reducción ~40% costos)
- **Spark Structured Streaming**: Procesamiento de ventanas temporales
- Razón: Reemplazar Dataproc por GKE + Tanzu para homogeneidad
- Razón: No usar Databricks por costos vs eficiencia

#### Networking y Seguridad
- **Cloudflare Zero Trust**:
  - Cloudflare Access y Zero Trust Network Access
  - Cloudflare One Private Networks
  - Backbone global anycast privado
  - No usar Layer 3 tradicional entre nubes
  - Cada despliegue con red IP independiente (10.0.0.0/24)
  - OAuth/mTLS para autenticación
  - WARP VPN para usuarios/proveedores/clientes
  - Interconnect + VPN solo como habilitador para Cloudflare Layer 3
- **GCP Shared VPC**: Hub-and-spoke
- **VPC Service Controls**: Datos sensibles
- **Secret Manager + KMS/CMEK**: Secretos y encriptación

#### GitOps y CI/CD
- **Harness**:
  - Control de despliegues y CI
  - Backstage como Internal Developer Portal (IDP)
  - Blue/Green y Canary deployments
  - Chaos Engineering para validación RPO/RTO
  - Métricas DORA y SPACE
  - FinOps predictivo (cloud + on-premise)
- **OPA (Open Policy Agent)**: Gobierno y compliance
- **Tanzu Control Plane**: On-premise GitOps
- **GKE Control Plane**: Cloud GitOps
- **Terraform**: Automatización Cloudflare

#### Data Platform
- **Arquitectura Medallion (extendida)**:
  - Tópico RAW: Captura inicial via Kafka Connect
  - Capas adicionales: Anonimización, limpieza, deduplicación, agregaciones
  - Protección de BD transaccionales: Lectura una vez, consumo múltiple
- **Google Cloud Storage**: Persistencia final (hot/cold/archive tiers)
- **BigQuery**: MPP para analytics
- **Looker**: Visualización
- **Kafka Tiered Storage**: Reducción de costos

#### MLOps y AI
- **Vertex.ai**: MLOps nativo GCP (con versión OSS para Tanzu)
- **Cast.ai LLM/Data Cache**: Reducción costos transferencia y LLM
- **LangFuse + LangChain**: FinOps para LLM
- **Principio**: Todo alimentado por eventos (incluso en MVP)

#### Observabilidad
- **Grafana Cloud** (preferido): Observabilidad completa con OpenTelemetry
- **GCP Observability Suite**: Alternativa para no divergir de TCO
- Evaluación: Grafana vs GCP (Grafana es partner GCP)

### Capas de Datos (Data Hub)

```
Fuentes Legadas → Kafka Connect/Debezium → Tópico RAW
                                              ↓
                                    Procesamiento KSQL/Spark
                                              ↓
                    ┌─────────────────────────┼─────────────────────────┐
                    ↓                         ↓                         ↓
              Anonimización              Limpieza                 Deduplicación
                    ↓                         ↓                         ↓
              Agregaciones              Enriquecimiento          Validación
                    └─────────────────────────┼─────────────────────────┘
                                              ↓
                                    Tópicos Procesados
                                              ↓
                                    Google Cloud Storage
                                    (hot/cold/archive)
                                              ↓
                                ┌─────────────┴─────────────┐
                                ↓                           ↓
                            BigQuery                    Lakehouse
                                ↓                           ↓
                            Looker                      Vertex.ai
```

### Ventajas Clave de la Arquitectura

1. **RPO/RTO ≈ 0**: Cluster Linking con latencia sub-segundo
2. **Recuperación avanzada**: Via offset y replay de historia
3. **Orden garantizado**: Kafka mantiene orden en particiones (crítico para señales industriales)
4. **Protección de fuentes**: Lectura única, consumo múltiple sin impacto
5. **Eliminación de ETL Spaghetti**: Arquitectura basada en eventos
6. **Topología arbitraria**: Cluster Linking permite cualquier topología multi-región
7. **Arquitectura simétrica**: Mismo stack on-premise y cloud
8. **Desarrollo local**: Redpanda + Spark standalone para desarrollo/pruebas
9. **Conectividad inteligente**: Cloudflare optimiza tráfico con IA
10. **Costos optimizados**: Cast.ai, Tiered Storage, políticas OPA

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
   - Arquitectura simétrica: On-premise (Confluent + VMware) = Cloud (Confluent managed)
   - Partner de GCP: Facturación en cuenta GCP via Marketplace

### ¿Por qué no MirrorMaker 2?

- RPO/RTO=0 requiere latencias sub-segundo
- Cluster Linking ofrece mejor rendimiento y simplicidad operacional

### ¿Por qué no ETL tradicional o multi-región estándar?

- Implementación simple basada en eventos
- Carga operativa manejada por Confluent, VMware, GCP
- No requiere programación custom de resiliencia/recuperación

### ¿Por qué Cloudflare Zero Trust?

- Backbone global anycast privado
- No exponer IPs privadas/públicas reales
- Cada despliegue con red independiente
- Gestión centralizada con AD/SSO federado
- WARP VPN sin degradación de Internet
- Optimización de tráfico con IA
- Interconnect/VPN solo como habilitador Layer 3

### ¿Por qué Harness?

- Internal Developer Portal (Backstage)
- Control completo del ciclo de vida
- Blue/Green y Canary nativo
- Chaos Engineering para RPO/RTO
- Métricas DORA y SPACE
- FinOps predictivo integrado
- OPA para políticas

### ¿Por qué Cast.ai?

- Reducción hasta 40% en costos de hardware
- Gestión dinámica predictiva inteligente
- Mejor que PaaS/SaaS tradicional
- Despliegue homogéneo GKE/Tanzu
- LLM/Data caching

### ¿Por qué no Databricks?

- Costos más altos
- Mayor eficiencia pero más administración
- Arquitectura actual suficiente para necesidades

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

1. **Arquitecto de Plataforma**: Diseño arquitectura distribuida, Kafka Confluent, topología
2. **Arquitecto de Datos**: Data hub, capas medallion, lakehouse, BigQuery
3. **Administradores Sistemas Legados/On-Premise**: Integración SCADA, SQL Server, VMware Tanzu
4. **Experto en Redes**: Cloudflare Zero Trust, Interconnect, VPN, segmentación
5. **DevSecOps**: GitOps, Harness, OPA, seguridad, chaos engineering
6. **Data Engineer**: Pipelines KSQL, Spark Streaming, Kafka Connect, Debezium
7. **Data Scientist**: MLOps, Vertex.ai, FinOps LLM, modelos forecast/anomalías
8. **Finanzas**: TCO, CAPEX/OPEX, CUD/RI, unit economics, sensibilidades

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
- Topología de red (Cloudflare)
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

1. Latencia OT/SCADA
2. Viabilidad RPO/RTO=0 inter-región
3. .exe locales en procedimientos almacenados
4. Brecha de skills GCP/FinOps
5. Ventanas de planta/freeze
6. Etiquetado/Reserved Instances
7. Seguridad/compliance
8. Licenciamiento
9. Cortes de energía en Monterrey
10. Dependencias ocultas
11. Shadow-IT
12. Adopción Cloudflare Zero Trust

## Supuestos Clave

1. **Confluent + VMware on-premise**: Asumimos que se puede desplegar arquitectura idéntica administrada por Confluent en entornos on-premise usando VMware vSphere y Tanzu
2. **Facturación GCP consolidada**: Confluent y Grafana pueden facturarse via GCP Marketplace con órdenes de compra
3. **Skills internos**: Se requiere upskilling significativo en Kafka, Kubernetes, FinOps
4. **Conectores propietarios**: Proveedores de SCADA pueden tener conectores para enviar CDC a Kafka (investigar)
5. **Redpanda para desarrollo**: Viabilidad de replicar arquitectura en laptops para dev/test
6. **Cast.ai savings**: 40% de reducción es alcanzable según benchmarks
7. **Cloudflare performance**: Optimización IA de tráfico compensa latencia añadida
8. **OPA enforcement**: Todas las políticas pueden ser enforzadas pre-despliegue
9. **Interconnect capacidad**: 1Gbps suficiente para workloads iniciales, requiere monitoreo
10. **Change Data Capture**: Todos los sistemas legacy soportan CDC via Kafka Connect/Debezium

## Tecnologías Complementarias

### Entorno de Desarrollo Local
- **Redpanda**: Kafka-compatible ligero para laptops
- **Spark Standalone**: Procesamiento local
- **Docker Compose**: Orquestación local
- **Kind/Minikube**: Kubernetes local

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
