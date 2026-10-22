import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "finanzas.db"


def get_connection():
    DATA_DIR.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla categorías
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id_categoria INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE,
            tipo TEXT NOT NULL CHECK(tipo IN ('ingreso', 'gasto'))
        )
    """)

    # Tabla movimientos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS movimientos (
            id_movimiento INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            cantidad REAL NOT NULL CHECK(cantidad >= 0),
            descripcion TEXT,
            id_categoria INTEGER NOT NULL,
            FOREIGN KEY (id_categoria)
                REFERENCES categorias(id_categoria)
                ON DELETE RESTRICT
                ON UPDATE CASCADE
        )
    """)

    # Índice
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_movimientos_fecha
        ON movimientos(fecha)
    """)

    # Categorías iniciales
    categorias = [
        ("Salario", "ingreso"),
        ("Ventas", "ingreso"),
        ("Comida", "gasto"),
        ("Transporte", "gasto"),
        ("Vivienda", "gasto"),
        ("Ocio", "gasto"),
        ("Salud", "gasto"),
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO categorias (nombre, tipo)
        VALUES (?, ?)
    """, categorias)

    conn.commit()
    conn.close()