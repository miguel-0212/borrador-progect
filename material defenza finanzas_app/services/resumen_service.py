from datetime import datetime
from database.db import get_connection


def obtener_resumen():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.tipo,
            SUM(m.cantidad)
        FROM movimientos m
        JOIN categorias c ON m.id_categoria = c.id_categoria
        GROUP BY c.tipo
    """)

    datos = dict(cursor.fetchall())

    ingresos = datos.get("ingreso", 0) or 0
    gastos = datos.get("gasto", 0) or 0
    balance = ingresos - gastos

    conn.close()

    return {
        "ingresos": float(ingresos),
        "gastos": float(gastos),
        "balance": float(balance)
    }


def obtener_resumen_mes_actual():
    conn = get_connection()
    cursor = conn.cursor()

    mes_actual = datetime.now().strftime("%Y-%m")

    cursor.execute("""
        SELECT
            c.tipo,
            SUM(m.cantidad)
        FROM movimientos m
        JOIN categorias c ON m.id_categoria = c.id_categoria
        WHERE m.fecha LIKE ?
        GROUP BY c.tipo
    """, (mes_actual + "%",))

    datos = dict(cursor.fetchall())

    ingresos = datos.get("ingreso", 0) or 0
    gastos = datos.get("gasto", 0) or 0
    balance = ingresos - gastos

    conn.close()

    return {
        "ingresos": float(ingresos),
        "gastos": float(gastos),
        "balance": float(balance)
    }