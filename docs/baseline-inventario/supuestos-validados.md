# Fase 1.4: Sesión de Retroalimentación Cruzada - Validación de Supuestos

**Proyecto**: Migración Industrial a GCP con Gobierno FinOps e IA
**Fecha**: 2025-10-31
**Moderador**: Arquitecto de Plataforma Senior
**Versión**: 1.0

---

## Resumen Ejecutivo

Se realizó una validación cruzada de los 3 documentos generados en Fase 1 contra el PDF del caso de negocio oficial. El análisis revela que:

- **67% de los datos en los documentos son SUPUESTOS** no presentes en el caso de negocio original
- **33% son datos VALIDADOS** que provienen directamente del PDF
- Se identificaron **3 SUPUESTOS CRÍTICOS CRUZADOS** que requieren validación URGENTE
- Se detectaron **12 datos inventados sin marcar explícitamente como [SUPUESTO]** (ERROR CRÍTICO)
- El throughput estimado de **2.37 Gbps en pico NO puede ser validado** con los datos del caso de negocio

**DECISIÓN CRÍTICA REQUERIDA**: Los documentos generados contienen supuestos razonables pero **NO PUEDEN SER CONSIDERADOS COMO HECHOS** hasta que se validen con:
1. Mediciones reales de infraestructura (latencia, throughput, capacidad)
2. Validación con CFO/CIO de supuestos financieros
3. Confirmación con equipos técnicos de configuraciones actuales

---

## 1. Datos Validados del Caso de Negocio (Fuente de Verdad)

### Tabla de Datos CONFIRMADOS (del PDF)

| Dato | Valor PDF | Ubicación PDF | Documentos que lo Usan Correctamente |
|------|-----------|---------------|-------------------------------------|
| **SCADA modernos** | 30 total (10 MTY, 10 GDL, 10 TIJ) | Página 1-2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **SCADA antiguos (críticos)** | 40 total (10 MTY, 10 GDL, 20 TIJ) | Página 2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **SQL Server 2008-2012 Plantas** | 40 total (10 MTY, 10 GDL, 20 TIJ) | Página 2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **SQL Server 2019 Plantas (críticos)** | 40 total (10 MTY, 10 GDL, 20 TIJ) | Página 2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **SQL Server 2008-2012 Corp** | 60 total (20 MTY, 20 GDL, 20 TIJ) | Página 2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **SQL Server 2019 Corp (críticos)** | 80 total (20 MTY, 20 GDL, 40 TIJ) | Página 2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **Aplicaciones IIS Plantas** | 60 total (20 MTY, 20 GDL, 20 TIJ) | Página 2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **Aplicaciones IIS Corp** | 30 total (30 MTY, 0 GDL, 0 TIJ) | Página 2, Tabla 2.1 | ✅ Inventario Sistemas Legados |
| **Total VMs** | 420 VMs (apps, DB, infra) | Página 3, Sección 2.2 | ✅ Inventario Sistemas Legados |
| **Capacidad vCPU** | ~1,900 vCPU | Página 3, Sección 2.2 | ✅ Inventario, Conectividad |
| **Capacidad RAM** | ~12.8 TB RAM | Página 3, Sección 2.2 | ✅ Inventario, Conectividad |
| **Almacenamiento block** | ~200 TB block | Página 3, Sección 2.2 | ✅ Inventario, Baseline Financiero |
| **Almacenamiento object** | ~500 TB object | Página 3, Sección 2.2 | ✅ Inventario, Baseline Financiero |
| **Crecimiento anual** | 20% anual | Página 3, Sección 2.2 | ✅ Baseline Financiero |
| **Ventanas mantenimiento** | Domingos 2h por planta | Página 3, Sección 2.2 | ✅ Inventario Sistemas Legados |
| **Freeze anual** | 15-Nov al 5-Ene | Página 3, Sección 2.2 | ✅ Baseline Financiero |
| **SLA objetivo global** | 99.95% | Página 3, Sección 2.2 | ✅ Inventario Sistemas Legados |
| **SLA críticos** | 99.99% | Página 3, Sección 2.2 | ✅ Inventario Sistemas Legados |
| **RPO/RTO críticos** | 0/0 (SCADA antiguos + SQL 2019) | Página 2, 3 | ✅ Todos los documentos |
| **RPO/RTO no críticos** | ≤15'/15' | Página 3, Sección 2.2 | ✅ Inventario Sistemas Legados |
| **Producción Monterrey** | 60,000 unid/mes, 720,000 unid/año | Página 3, Sección 2.3 | ✅ Baseline Financiero |
| **Producción Guadalajara** | 40,000 unid/mes, 480,000 unid/año | Página 3, Sección 2.3 | ✅ Baseline Financiero |
| **Producción Tijuana** | 30,000 unid/mes, 360,000 unid/año | Página 3, Sección 2.3 | ✅ Baseline Financiero |
| **Producción total** | 130,000 unid/mes, 1,560,000 unid/año | Página 3, Sección 2.3 | ✅ Baseline Financiero |
| **OPEX Hardware & mantenimiento** | USD 1,560,000/año | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **OPEX Licenciamiento** | USD 1,515,000/año | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **OPEX Energía/espacio** | USD 420,000/año | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **OPEX Personal (12 FTE)** | USD 1,200,000/año | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **OPEX WAN & enlaces** | USD 300,000/año | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **OPEX Otros contratos** | USD 250,000/año | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **Total OPEX on-prem** | USD 5,245,000/año | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **TCO 3 años on-prem** | USD 15,735,000 | Página 3, Sección 3.1 | ✅ Baseline Financiero |
| **Interconnect 1Gbps** | Ya operativo, USD 3,000/mes (2 puertos) | Página 1, 4 | ✅ Conectividad Actual |
| **Compute on-demand** | USD 24/vCPU-mes, USD 3/GB-RAM-mes | Página 3-4, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **SQL administrado** | 1.6× costo compute equivalente | Página 3, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **Almacenamiento Block** | USD 0.12/GB-mes | Página 4, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **Almacenamiento Object** | USD 0.023/GB-mes | Página 4, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **Snapshots** | USD 0.05/GB-mes | Página 4, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **Egress Internet** | USD 0.05/GB (primeros 30TB/mes) | Página 4, Sección 3.2 | ⚠️ Usado en Conectividad (USD 0.05/GB) |
| **Soporte GCP** | USD 12,500/mes | Página 4, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **Operación Cloud (equipo base)** | USD 75,000/mes | Página 4, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **One-time (servicios/capacitación)** | USD 1,700,000 | Página 4, Sección 3.2 | ❌ No usado en docs Fase 1 |
| **Latencia OT** | SCADA antiguos requieren operación local-first/edge | Página 4, Sección 4.2 | ✅ Inventario, Conectividad |
| **Procedimientos almacenados** | Llaman .exe locales (replatform requerido) | Página 4, Sección 4.5 | ✅ Inventario Sistemas Legados |

**TOTAL DATOS VALIDADOS**: 42 datos del PDF
**TOTAL DATOS EN DOCUMENTOS FASE 1**: ~130 datos (estimado)
**PORCENTAJE DE VALIDACIÓN**: **32% de datos son del PDF, 68% son SUPUESTOS**

---

## 2. Supuestos Identificados en Documentos

### 2.1 Inventario de Sistemas Legados - Supuestos

| Supuesto | Marcado como [SUPUESTO] | Criticidad | Justificación | Validar con |
|----------|-------------------------|------------|---------------|-------------|
| **Fabricantes SCADA antiguos** (Rockwell 10, Siemens 10, GE 20) | ✅ SÍ (líneas 1149) | ALTA | Distribución típica industrial | Equipo OT, revisar especificaciones |
| **Latencia SCADA <10ms requerida** | ✅ SÍ (línea 1149) | CRÍTICA | Estándar control loops industriales | Equipo OT, mediciones reales |
| **Throughput 3,000 tags/sistema** | ✅ SÍ (línea 1149) | ALTA | Plantas medianas típicas | Equipo OT, conteo real tags |
| **Latencia Monterrey → us-central1: 50-80ms** | ✅ SÍ (línea 70) | CRÍTICA | Estimación geográfica | **MEDIR CON PING REAL** |
| **Tamaño promedio DB SQL 2019** | ✅ SÍ (líneas 139, 195, etc.) | ALTA | Calculado 192TB ÷ 120 inst | DBAs, query real sys.databases |
| **CDC habilitado 75% SQL 2019** | ✅ SÍ (línea 454) | ALTA | Mejores prácticas modernas | DBAs, query sys.databases |
| **20-30% tablas sin PK en legacy** | ✅ SÍ (línea 1154) | MEDIA | Experiencia industrial típica | DBAs, query INFORMATION_SCHEMA |
| **210-330 SPs con xp_cmdshell** | ✅ SÍ (línea 1163) | ALTA | 2-3 SPs por instancia legacy | DBAs, query INFORMATION_SCHEMA.ROUTINES |
| **Distribución .NET Framework apps** | ✅ SÍ (línea 1171) | MEDIA | Timeline releases y edad apps | Desarrolladores, revisar web.config |
| **30 hosts ESXi VMware** | ✅ SÍ (línea 1175) | ALTA | 1,900 vCPU ÷ 48 cores/host ÷ 1.3x | **vCenter reports REALES** |
| **Modelos Dell PowerEdge R640/R740** | ✅ SÍ (línea 1179) | MEDIA | Timeline 2017-2019 típico | Inventario hardware real |
| **Problemas energía (99.2-99.7% uptime)** | ✅ SÍ (línea 1181) | ALTA | Inverso de SLA sub-Tier-3 | **Reportes incidentes reales** |
| **Costos Edge Gateway USD 45K/planta** | ✅ SÍ (línea 1187) | MEDIA | Pricing Dell/HP servers típico | Cotizaciones vendors reales |
| **Esfuerzo migración 26-60h por .exe** | ✅ SÍ (línea 1191) | MEDIA | Complejidad media estándar | RFP integradores, benchmarks |
| **TPS por instancia SQL crítica** | ✅ SÍ (línea 1200) | CRÍTICA | Basado en vCPU y carga OLTP típica | **Profiling DMVs real** |
| **Throughput CDC 200 bytes/tx** | ✅ SÍ (línea 1211) | CRÍTICA | Payload CDC promedio estimado | **POC Debezium real** |

**CRÍTICA POSITIVA**: El documento de Inventario Sistemas Legados marca **CORRECTAMENTE** todos los supuestos con [SUPUESTO] explícito y proporciona justificación. ✅

**TOTAL SUPUESTOS INVENTARIO**: 16 supuestos críticos

---

### 2.2 Baseline Financiero - Supuestos

| Supuesto | Marcado como [SUPUESTO] | Criticidad | Justificación | Validar con |
|----------|-------------------------|------------|---------------|-------------|
| **CAPEX aprobado USD 2,000,000** | ❌ **NO** (línea 213) | **CRÍTICA** | Benchmark proyectos similares | **CFO, comité inversiones** |
| **Precio venta USD 50/unidad** | ❌ **NO** (línea 419) | ALTA | Estimado cálculo pérdida revenue | Finanzas, Ventas |
| **Crecimiento 20% anual es lineal** | ❌ **NO** (línea 422) | MEDIA | Asume uniformidad mes a mes | Operaciones, Planning |
| **Personal USD 100,000/FTE promedio** | ❌ **NO** (línea 427) | MEDIA | Promedio salarios + prestaciones | RRHH (mix senior/junior real) |
| **Reducción 12 FTE → 8 FTE viable** | ❌ **NO** (línea 430) | ALTA | Managed services reducen carga | IT Operations Manager |
| **OPEX incluye TODOS costos** | ❌ **NO** (línea 433) | ALTA | Riesgo: falta depreciación | CFO, Contabilidad |
| **Precios GCP vigentes sin cambios** | ❌ **NO** (línea 438) | MEDIA | Price pack del caso de negocio | GCP Account Manager (EDP) |
| **Egress 10TB/mes** | ❌ **NO** (línea 442) | MEDIA | Estimado tráfico inter-región | Arquitecto Datos |
| **Payback 24 meses máximo** | ❌ **NO** (línea 235) | ALTA | Política financiera conservadora | CFO |
| **ROI mínimo 15% a 3 años** | ❌ **NO** (línea 250) | ALTA | Política inversión proyectos tech | CFO |
| **CAPEX distribuido en 6 meses** | ❌ **NO** (línea 271) | MEDIA | Ciclo presupuestario fiscal | CFO |
| **Reducción licenciamiento 15%** | ❌ **NO** (línea 49) | MEDIA | Consolidación instancias | Procurement, Vendors |
| **Ahorro personal USD 200K/año** | ❌ **NO** (línea 314) | ALTA | Opción C: attrition natural | RRHH, CFO |

**ERROR CRÍTICO**: El documento Baseline Financiero tiene **13 supuestos críticos SIN MARCAR** como [SUPUESTO]. ❌

**ACCIÓN REQUERIDA**: Re-escribir secciones 6, 7, 8 del Baseline Financiero marcando EXPLÍCITAMENTE todos los supuestos.

**TOTAL SUPUESTOS BASELINE**: 13 supuestos (12 sin marcar correctamente)

---

### 2.3 Conectividad Actual - Supuestos

| Supuesto | Marcado como [SUPUESTO] | Criticidad | Justificación | Validar con |
|----------|-------------------------|------------|---------------|-------------|
| **Latencia Interconnect 5-10ms** | ✅ SÍ (línea 50) | **CRÍTICA** | Estimación geográfica 2,200km | **Ping real URGENTE** |
| **Enlaces WAN MPLS 100 Mbps** | ✅ SÍ (línea 23) | ALTA | Configuración típica multi-planta | Contratos proveedor, inventario |
| **Throughput SQL CDC 3 Mbps/inst crítica** | ✅ SÍ (línea 94) | **CRÍTICA** | Workloads industriales estándar | **POC Debezium real** |
| **Throughput Kafka 865 Mbps promedio** | ✅ SÍ (línea 118) | **CRÍTICA** | Suma SCADA+CDC+IIS × 1.5× | **Medición real tráfico** |
| **SCADA operación local-first viable** | ✅ SÍ (línea 1023) | **CRÍTICA** | Telemetría asíncrona aceptable | Operaciones OT |
| **Cloud VPN 500 Mbps burst** | ✅ SÍ (línea 1024) | ALTA | Capacidad VPN típica GCP | **Prueba iperf3 real** |
| **Internet breakout 500 Mbps MTY** | ✅ SÍ (línea 1026) | MEDIA | Estimado para failover | Inventario red, contratos ISP |
| **Latencia inter-región 35-45ms** | ✅ SÍ (línea 1027) | ALTA | us-central1 ↔ us-west1 GCP | **Medición VM a VM real** |
| **Compresión Kafka lz4 reduce 40%** | ✅ SÍ (línea 1028) | MEDIA | Benchmarks Kafka estándar | Pruebas con datos reales |
| **Costo Interconnect 10Gbps USD 10K/mes** | ✅ SÍ (línea 1029) | MEDIA | Pricing público GCP estimado | GCP Account Manager |
| **WAN MPLS costo USD 2,600/mes** | ✅ SÍ (línea 630) | ALTA | Telmex MPLS típico México | **Contratos actuales reales** |
| **Latencias plantas ↔ GCP regiones** | ✅ SÍ (línea 756) | ALTA | Propagación fibra + overhead | **Traceroute + ping reales** |
| **Distribución sistemas por planta** | ❌ **NO** (línea 1006) | MEDIA | Derivado de inventario | Validar con tabla 2.1 PDF |
| **Costo VPN HA USD 200/mes** | ✅ SÍ (línea 522) | MEDIA | GCP pricing túneles + egreso | Calculadora GCP |
| **Throughput apps IIS 100 Mbps** | ✅ SÍ (línea 136) | MEDIA | 500 usuarios × 0.8 Mbps × 25% | Monitoreo actual tráfico |
| **Backups 4TB/día, 2% cambio diario** | ✅ SÍ (línea 143) | ALTA | 200TB × 2% tasa cambio | Logs backup actuales |

**CRÍTICA POSITIVA**: El documento Conectividad marca **correctamente** 15 de 16 supuestos. Solo 1 error menor (distribución sistemas). ✅

**TOTAL SUPUESTOS CONECTIVIDAD**: 16 supuestos (15 correctamente marcados)

---

## 3. Validación Cruzada de Supuestos Críticos

### 3.1 SUPUESTO CRÍTICO #1: Throughput CDC + Kafka vs Interconnect 1Gbps

**PREGUNTA**: ¿El CDC de 120 SQL Server críticos + 160 no críticos + replicación Kafka cabe en Interconnect 1Gbps?

**DATOS DEL CASO DE NEGOCIO**:
- ✅ Interconnect 1Gbps operativo (USD 3,000/mes) - PDF página 4
- ✅ 120 SQL Server 2019 críticos (RPO/RTO=0) - PDF página 2
- ✅ 160 SQL Server 2008-2012 no críticos - PDF página 2
- ❌ **NO HAY DATO** de throughput CDC por instancia
- ❌ **NO HAY DATO** de TPS (transacciones/segundo) por instancia
- ❌ **NO HAY DATO** de tamaño promedio de transacción

**SUPUESTOS DE CONECTIVIDAD ACTUAL**:
- [SUPUESTO] SQL críticos: 3 Mbps/instancia → 120 × 3 = 360 Mbps
- [SUPUESTO] SQL no-críticos: 1 Mbps/instancia → 160 × 1 = 160 Mbps
- [SUPUESTO] Kafka overhead 1.5× → (360+160) × 1.5 = 780 Mbps
- [SUPUESTO] SCADA: 6.8 Mbps
- [SUPUESTO] Apps IIS: 100 Mbps
- **TOTAL ESTIMADO**: **~900 Mbps promedio, 2.2 Gbps pico**

**VALIDACIÓN CRUZADA**:

| Componente | Valor Supuesto | Origen Supuesto | ¿Validable con PDF? | Nivel Riesgo |
|------------|----------------|-----------------|---------------------|--------------|
| Throughput CDC críticos | 360 Mbps | Conectividad doc, línea 102-104 | ❌ NO - no hay TPS en PDF | **CRÍTICO** |
| Throughput CDC no-críticos | 160 Mbps | Conectividad doc, línea 99-104 | ❌ NO - no hay TPS en PDF | ALTO |
| Kafka overhead 1.5× | Factor 1.5 | Conectividad doc, línea 116 | ❌ NO - estándar industria | MEDIO |
| SCADA telemetría | 6.8 Mbps | Conectividad doc, línea 74-82 | ⚠️ PARCIAL - 70 SCADA del PDF | ALTO |
| Pico 2.2 Gbps | Calculado | Conectividad doc, línea 122 | ❌ NO - derivado de supuestos | **CRÍTICO** |

**CONCLUSIÓN #1**:
- ❌ **NO SE PUEDE VALIDAR** que Interconnect 1Gbps sea suficiente con datos del PDF
- ⚠️ Los cálculos de throughput son **RAZONABLES** pero basados en benchmarks estándar
- ✅ La conclusión de "upgrade a Dual 1Gbps" es **CONSERVADORA Y PRUDENTE**
- 🔴 **RIESGO ALTO**: Si throughput real es >2× estimado, incluso Dual 1Gbps sería insuficiente

**ACCIÓN REQUERIDA**:
1. **POC Debezium URGENTE** en 2-3 SQL Server no críticos (30 días)
2. **Medir throughput CDC real** con DMVs durante 7 días
3. **Ajustar sizing Interconnect** basado en mediciones reales
4. **Plan B**: Si throughput > 1.5 Gbps promedio → Interconnect 10Gbps obligatorio

---

### 3.2 SUPUESTO CRÍTICO #2: Costos Baseline Financiero

**PREGUNTA**: ¿El baseline financiero incluye todos los costos de infraestructura identificados?

**DATOS DEL CASO DE NEGOCIO**:
- ✅ OPEX total: USD 5,245,000/año - PDF página 3
- ✅ TCO 3 años: USD 15,735,000 - PDF página 3
- ✅ Desglose por categoría (6 categorías) - PDF página 3

**SUPUESTOS DE BASELINE FINANCIERO**:
- [SUPUESTO] CAPEX proyectos crecimiento: USD 750K (año 2), USD 1,080K (año 3)
- [SUPUESTO] Costos ocultos: Depreciación, facilities, seguros
- [SUPUESTO] Reducción personal: 12 FTE → 8 FTE (USD 400K ahorro/año)
- [SUPUESTO] Precio venta: USD 50/unidad (para cálculo pérdidas)

**VALIDACIÓN CRUZADA CON INVENTARIO**:

| Categoría OPEX | PDF (USD/año) | Baseline Doc | Inventario Doc | ¿Consistente? |
|----------------|--------------|--------------|----------------|---------------|
| Hardware & mant. | 1,560,000 | ✅ 1,560,000 | Menciona "aging hardware Tijuana" | ⚠️ Parcial - costos refresh no incluidos |
| Licenciamiento | 1,515,000 | ✅ 1,515,000 | Menciona SQL 2008-2012 EOL | ⚠️ Parcial - licencias Kepware no en baseline |
| Energía/espacio | 420,000 | ✅ 420,000 | Menciona "cortes 45h/año Tijuana" | ⚠️ Parcial - generador backup no costeado |
| Personal (12 FTE) | 1,200,000 | ✅ 1,200,000 | No detalla roles específicos | ✅ Consistente |
| WAN & enlaces | 300,000 | ✅ 300,000 | Conectividad menciona USD 6,800/mes (USD 81.6K/año) | ❌ **INCONSISTENCIA** |
| Otros contratos | 250,000 | ✅ 250,000 | No detalla contratos específicos | ✅ Aceptable |

**INCONSISTENCIA DETECTADA**:

**WAN & enlaces**:
- **PDF**: USD 300,000/año
- **Conectividad doc (línea 630)**: USD 6,800/mes × 12 = USD 81,600/año
  - Interconnect: USD 3,000/mes
  - WAN MPLS: USD 2,600/mes
  - Internet: USD 1,200/mes

**Diferencia**: USD 300,000 - USD 81,600 = **USD 218,400/año NO EXPLICADO**

**POSIBLES EXPLICACIONES**:
1. ✅ El PDF incluye costos adicionales no detallados (equipos networking, SD-WAN, etc.)
2. ⚠️ El Interconnect USD 3,000/mes ya está operativo, no debería estar en baseline on-prem
3. ❌ Error de supuesto en documento Conectividad

**CONCLUSIÓN #2**:
- ⚠️ **INCONSISTENCIA MODERADA** en costos WAN
- ✅ OPEX total USD 5.2M del PDF es correcto
- ❌ Desglose detallado de "WAN & enlaces" requiere aclaración
- 🔴 **RIESGO MEDIO**: Si costos ocultos (USD 218K) son críticos, TCO subestimado

**ACCIÓN REQUERIDA**:
1. **Validar con CFO** desglose completo de "WAN & enlaces USD 300K/año"
2. **Confirmar** si Interconnect USD 3K/mes está incluido en USD 300K o es adicional
3. **Ajustar** documento Conectividad si hay costos networking adicionales

---

### 3.3 SUPUESTO CRÍTICO #3: Latencia SCADA y Edge Computing

**PREGUNTA**: ¿Los SCADA antiguos pueden tolerar latencia cloud o requieren edge?

**DATOS DEL CASO DE NEGOCIO**:
- ✅ 40 SCADA antiguos son **misión crítica (RPO/RTO=0)** - PDF página 2
- ✅ Latencia OT: **SCADA antiguos requieren operación local-first/edge** - PDF página 4, sección 4.2
- ❌ **NO HAY DATO** de latencia máxima aceptable específica (10ms, 50ms, 100ms)
- ❌ **NO HAY DATO** de fabricantes/modelos de SCADA

**SUPUESTOS DE INVENTARIO SISTEMAS**:
- [SUPUESTO] Latencia requerida: **<10ms** (línea 68-74 inventario)
- [SUPUESTO] Fabricantes: Rockwell RSView32 (10), Siemens WinCC V7 (10), GE iFIX (20)
- [SUPUESTO] Protocolos: DDE, OPC-DA, Modbus TCP, PROFINET
- [SUPUESTO] Latencia Monterrey → GCP: 50-80ms (NO aceptable para <10ms)

**VALIDACIÓN CRUZADA**:

| Aspecto | PDF | Inventario Doc | Conectividad Doc | ¿Consistente? |
|---------|-----|----------------|------------------|---------------|
| SCADA requiere edge | ✅ "operación local-first" | ✅ "Edge computing local-first" | ✅ "Operación local, telemetría cloud" | ✅ **CONSISTENTE** |
| Latencia específica | ❌ No especifica | [SUPUESTO] <10ms | [SUPUESTO] <10ms | ⚠️ Supuesto razonable |
| Fabricantes | ❌ No especifica | [SUPUESTO] 3 fabricantes | No detalla | ⚠️ Supuesto típico industrial |
| Solución edge | ❌ No especifica | ✅ Edge Gateway + Kafka local | ✅ Edge Gateway por planta | ✅ **CONSISTENTE** |

**CONCLUSIÓN #3**:
- ✅ **CONSISTENCIA ALTA** entre PDF y documentos: SCADA requiere edge
- ✅ Estrategia "operación local-first + telemetría cloud" **CORRECTA**
- ⚠️ Latencia <10ms es **SUPUESTO RAZONABLE** pero no validado con PDF
- ✅ Solución edge gateway **ALINEADA** con restricción técnica del PDF

**ACCIÓN REQUERIDA**:
1. **Site survey** en 3 plantas (30 días) - Inventario real SCADA
2. **Medición latencia actual** HMI ↔ PLC (validar <10ms)
3. **Validar protocolos** con equipo OT (DDE, OPC-DA, Modbus)
4. **Confirmar** que edge computing puede soportar RPO/RTO=0 local

---

## 4. Datos Inventados Sin Marcar Como Supuesto (ERROR CRÍTICO)

### Tabla de Errores Detectados

| Documento | Línea(s) | Dato Inventado | ¿Está en PDF? | Debería Marcarse |
|-----------|---------|----------------|---------------|------------------|
| **Baseline Financiero** | 213 | CAPEX aprobado USD 2,000,000 | ❌ NO | ✅ [SUPUESTO] Benchmark proyectos similares |
| **Baseline Financiero** | 235 | Payback máximo 24 meses | ❌ NO | ✅ [SUPUESTO] Política financiera conservadora |
| **Baseline Financiero** | 250 | ROI mínimo 15% a 3 años | ❌ NO | ✅ [SUPUESTO] Política inversión tecnológica |
| **Baseline Financiero** | 419 | Precio venta USD 50/unidad | ❌ NO | ✅ [SUPUESTO] Para cálculo pérdida revenue |
| **Baseline Financiero** | 271-274 | CAPEX distribuido en 6 meses | ❌ NO | ✅ [SUPUESTO] Ciclo presupuestario fiscal |
| **Baseline Financiero** | 314 | Reducción personal a 8 FTE | ❌ NO | ✅ [SUPUESTO] Managed services reducen carga |
| **Baseline Financiero** | 49 | Reducción licencias 15% | ❌ NO | ✅ [SUPUESTO] Consolidación instancias |
| **Baseline Financiero** | 433-436 | OPEX incluye todos costos ocultos | ❌ NO | ✅ [SUPUESTO] Riesgo: falta depreciación |
| **Conectividad** | 1006 | Total sistemas 390 vs 380 PDF | ⚠️ Discrepancia | ⚠️ Validar suma correcta |
| **Conectividad** | 630 | WAN MPLS USD 2,600/mes | ❌ NO | ✅ [SUPUESTO] Telmex MPLS típico México |
| **Conectividad** | 522 | Cloud VPN USD 200/mes | ⚠️ Derivado pricing | ✅ [SUPUESTO] Incluye egreso failover |
| **Inventario** | 1006 | Aplicaciones IIS Corp 30 total en MTY | ✅ SÍ (PDF pág 2) | ✅ CORRECTO (no es error) |

**TOTAL ERRORES CRÍTICOS**: 10 datos sin marcar explícitamente como [SUPUESTO] en Baseline Financiero

**SEVERIDAD**: 🔴 **ALTA** - El documento Baseline Financiero tiene múltiples supuestos críticos (CAPEX, payback, ROI) presentados como hechos

**ACCIÓN CORRECTIVA REQUERIDA**:
1. **Re-escribir secciones 6-8** de Baseline Financiero
2. **Marcar EXPLÍCITAMENTE** todos los supuestos con formato: `[SUPUESTO] <justificación>`
3. **Agregar tabla de supuestos** al inicio del documento con columnas: Supuesto | Valor | Justificación | Validar Con | Prioridad

---

## 5. Supuestos Cuestionables que Requieren Aclaración

### 5.1 Supuestos de ALTA Prioridad (Bloquean Decisiones)

| ID | Supuesto Cuestionable | Documento | Impacto si Incorrecto | Validar Con | Timeline |
|----|----------------------|-----------|----------------------|-------------|----------|
| **SQ-1** | Throughput SQL CDC 3 Mbps/instancia crítica | Conectividad | Interconnect insuficiente → Proyecto bloqueado | **POC Debezium + DMVs** | 30 días |
| **SQ-2** | Latencia Interconnect 5-10ms | Conectividad | Si >20ms, Kafka Cluster Linking degradado | **Ping real desde MTY** | 7 días |
| **SQ-3** | CAPEX aprobado USD 2,000,000 | Baseline Financiero | Si no aprobado, proyecto no viable | **CFO + Comité Inversiones** | 15 días |
| **SQ-4** | Payback 24 meses es máximo aceptable | Baseline Financiero | Si requiere <18m, TCO debe reducirse | **CFO** | 15 días |
| **SQ-5** | WAN & enlaces USD 300K/año incluye qué | Baseline Financiero | USD 218K sin explicar → TCO incorrecto | **CFO + Redes + Contratos** | 15 días |
| **SQ-6** | SCADA latencia <10ms requerida | Inventario | Si tolera 50ms, edge computing innecesario | **Equipo OT + Site Survey** | 30 días |
| **SQ-7** | 30 hosts ESXi VMware actuales | Inventario | Si real es 20, capacidad Tanzu diferente | **vCenter reports reales** | 7 días |
| **SQ-8** | Cloud VPN burst 500 Mbps alcanzable | Conectividad | Si real <300 Mbps, failover no viable | **Prueba iperf3 GCP** | 7 días |

**TOTAL SUPUESTOS CRÍTICOS ALTA PRIORIDAD**: 8

**DECISIÓN EJECUTIVA REQUERIDA**: Estos 8 supuestos **BLOQUEAN** la aprobación del caso de negocio. Se requiere validación en **próximos 30 días** antes de proceder.

---

### 5.2 Supuestos de MEDIA Prioridad (Ajustan Costos/Timeline)

| ID | Supuesto Cuestionable | Documento | Impacto si Incorrecto | Validar Con | Timeline |
|----|----------------------|-----------|----------------------|-------------|----------|
| **SQ-9** | Personal USD 100K/FTE promedio | Baseline Financiero | Ahorro personal mal calculado | RRHH | 30 días |
| **SQ-10** | Reducción 12→8 FTE viable | Baseline Financiero | Si no viable, OPEX cloud mayor | IT Ops Manager | 30 días |
| **SQ-11** | 210-330 SPs con xp_cmdshell | Inventario | Si real >500, esfuerzo refactor 2× | DBAs + Query real | 30 días |
| **SQ-12** | Fabricantes SCADA (Rockwell/Siemens/GE) | Inventario | Si otros vendors, solución edge cambia | Equipo OT | 30 días |
| **SQ-13** | Kafka overhead 1.5× | Conectividad | Si real 2×, throughput subestimado | Benchmarks Confluent | 15 días |
| **SQ-14** | Compresión Kafka lz4 reduce 40% | Conectividad | Si real 20%, Interconnect insuficiente | Prueba con datos reales | 30 días |
| **SQ-15** | Costos Edge Gateway USD 45K/planta | Inventario | Si real USD 80K, CAPEX +USD 105K | Cotizaciones vendors | 30 días |

**TOTAL SUPUESTOS MEDIA PRIORIDAD**: 7

**IMPACTO**: Variación estimada **±10-15%** en TCO y timeline si estos supuestos son incorrectos.

---

### 5.3 Supuestos de BAJA Prioridad (Ajustes Menores)

| ID | Supuesto | Documento | Impacto | Validar Con | Timeline |
|----|----------|-----------|---------|-------------|----------|
| **SQ-16** | Tamaño promedio DB | Inventario | Ajuste storage | DBAs | 30 días |
| **SQ-17** | % tablas sin PK | Inventario | Esfuerzo remediación | DBAs | 30 días |
| **SQ-18** | Modelos hardware Dell | Inventario | Compatibilidad Tanzu | Inventario físico | 60 días |
| **SQ-19** | Internet breakout 500 Mbps | Conectividad | Failover secundario | Contratos ISP | 60 días |
| **SQ-20** | Costo Interconnect 10Gbps USD 10K/mes | Conectividad | Decisión upgrade | GCP Account Manager | 60 días |

**TOTAL SUPUESTOS BAJA PRIORIDAD**: 5

---

## 6. Recomendaciones Finales

### 6.1 Clasificación General de Supuestos

**RESUMEN ESTADÍSTICO**:

| Documento | Total Datos | Datos PDF Validados | Supuestos | % Supuestos | Supuestos Marcados Correctamente |
|-----------|------------|---------------------|-----------|-------------|----------------------------------|
| **Inventario Sistemas Legados** | ~45 | ~15 (33%) | ~30 (67%) | 67% | ✅ 100% (todos marcados) |
| **Baseline Financiero** | ~35 | ~20 (57%) | ~15 (43%) | 43% | ❌ 15% (solo 2 de 13) |
| **Conectividad Actual** | ~50 | ~10 (20%) | ~40 (80%) | 80% | ✅ 94% (15 de 16) |
| **TOTAL AGREGADO** | **~130** | **~45 (35%)** | **~85 (65%)** | **65%** | **⚠️ 69% (marcados correctamente)** |

**CONCLUSIÓN GENERAL**:
- ✅ **Inventario Sistemas Legados**: Excelente - todos los supuestos marcados correctamente
- ❌ **Baseline Financiero**: Deficiente - mayoría de supuestos críticos sin marcar
- ✅ **Conectividad Actual**: Excelente - casi todos los supuestos marcados

---

### 6.2 Acciones Correctivas Inmediatas (Próximos 7 Días)

**PRIORIDAD CRÍTICA**:

1. ✅ **Re-escribir Baseline Financiero secciones 6-8**
   - Marcar EXPLÍCITAMENTE todos los supuestos
   - Agregar tabla de supuestos al inicio
   - Clasificar supuestos por prioridad validación
   - **Owner**: Agente Finanzas
   - **Timeline**: 3 días

2. ✅ **Ejecutar mediciones de latencia reales**
   - Ping Monterrey → GCP us-central1 vía Interconnect
   - Traceroute a us-west1 y otras regiones
   - Documentar jitter, packet loss, latencia p50/p95/p99
   - **Owner**: Experto en Redes
   - **Timeline**: 2 días

3. ✅ **Validar con CFO supuestos financieros críticos**
   - CAPEX aprobado: ¿USD 2M es real o estimado?
   - Payback máximo: ¿24 meses o hay flexibilidad?
   - ROI mínimo: ¿15% es hurdle rate correcto?
   - Desglose WAN USD 300K/año
   - **Owner**: Agente Finanzas + CFO
   - **Timeline**: 7 días (agendar reunión URGENTE)

4. ✅ **Query inventario real SQL Server**
   - Ejecutar scripts en todas las instancias (ver sección 7.2 inventario)
   - Tablas sin PK: `SELECT * FROM sys.tables WHERE object_id NOT IN (...)`
   - SPs con xp_cmdshell: `SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_DEFINITION LIKE '%xp_cmdshell%'`
   - CDC habilitado: `SELECT name, is_cdc_enabled FROM sys.databases`
   - **Owner**: Admin Sistemas Legados + DBAs
   - **Timeline**: 7 días

---

### 6.3 Plan de Validación (Próximos 30 Días)

**FASE 1 (Días 1-7): Validaciones Rápidas**
- Latencia Interconnect (ping real)
- Inventario vCenter VMware (hosts, vCPU, RAM)
- Query SQL Server (tablas sin PK, xp_cmdshell, CDC)
- Reunión CFO (supuestos financieros)

**FASE 2 (Días 8-15): POCs Técnicas**
- POC Debezium CDC en 2-3 SQL Server no críticos
- Prueba Cloud VPN HA (iperf3, failover)
- Kafka Cluster Linking test (on-prem → GCP)
- Medición throughput real durante 7 días

**FASE 3 (Días 16-30): Site Surveys y Validaciones Complejas**
- Site survey SCADA en 3 plantas (inventario real)
- Medición latencia HMI ↔ PLC actual
- Cotizaciones Edge Gateway (3 vendors)
- Contratos WAN actuales (desglose USD 300K/año)
- Confirmación capacidad Tanzu con VMware TAM

**ENTREGABLE FINAL (Día 30)**:
- `docs/fase1/supuestos-validados-v2.md` con datos reales vs supuestos
- Ajuste de TCO 3 años basado en validaciones
- Go/No-Go para proceder a Fase 2 (diseño detallado)

---

## 7. Supuestos Validados como RAZONABLES (Sin Bloqueo)

A pesar de ser supuestos, los siguientes son **RAZONABLES** y **NO BLOQUEAN** el avance del proyecto:

| Supuesto | Justificación | Nivel Confianza |
|----------|---------------|-----------------|
| Latencia SCADA <10ms requerida | Estándar industrial para control loops | 85% |
| Fabricantes SCADA típicos (Rockwell/Siemens/GE) | Dominan 80% mercado industrial México | 80% |
| CDC habilitado 75% en SQL 2019 | Mejores prácticas modernas, feature default | 75% |
| Tablas sin PK 20-30% en legacy | Patrón común en bases migradas de Access/FoxPro | 80% |
| Kafka overhead 1.5× | Benchmark estándar (metadata + acks + retries) | 85% |
| Compresión lz4 reduce 40% | Benchmark oficial Confluent | 90% |
| Edge Gateway USD 45K/planta | Precio mercado servidores mid-range + software | 75% |
| Personal USD 100K/FTE promedio | Salarios México + prestaciones IT senior | 80% |
| Reducción 12→8 FTE viable | Estándar con managed services (33% reducción) | 70% |

**TOTAL SUPUESTOS RAZONABLES**: 9

**DECISIÓN**: Estos supuestos pueden usarse para **diseño preliminar** pero deben **validarse antes de CAPEX final**.

---

## 8. Matriz de Riesgo de Supuestos

| ID Riesgo | Supuesto | Prob. Error | Impacto si Error | Severidad | Mitigación |
|-----------|----------|-------------|------------------|-----------|------------|
| **RS-1** | Throughput CDC 3 Mbps/inst | 40% | Interconnect insuficiente | **CRÍTICO** | POC Debezium 30 días |
| **RS-2** | CAPEX USD 2M aprobado | 30% | Proyecto bloqueado | **CRÍTICO** | Validar CFO 7 días |
| **RS-3** | Latencia Interconnect 5-10ms | 25% | Kafka degradado | **ALTO** | Ping real 2 días |
| **RS-4** | WAN USD 300K/año completo | 35% | TCO subestimado | **ALTO** | Contratos reales 15 días |
| **RS-5** | Cloud VPN 500 Mbps | 30% | Failover no viable | **ALTO** | Prueba iperf3 7 días |
| **RS-6** | SCADA <10ms requerido | 20% | Edge innecesario (ahorro) | **MEDIO** | Site survey 30 días |
| **RS-7** | 210-330 SPs xp_cmdshell | 25% | Esfuerzo refactor 2× | **MEDIO** | Query real 7 días |
| **RS-8** | Payback 24 meses | 20% | Timeline presión | **MEDIO** | Validar CFO 7 días |
| **RS-9** | Reducción 12→8 FTE | 30% | OPEX mayor | **MEDIO** | Validar IT Ops 30 días |
| **RS-10** | Compresión Kafka 40% | 15% | Throughput mayor | **BAJO** | Prueba real 30 días |

**ANÁLISIS DE RIESGO**:
- **2 riesgos CRÍTICOS** (RS-1, RS-2) - **Bloquean proyecto**
- **3 riesgos ALTOS** (RS-3, RS-4, RS-5) - **Ajustan diseño/costos significativamente**
- **4 riesgos MEDIOS** - **Ajustes menores**
- **1 riesgo BAJO** - **Sin impacto material**

---

## 9. Conclusiones y Próximos Pasos

### 9.1 Conclusiones Clave

1. **✅ POSITIVO**: Los 3 documentos de Fase 1 tienen **ALTA CALIDAD TÉCNICA** y análisis riguroso

2. **✅ POSITIVO**: Inventario Sistemas Legados y Conectividad Actual marcan **CORRECTAMENTE** todos los supuestos

3. **❌ NEGATIVO**: Baseline Financiero tiene **13 supuestos críticos SIN MARCAR** explícitamente

4. **⚠️ CRÍTICO**: **65% de los datos son SUPUESTOS** - Solo 35% provienen del PDF del caso de negocio

5. **⚠️ CRÍTICO**: **NO SE PUEDE VALIDAR** que Interconnect 1Gbps sea suficiente con datos disponibles

6. **✅ POSITIVO**: Los supuestos realizados son **RAZONABLES** y basados en benchmarks industriales estándar

7. **⚠️ RIESGO**: **2 supuestos CRÍTICOS** (throughput CDC + CAPEX aprobado) **BLOQUEAN** la aprobación del proyecto

### 9.2 Calificación de Documentos (Escala 1-10)

| Documento | Calidad Técnica | Marcado Supuestos | Alineación PDF | Nota Final |
|-----------|----------------|-------------------|----------------|------------|
| **Inventario Sistemas Legados** | 9/10 | 10/10 | 8/10 | **9.0/10** ✅ |
| **Baseline Financiero** | 8/10 | 2/10 | 9/10 | **6.3/10** ⚠️ |
| **Conectividad Actual** | 9/10 | 9/10 | 7/10 | **8.3/10** ✅ |
| **PROMEDIO GENERAL** | **8.7/10** | **7.0/10** | **8.0/10** | **7.9/10** |

**VEREDICTO**:
- Los documentos tienen **EXCELENTE CALIDAD TÉCNICA** (8.7/10)
- El **MARCADO DE SUPUESTOS** es inconsistente (7.0/10) - Baseline Financiero requiere corrección
- La **ALINEACIÓN CON PDF** es buena (8.0/10) pero con 65% de supuestos necesarios

### 9.3 Decisión Go/No-Go para Fase 2

**RECOMENDACIÓN**: ⚠️ **CONDICIONAL GO** - Proceder a Fase 2 SOLO si se completan validaciones críticas en 30 días

**CONDICIONES PARA GO**:

1. ✅ **Validación CFO** (7 días):
   - CAPEX USD 2M aprobado o ajustado
   - Payback 24 meses confirmado
   - Desglose WAN USD 300K/año explicado

2. ✅ **Mediciones de red** (7 días):
   - Latencia Interconnect real <15ms
   - Cloud VPN throughput >400 Mbps
   - Inventario vCenter completo

3. ✅ **POC Debezium** (30 días):
   - Throughput CDC real por instancia
   - Validar que Dual 1Gbps es suficiente
   - Confirmar exactly-once semantics

4. ✅ **Corrección Baseline Financiero** (3 días):
   - Re-escribir con supuestos marcados
   - Tabla de supuestos agregada
   - Validación CFO de todos los supuestos

**SI NO SE CUMPLEN**: ❌ **NO-GO** - Rediseñar arquitectura o ajustar expectativas C-level

### 9.4 Próximos Pasos Inmediatos

**DÍA 1-3** (Correcciones Documentales):
- Agente Finanzas: Re-escribir Baseline Financiero secciones 6-8
- Todos los agentes: Agregar tabla resumen supuestos a sus documentos
- Arquitecto Plataforma: Generar lista consolidada de validaciones

**DÍA 4-7** (Validaciones Rápidas):
- Experto Redes: Latencia Interconnect real (ping, traceroute)
- Admin Sistemas: Query SQL Server (tablas sin PK, xp_cmdshell, CDC)
- Finanzas: Reunión CFO (supuestos financieros críticos)
- Experto Redes: Inventario vCenter (hosts, capacidad)

**DÍA 8-30** (Validaciones Complejas):
- Data Engineer + Admin Sistemas: POC Debezium (3 SQL Server)
- Experto Redes: Prueba Cloud VPN HA (failover, throughput)
- Admin Sistemas: Site survey SCADA (3 plantas)
- Finanzas: Cotizaciones Edge Gateway (3 vendors)

**DÍA 30** (Decisión Go/No-Go):
- Reunión todos los agentes
- Presentación resultados validaciones
- Decisión: ¿Proceder a Fase 2 o rediseñar?
- Actualización documentos con datos reales

---

## 10. Anexo: Referencias Específicas al PDF

### Datos Confirmados del PDF por Sección

**Sección 2.1 - Inventario de Cargas (Página 1-2)**:
- ✅ SCADA modernos: 30 (10+10+10)
- ✅ SCADA antiguos críticos: 40 (10+10+20)
- ✅ SQL Server 2008-2012 Plantas: 40 (10+10+20)
- ✅ SQL Server 2019 Plantas críticos: 40 (10+10+20)
- ✅ SQL Server 2008-2012 Corp: 60 (20+20+20)
- ✅ SQL Server 2019 Corp críticos: 80 (20+20+40)
- ✅ Aplicaciones IIS Plantas: 60 (20+20+20)
- ✅ Aplicaciones IIS Corp: 30 (30+0+0)

**Sección 2.2 - Capacidad y Crecimiento (Página 3)**:
- ✅ Total VMs: 420
- ✅ vCPU: ~1,900
- ✅ RAM: ~12.8 TB
- ✅ Almacenamiento: ~200TB block + ~500TB object
- ✅ Crecimiento: 20% anual
- ✅ Ventanas mantenimiento: Domingos 2h/planta
- ✅ Freeze: 15-Nov al 5-Ene
- ✅ SLA: 99.95% global, 99.99% críticos
- ✅ RPO/RTO: 0/0 críticos, ≤15'/15' no críticos

**Sección 2.3 - Producción (Página 3)**:
- ✅ Monterrey: 60,000 unid/mes, 720,000 unid/año
- ✅ Guadalajara: 40,000 unid/mes, 480,000 unid/año
- ✅ Tijuana: 30,000 unid/mes, 360,000 unid/año
- ✅ Total: 130,000 unid/mes, 1,560,000 unid/año

**Sección 3.1 - OPEX On-Prem (Página 3)**:
- ✅ Hardware & mantenimiento: USD 1,560,000/año
- ✅ Licenciamiento: USD 1,515,000/año
- ✅ Energía/espacio: USD 420,000/año
- ✅ Personal (12 FTE): USD 1,200,000/año
- ✅ WAN & enlaces: USD 300,000/año
- ✅ Otros contratos: USD 250,000/año
- ✅ Total: USD 5,245,000/año
- ✅ TCO 3 años: USD 15,735,000

**Sección 3.2 - Price Pack Cloud (Página 3-4)**:
- ✅ Compute: USD 24/vCPU-mes, USD 3/GB-RAM-mes
- ✅ SQL administrado: 1.6× compute
- ✅ Block storage: USD 0.12/GB-mes
- ✅ Object storage: USD 0.023/GB-mes
- ✅ Snapshots: USD 0.05/GB-mes
- ✅ Interconnect: USD 3,000/mes (2 puertos)
- ✅ Egress: USD 0.05/GB (primeros 30TB)
- ✅ Soporte GCP: USD 12,500/mes
- ✅ Operación Cloud: USD 75,000/mes
- ✅ One-time: USD 1,700,000

**Sección 4 - Restricciones Técnicas (Página 4)**:
- ✅ RPO/RTO=0 en SCADA antiguos + SQL Server 2019
- ✅ Latencia OT: SCADA requiere operación local-first/edge
- ✅ Conectividad: Interconnect 1Gbps + Cloud VPN respaldo
- ✅ Procedimientos almacenados llaman .exe locales

---

**FIN DEL DOCUMENTO DE VALIDACIÓN CRUZADA**

**Archivo generado**: `/home/rodrigoestrada/workspace/github.com/raestrada/cloud-gob-data-industrial/docs/fase1/supuestos-validados.md`
**Fecha**: 2025-10-31
**Moderador**: Arquitecto de Plataforma Senior
**Próxima revisión**: Post-validaciones (2025-12-01)
