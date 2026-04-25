# MS1 - Gestion de Portafolios

Servicio encargado de administrar portafolios y simbolos favoritos de los usuarios en FinTrend.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-Database-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## Responsabilidad

- Crear, listar, actualizar y eliminar portafolios.
- Agregar y quitar simbolos favoritos dentro de cada portafolio.
- Exponer estado de salud del servicio y conexion a base de datos.

## Requisitos

- Python 3.11+
- MySQL
- pip

## Instalacion

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Edita `.env` con las credenciales reales de MySQL.

## Variables de entorno

```env
DB_HOST=localhost
DB_PORT=3306
DB_NAME=portafolio_db
DB_USER=root
DB_PASSWORD=your_mysql_password
SECRET_KEY=change-this-to-a-random-secret
```

## Ejecutar en desarrollo

```bash
python app/main.py
```

El servicio queda disponible en:

```text
http://localhost:5001
```

## Endpoints principales

| Metodo | Ruta | Descripcion |
| ------ | ---- | ----------- |
| GET | `/health` | Health check y conexion a DB |
| GET | `/api/portafolios/` | Lista portafolios |
| GET | `/api/portafolios/:id` | Obtiene un portafolio |
| POST | `/api/portafolios/` | Crea un portafolio |
| PUT | `/api/portafolios/:id` | Actualiza un portafolio |
| DELETE | `/api/portafolios/:id` | Elimina un portafolio |
| GET | `/api/favoritos/:portafolio_id` | Lista favoritos de un portafolio |
| POST | `/api/favoritos/:portafolio_id` | Agrega un simbolo favorito |
| DELETE | `/api/favoritos/:portafolio_id/:simbolo` | Elimina un favorito |

## Seed de datos

```bash
python seed_data.py
```

## Docker

```bash
docker build -t fintrend-ms1-portafolio .
docker run --env-file .env -p 5001:5001 fintrend-ms1-portafolio
```

## Estructura

```text
.
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── seed_data.py
├── requirements.txt
├── Dockerfile
└── .env.example
```
