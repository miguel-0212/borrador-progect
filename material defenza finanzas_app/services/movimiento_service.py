from datetime import datetime
from database.db import get_connection


def validar_fecha(fecha):
    try:
        datetime.strptime(fecha, "%Y-%m-%d")
    except ValueError:
        raise ValueError("La fecha debe tener formato YYYY-MM-DD.")


def validar_cantidad(cantidad):
    try:
        cantidad = float(cantidad)
    except ValueError:
        raise ValueError("La cantidad debe ser numérica.")

    if cantidad < 0:
        raise ValueError("La cantidad no puede ser negativa.")

    return cantidad


def registrar_movimiento(fecha, cantidad, descripcion, id_categoria):
    validar_fecha(fecha)
    cantidad = validar_cantidad(cantidad)
    descripcion = descripcion.strip()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO movimientos
            (fecha, cantidad, descripcion, id_categoria)
            VALUES (?, ?, ?, ?)
        """, (fecha, cantidad, descripcion, id_categoria))

        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        conn.rollback()
        raise ValueError(f"No se pudo registrar el movimiento: {e}")

    finally:
        conn.close()


def listar_movimientos(mes=None, id_categoria=None, tipo=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT
            m.id_movimiento,
            m.fecha,
            m.cantidad,
            m.descripcion,
            c.nombre AS categoria,
            c.tipo
        FROM movimientos m
        JOIN categorias c
            ON m.id_categoria = c.id_categoria
        WHERE 1=1
    """

    params = []

    if mes:
        query += " AND strftime('%Y-%m', m.fecha) = ?"
        params.append(mes)

    if id_categoria:
        query += " AND m.id_categoria = ?"
        params.append(id_categoria)

    if tipo and tipo in ("ingreso", "gasto"):
        query += " AND c.tipo = ?"
        params.append(tipo)

    query += " ORDER BY m.fecha DESC, m.id_movimiento DESC"

    cursor.execute(query, params)
    movimientos = cursor.fetchall()

    conn.close()
    return movimientos


def obtener_movimiento(id_movimiento):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_movimiento, fecha, cantidad, descripcion, id_categoria
        FROM movimientos
        WHERE id_movimiento = ?
    """, (id_movimiento,))

    movimiento = cursor.fetchone()
    conn.close()
    return movimiento


def actualizar_movimiento(id_movimiento, fecha, cantidad, descripcion, id_categoria):
    validar_fecha(fecha)
    cantidad = validar_cantidad(cantidad)
    descripcion = descripcion.strip()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE movimientos
        SET fecha = ?, cantidad = ?, descripcion = ?, id_categoria = ?
        WHERE id_movimiento = ?
    """, (fecha, cantidad, descripcion, id_categoria, id_movimiento))

    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()

    return actualizado


def eliminar_movimiento(id_movimiento):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM movimientos
        WHERE id_movimiento = ?
    """, (id_movimiento,))

    eliminado = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return eliminado