"""
Seed script: inserta portafolios y favoritos de prueba en MySQL (MS1).

Uso:
    pip install pymysql python-dotenv
    python seed_data.py

Variables de entorno (.env o shell):
    DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
"""

import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pymysql

load_dotenv()

DB_CONFIG = {
    "host":   os.getenv("DB_HOST", "localhost"),
    "port":   int(os.getenv("DB_PORT", 3306)),
    "user":   os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "portafolio_db"),
    "charset": "utf8mb4",
}

PORTAFOLIOS = [
    ("Tech Giants",    "Portafolio enfocado en las grandes tecnológicas del NASDAQ"),
    ("Energía Verde",  "Acciones relacionadas con energías renovables y ESG"),
    ("Dividendos",     "Empresas con historial sólido de pago de dividendos"),
    ("Crecimiento",    "Startups y empresas de alto crecimiento"),
    ("Defensivo",      "Valores defensivos ante recesiones"),
]

# simbolo → nombre empresa
ACCIONES = {
    "AAPL":  "Apple Inc.",
    "NVDA":  "NVIDIA Corporation",
    "MSFT":  "Microsoft Corporation",
    "GOOGL": "Alphabet Inc.",
    "TSLA":  "Tesla Inc.",
    "AMZN":  "Amazon.com Inc.",
    "META":  "Meta Platforms Inc.",
    "JPM":   "JPMorgan Chase & Co.",
    "V":     "Visa Inc.",
    "JNJ":   "Johnson & Johnson",
    "XOM":   "Exxon Mobil Corporation",
    "WMT":   "Walmart Inc.",
    "NFLX":  "Netflix Inc.",
    "PYPL":  "PayPal Holdings Inc.",
    "AMD":   "Advanced Micro Devices Inc.",
}

ACCIONES_LIST = list(ACCIONES.items())

# Catálogo de nombres para generación masiva
NOMBRES = ["Alejandro", "Maria", "Juan", "Sofia", "Carlos", "Laura", "Diego", "Lucia", "Gabriel", "Valentina", "Mateo", "Camila", "Nicolas", "Isabella", "Andres", "Martina", "Sebastian", "Elena", "Lucas", "Victoria"]
TIPOS = ["Inversión a Largo Plazo", "Trading Diario", "Dividendos Mensuales", "Acciones Tech", "Crecimiento Agresivo", "Retiro Seguro", "Estrategia Quant", "Momentum", "Value Investing", "Penny Stocks"]

def seed():
    print("Conectando a MySQL...")
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Resetear tablas con esquema limpio
    cur.execute("SET FOREIGN_KEY_CHECKS=0")
    cur.execute("DROP TABLE IF EXISTS favoritos")
    cur.execute("DROP TABLE IF EXISTS portafolios")
    cur.execute("SET FOREIGN_KEY_CHECKS=1")
    cur.execute("""
        CREATE TABLE portafolios (
            id          INT AUTO_INCREMENT PRIMARY KEY,
            nombre      VARCHAR(100) NOT NULL,
            descripcion VARCHAR(255),
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cur.execute("""
        CREATE TABLE favoritos (
            id              INT AUTO_INCREMENT PRIMARY KEY,
            portafolio_id   INT NOT NULL,
            simbolo         VARCHAR(10) NOT NULL,
            nombreEmpresa   VARCHAR(120),
            added_at        DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE KEY unique_portfolio_stock (portafolio_id, simbolo),
            FOREIGN KEY (portafolio_id) REFERENCES portafolios(id) ON DELETE CASCADE
        )
    """)
    conn.commit()

    # --- GENERACIÓN MASIVA DE PORTAFOLIOS (2,000) ---
    print("Generando 2,000 portafolios...")
    portfolios_data = []
    base_date = datetime(2024, 1, 1)
    
    for i in range(2000):
        nombre = f"Portafolio de {random.choice(NOMBRES)} - {random.choice(TIPOS)} #{i+1}"
        desc = f"Estrategia personalizada generada automáticamente para el perfil {i+1}."
        created = base_date + timedelta(minutes=i * 10)
        portfolios_data.append((nombre, desc, created))

    cur.executemany(
        "INSERT INTO portafolios (nombre, descripcion, created_at) VALUES (%s, %s, %s)",
        portfolios_data
    )
    conn.commit()
    
    # Obtener todos los IDs insertados
    cur.execute("SELECT id FROM portafolios")
    portfolio_ids = [row[0] for row in cur.fetchall()]
    print(f"  {len(portfolio_ids)} portafolios insertados ✓")

    # --- GENERACIÓN MASIVA DE FAVORITOS (~20,000) ---
    print("Generando 20,000 favoritos (10 por portafolio)...")
    favoritos_data = []
    fav_count = 0
    
    for pid in portfolio_ids:
        # 10 acciones fijas por portafolio para asegurar el conteo exacto
        seleccion = random.sample(ACCIONES_LIST, k=10)
        for simbolo, empresa in seleccion:
            added = base_date + timedelta(days=random.randint(1, 120))
            favoritos_data.append((pid, simbolo, empresa, added))
            fav_count += 1
            
            # Insertar en lotes de 5000 para no saturar la memoria
            if len(favoritos_data) >= 5000:
                cur.executemany(
                    "INSERT INTO favoritos (portafolio_id, simbolo, nombreEmpresa, added_at) VALUES (%s, %s, %s, %s)",
                    favoritos_data
                )
                conn.commit()
                favoritos_data = []

    # Insertar remanente
    if favoritos_data:
        cur.executemany(
            "INSERT INTO favoritos (portafolio_id, simbolo, nombreEmpresa, added_at) VALUES (%s, %s, %s, %s)",
            favoritos_data
        )
        conn.commit()

    print(f"  {fav_count} favoritos insertados ✓")

    cur.close()
    conn.close()
    print("\nSeed MS1 completado con éxito para la rúbrica (20,000+ registros) ✓")


if __name__ == "__main__":
    seed()
