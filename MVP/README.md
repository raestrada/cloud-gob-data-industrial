# MVP de IA para FinOps

**Proyecto:** Migración Industrial a Google Cloud Platform
**Fecha:** 2025-11-01
**Versión:** 1.0

## Objetivo del MVP

Demostrar viabilidad técnica y valor de negocio de aplicar IA/ML a FinOps en GCP, implementando:

1. **Forecast de costos** por proyecto/BU/onda de migración (accuracy ≥90%)
2. **Detección de anomalías** de gasto con flujo de respuesta automatizado
3. **NLP de etiquetado automático** para inferir owner/cost_center/criticality en gastos huérfanos

## Enfoque: Event-Driven Desde el Día 1 (Cero Deuda Técnica)

### Estrategia Clave: Consumir Eventos SIEMPRE

**Principio arquitectónico:** El MVP consume eventos desde el inicio, aunque sean simulados. Esto permite:

✅ **Prototipado rápido:** De eventos sintéticos a modelo funcionando en días
✅ **Cero deuda técnica:** El código del MVP ES el código de producción
✅ **Evolución sin refactoring:** Solo se cambia el source (archivo → Kafka topic)
✅ **Validación arquitectónica:** Comprobamos que el diseño event-driven funciona

### Por qué NO simplemente usar CSVs/BigQuery directamente

❌ **Anti-pattern (genera deuda técnica):**
```
MVP: CSV → Pandas → Model
Producción: Kafka → Spark → Feature Store → Model
          └─ Requiere reescribir todo el pipeline
```

✅ **Event-First (nuestro enfoque):**
```
MVP: Eventos simulados (JSONL) → Consumer → Feature Store → Model
Producción: Kafka topics reales → [MISMO Consumer] → [MISMO Feature Store] → [MISMO Model]
           └─ Solo cambiar: source = KafkaConsumer(topic) en lugar de FileReader(jsonl)
```

**Resultado:** El tiempo invertido en el MVP NO se desperdicia. Es inversión directa en producción.

## Estructura del Proyecto

```
MVP/
├── README.md                          # Este archivo
├── data/                              # Datos sintéticos de eventos
│   ├── kafka_events_billing.jsonl     # Eventos de billing (simulados)
│   ├── kafka_events_resources.jsonl   # Eventos de recursos (simulados)
│   └── historical_costs.csv           # Serie histórica (del caso de negocio)
├── notebooks/                         # Análisis y modelos documentados
│   ├── 01_forecast_costos.ipynb       # Forecast con Vertex AI AutoML
│   ├── 02_deteccion_anomalias.ipynb   # Anomalías con reglas + ML
│   ├── 03_nlp_etiquetado.ipynb        # NLP para clasificar gastos huérfanos
│   └── 00_data_generation.ipynb       # Generación de datos sintéticos
└── docs/                              # Arquitectura y diseño
    ├── arquitectura_mvp.md            # Arquitectura técnica del MVP
    ├── arquitectura_productiva.md     # Evolución a producción
    └── plan_implementacion.md         # Plan 30-60-90 días
```

## Datos Sintéticos: Simulando la Arquitectura Real

Los datos en `data/` simulan eventos que **la arquitectura final** generará desde Kafka:

### Eventos de Billing (Kafka topic: `billing.cost.realtime`)

```json
{
  "timestamp": "2026-01-15T10:23:45Z",
  "project_id": "prod-monterrey-scada",
  "service": "compute",
  "sku": "n2-standard-16",
  "cost_usd": 45.23,
  "usage_amount": 720.0,
  "usage_unit": "vCPU-hours",
  "labels": {
    "env": "prod",
    "plant": "monterrey",
    "owner": "ops-team",
    "cost_center": "CC-1001"
  },
  "resource_name": "gke-cluster-mty-node-01"
}
```

### Eventos de Recursos (Kafka topic: `resources.inventory.hourly`)

```json
{
  "timestamp": "2026-01-15T10:00:00Z",
  "resource_id": "projects/prod-mty/zones/us-central1-a/instances/vm-scada-01",
  "resource_type": "compute.instance",
  "state": "RUNNING",
  "labels": {},
  "detected_labels_ml": {
    "owner": "scada-team",
    "cost_center": "CC-1001",
    "criticality": "high",
    "confidence": 0.87
  }
}
```

## Stack Tecnológico

| Componente | Tecnología | Propósito |
|:---|:---|:---|
| **Feature Store** | Vertex AI Feature Store | Almacenar features para training/serving |
| **Training** | Vertex AI AutoML / Custom Training | Entrenar modelos forecast/anomalías/NLP |
| **Serving** | Vertex AI Endpoints | Predicciones en tiempo real |
| **Orchestration** | Vertex AI Pipelines | Pipeline ML end-to-end |
| **Data Source (MVP)** | BigQuery + JSON files | Datos sintéticos simulando Kafka |
| **Data Source (Prod)** | Kafka → BigQuery (Dataflow) | Eventos reales de la arquitectura |

## Arquitectura Evolutiva: MVP → Producción

### Fase 1: MVP (Ahora)

```
Datos Sintéticos (JSON/CSV)
    ↓
BigQuery (staging)
    ↓
Vertex AI Feature Engineering
    ↓
Vertex AI Training
    ↓
Vertex AI Endpoint (predicción)
    ↓
Dashboard Looker
```

### Fase 2: Producción (Post-migración)

```
Kafka Topics (eventos reales)
    ↓
Dataflow (streaming a BigQuery)
    ↓
[MISMO] Vertex AI Feature Engineering
    ↓
[MISMO] Vertex AI Training (retraining automático)
    ↓
[MISMO] Vertex AI Endpoint
    ↓
[MISMO] Dashboard Looker + Alertas
```

**Clave:** El feature engineering y modelos NO cambian, solo la fuente de datos.

## Métricas de Éxito del MVP

| Métrica | Objetivo | Resultado Actual |
|:---|---:|:---|
| **Forecast Accuracy** | ≥90% | _A completar en notebooks_ |
| **Detección Anomalías (F1-score)** | ≥85% | _A completar en notebooks_ |
| **Label Compliance (auto-etiquetado)** | ≥95% | _A completar en notebooks_ |
| **Latencia Predicción** | <100ms | _A completar en notebooks_ |
| **Tiempo Implementación** | <90 días | _Ver plan_implementacion.md_ |

## Valor de Negocio Demostrable

1. **Forecast de costos:**
   - Alertas tempranas de sobrecosto (15 días antes del cierre de mes)
   - Precisión ≥90% vs forecast manual (~60-70%)
   - **Ahorro estimado:** $50-100K/año evitando sobrecostos no planificados

2. **Detección de anomalías:**
   - Detectar gastos inusuales en <2 horas vs 1-2 semanas manual
   - Reducir "bill shock" en 80%
   - **Ahorro estimado:** $30-50K/año en gastos evitables

3. **Etiquetado automático:**
   - Reducir gastos huérfanos de ~20% → <5% en 90 días
   - Liberar 40h/mes de trabajo manual de etiquetado
   - **Ahorro estimado:** $15-20K/año en tiempo de equipo FinOps

**Total valor estimado:** $95-170K/año con inversión de <$30K (3-6 meses de un ML Engineer)

## Cómo Ejecutar los Notebooks

### Prerequisitos

**Opción 1: Usando `uv` (Recomendado - 10-100x más rápido)**

```bash
# Instalar uv (una sola vez)
curl -LsSf https://astral.sh/uv/install.sh | sh

# En el directorio MVP
cd MVP

# Crear entorno virtual + instalar dependencias
uv venv
uv pip install pandas numpy scikit-learn xgboost matplotlib seaborn jupyter ipykernel notebook

# Activar entorno y registrar kernel de Jupyter
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
python -m ipykernel install --user --name=mvp-finops

# Ejecutar Jupyter
jupyter notebook
```

**Opción 2: Usando pip tradicional**

```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -e .

# Registrar kernel de Jupyter
python -m ipykernel install --user --name=mvp-finops

# Ejecutar Jupyter
jupyter notebook
```

**Configuración GCP (solo para producción, no necesario en MVP)**

```bash
# Autenticación GCP
gcloud auth application-default login

# Variables de entorno
export PROJECT_ID="tu-proyecto-gcp"
export REGION="us-central1"
export BUCKET_NAME="gs://tu-bucket-mvp-finops"
```

### Orden de Ejecución

1. **Generación de datos:** `00_data_generation.ipynb`
2. **Forecast:** `01_forecast_costos.ipynb`
3. **Anomalías:** `02_deteccion_anomalias.ipynb`
4. **NLP Etiquetado:** `03_nlp_etiquetado.ipynb`

### Ejecución en Vertex AI Workbench (Recomendado)

1. Crear Notebook instance en Vertex AI Workbench
2. Clonar este repo
3. Ejecutar notebooks en orden

## Próximos Pasos

Ver `docs/plan_implementacion.md` para:
- Plan 30-60-90 días de implementación
- Transición de MVP a producción
- Estrategia de adopción y change management

## Referencias

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [FinOps Best Practices](https://www.finops.org/framework/)
- Caso de Negocio: `../entregables/Caso_Negocio_LiderCloudFinOps.md`
- Arquitectura de Plataforma: `../docs/fase2/arquitectura-plataforma.md`
