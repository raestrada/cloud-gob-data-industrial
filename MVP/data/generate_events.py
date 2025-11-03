#!/usr/bin/env python3
"""
Generador de eventos sintéticos que simulan mensajes de Kafka.

Este script transforma los datos históricos del CSV a formato de eventos Kafka,
manteniendo la MISMA granularidad y valores que el CSV original.

Eventos generados:
- billing.cost.monthly: Eventos mensuales por servicio (60 eventos = 12 meses × 5 servicios)
"""

import json
import csv
from datetime import datetime
from typing import Dict, List

# Configuración base
PROJECTS = ["prod-monterrey-scada", "prod-guadalajara-scada", "prod-tijuana-scada"]

SERVICES_CONFIG = {
    "compute": {
        "csv_column": "compute_usd",
        "sku": "n2-standard-fleet",
        "usage_unit": "vCPU-hours"
    },
    "storage": {
        "csv_column": "storage_usd",
        "sku": "pd-ssd-fleet",
        "usage_unit": "GB-hours"
    },
    "network": {
        "csv_column": "network_usd",
        "sku": "interconnect-fleet",
        "usage_unit": "GB"
    },
    "support": {
        "csv_column": "support_usd",
        "sku": "premium-support",
        "usage_unit": "hours"
    },
    "operation": {
        "csv_column": "operation_usd",
        "sku": "monitoring-logging-fleet",
        "usage_unit": "API-calls"
    }
}


def read_historical_csv(filename: str) -> List[Dict]:
    """Lee el CSV histórico y retorna lista de registros mensuales."""
    data = []
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data


def generate_billing_events(csv_file: str, output_file: str):
    """
    Genera eventos de billing que simulan topic: billing.cost.monthly

    Convierte cada fila del CSV en eventos mensuales, uno por servicio.
    12 meses × 5 servicios = 60 eventos totales

    Mantiene EXACTAMENTE los mismos valores del CSV, solo cambia el formato.
    """
    historical_data = read_historical_csv(csv_file)
    events = []

    for row in historical_data:
        month_str = row['month']  # Formato: M1, M2, etc.
        month_num = int(month_str.replace('M', ''))

        # Fecha del mes (primer día)
        year = 2025
        timestamp = datetime(year, month_num, 1)

        # Generar un evento por cada servicio con su costo del CSV
        for service, config in SERVICES_CONFIG.items():
            cost = float(row[config['csv_column']])

            # Calcular usage_amount estimado basado en costo
            # (en un caso real vendría en el evento, aquí lo derivamos)
            usage_multiplier = {
                "compute": 720,      # horas vCPU/mes
                "storage": 1000,     # GB-hours/mes
                "network": 100,      # GB/mes
                "support": 730,      # hours/mes
                "operation": 1000000 # API calls/mes
            }
            usage_amount = round(cost * usage_multiplier.get(service, 100) / 100, 2)

            event = {
                "timestamp": timestamp.isoformat() + "Z",
                "period": "monthly",
                "month": month_str,
                "project_id": "prod-industrial-fleet",  # Proyecto consolidado
                "service": service,
                "sku": config['sku'],
                "resource_name": f"{service}-{config['sku']}-{timestamp.strftime('%Y%m%d')}",
                "cost_usd": cost,
                "usage_amount": usage_amount,
                "usage_unit": config['usage_unit'],
                "production_units": int(row['production_units']),
                "labels": {
                    "env": "prod",
                    "business_unit": "industrial-operations",
                    "cost_center": "CC-1000"
                }
            }

            events.append(event)

    # Guardar eventos en JSONL
    with open(output_file, 'w') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')

    print(f"✅ Generados {len(events)} eventos de billing en {output_file}")

    # Verificar que los totales coinciden
    total_csv = sum(float(row['total_usd']) for row in historical_data)
    total_events = sum(e['cost_usd'] for e in events)

    print(f"   Total CSV:     ${total_csv:,.2f}")
    print(f"   Total eventos: ${total_events:,.2f}")
    print(f"   Diferencia:    ${abs(total_csv - total_events):,.2f}")

    return len(events)


def generate_production_metrics_events(csv_file: str, output_file: str):
    """
    Genera eventos de métricas de producción (unidades producidas por mes).

    12 eventos = 12 meses
    """
    historical_data = read_historical_csv(csv_file)
    events = []

    for row in historical_data:
        month_str = row['month']
        month_num = int(month_str.replace('M', ''))

        year = 2025
        timestamp = datetime(year, month_num, 1)

        event = {
            "timestamp": timestamp.isoformat() + "Z",
            "period": "monthly",
            "month": month_str,
            "production_units": int(row['production_units']),
            "total_cost_usd": float(row['total_usd']),
            "cost_per_unit": round(float(row['total_usd']) / int(row['production_units']), 4),
            "labels": {
                "business_unit": "industrial-operations"
            }
        }

        events.append(event)

    with open(output_file, 'w') as f:
        for event in events:
            f.write(json.dumps(event) + '\n')

    print(f"✅ Generados {len(events)} eventos de producción en {output_file}")
    return len(events)


if __name__ == "__main__":
    print("Generando eventos Kafka desde datos históricos CSV...\n")
    print("Estrategia: Mantener la MISMA granularidad del CSV (mensual)")
    print("           Solo transformar el formato: CSV → eventos JSONL\n")

    billing_count = generate_billing_events("historical_costs.csv", "kafka_events_billing.jsonl")
    production_count = generate_production_metrics_events("historical_costs.csv", "kafka_events_production.jsonl")

    print(f"\n📊 Resumen:")
    print(f"   - Eventos de billing (mensuales por servicio): {billing_count}")
    print(f"   - Eventos de producción (mensuales): {production_count}")
    print(f"   - Total: {billing_count + production_count}")
    print(f"\n✨ Los eventos mantienen EXACTAMENTE los mismos datos del CSV.")
    print(f"   Solo cambia el formato para simular mensajes de Kafka.")
