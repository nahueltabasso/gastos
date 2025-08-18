# APP PARA CONTROL DE GASTOS DE CONSTRUCCIÓN

Aplicación de escritorio para gestionar y visualizar los gastos de una obra de remodelación, desarrollada en Python con Tkinter y SQLAlchemy.

## Características principales

- Visualización de la lista de gastos en una tabla interactiva.
- Panel de totales acumulados (Pesos, USD Oficial, USD MEP).
- Formulario para agregar nuevos gastos (Descripción, Fecha, Total Pesos, Titular).
- Eliminación de gastos con confirmación.
- Interfaz moderna con pestañas y diseño amigable.

## Requisitos

- Python 3.12+
- Tkinter (incluido en la mayoría de instalaciones de Python)
- SQLAlchemy
- pymysql
- pandas
- requests
- python-dotenv
- pydantic-settings

Instala las dependencias con:

```bash
pip install -r requirements.txt
```

O usando pipenv:

```bash
pipenv install
```

## Estructura del proyecto

```text
├── src/
│   ├── ui.py           # Interfaz gráfica principal
│   ├── crud.py         # Funciones de acceso y manipulación de datos
│   ├── models.py       # Modelos de datos SQLAlchemy
│   ├── database.py     # Configuración de la base de datos
│   ├── dolar_service.py# Servicio para obtener cotizaciones de dólar
│   └── ...
├── data/               # Archivos de datos de ejemplo
│   ├── gastos.json
│   ├── gastos.csv
│   └── gastos_1.json
├── requirements.txt
├── Pipfile
├── README.md
```

## Cómo ejecutar

1. Configura la base de datos en `src/database.py` según tus credenciales.
2. Ejecuta la interfaz gráfica:

```bash
python src/ui.py
```

## Uso

- **Agregar gasto:** Haz clic en "Agregar Gasto" y completa el formulario.
- **Eliminar gasto:** Haz doble clic en una fila y confirma la eliminación.
- **Visualizar totales:** Los totales se actualizan automáticamente al agregar o eliminar gastos.

## Autor

Nahuel Tabasso

