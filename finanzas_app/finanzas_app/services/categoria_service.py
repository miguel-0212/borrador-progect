from database.db import get_connection


def listar_categorias():
    """Devuelve todas las categorías."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_categoria, nombre, tipo
        FROM categorias
        ORDER BY tipo, nombre
    """)

    categorias = cursor.fetchall()
    conn.close()
    return categorias


def listar_categorias_por_tipo(tipo):
    """Devuelve las categorías de tipo ingreso o gasto."""
    if tipo not in ("ingreso", "gasto"):
        raise ValueError("El tipo debe ser 'ingreso' o 'gasto'.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id_categoria, nombre, tipo
        FROM categorias
        WHERE tipo = ?
        ORDER BY nombre
    """, (tipo,))

    categorias = cursor.fetchall()
    conn.close()
    return categorias


def crear_categoria(nombre, tipo):
    """Crea una nueva categoría."""
    nombre = nombre.strip()

    if not nombre:
        raise ValueError("El nombre no puede estar vacío.")

    if tipo not in ("ingreso", "gasto"):
        raise ValueError("El tipo debe ser 'ingreso' o 'gasto'.")

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO categorias (nombre, tipo)
            VALUES (?, ?)
        """, (nombre, tipo))

        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        raise ValueError(f"No se pudo crear la categoría: {e}")

    finally:
        conn.close()


def eliminar_categoria(id_categoria):
    """Elimina una categoría por su ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM categorias
        WHERE id_categoria = ?
    """, (id_categoria,))

    eliminado = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return eliminado

def actualizar_categoria(id_categoria, nuevo_nombre, nuevo_tipo):
    """Actualiza el nombre y tipo de una categoría existente."""
    nuevo_nombre = nuevo_nombre.strip()

    if not nuevo_nombre:
        raise ValueError("El nombre no puede estar vacío.")
    if nuevo_tipo not in ("ingreso", "gasto"):
        raise ValueError("El tipo debe ser 'ingreso' o 'gasto'.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE categorias
        SET nombre = ?, tipo = ?
        WHERE id_categoria = ?
    """, (nuevo_nombre, nuevo_tipo, id_categoria))

    actualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()

    if not actualizado:
        raise ValueError("No se encontró la categoría para actualizar.")

    return actualizado