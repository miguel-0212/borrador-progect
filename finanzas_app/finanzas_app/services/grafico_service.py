from database.db import get_connection


def obtener_gastos_por_categoria():
    """
    Devuelve una lista de tuplas:
    [(categoria, total_gastado), ...]
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            c.nombre,
            SUM(m.cantidad) AS total
        FROM movimientos m
        JOIN categorias c
            ON m.id_categoria = c.id_categoria
        WHERE c.tipo = 'gasto'
        GROUP BY c.nombre
        ORDER BY total DESC
    """)

    resultados = cursor.fetchall()
    conn.close()

    return resultados