# Arquitectura Hub and Spoke

## Principio General de Diseño

La arquitectura de la plataforma de datos se basará en un modelo **Hub and Spoke**.

- **Hub (Centro):** La infraestructura en **Google Cloud Platform (GCP)** actuará como el hub central. Será el punto de consolidación de datos de todas las plantas. Sus responsabilidades clave son:
    - **Centralización de Datos:** Almacenar y procesar datos provenientes de múltiples spokes.
    - **Resiliencia:** Asegurar la alta disponibilidad y recuperación ante desastres de los datos críticos.
    - **Procesamiento Avanzado:** Ejecutar análisis de datos que involucren información de más de una planta, generando insights globales.

- **Spokes (Radios):** Cada una de las **plantas industriales** (Monterrey, Guadalajara, Tijuana) funcionará como un spoke. Sus responsabilidades son:
    - **Captura de Datos en Origen:** Recolectar datos de los sistemas locales (SCADA, SQL Server, etc.).
    - **Procesamiento en el Borde (Edge):** Realizar el procesamiento inicial y filtrado si es necesario.
    - **Envío de Datos al Hub:** Transmitir los datos de forma segura y eficiente al hub en GCP.
