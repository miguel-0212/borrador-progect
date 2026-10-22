from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

from services.resumen_service import obtener_resumen
from services.movimiento_service import listar_movimientos


def generar_pdf(ruta="informe_financiero.pdf"):
    # Crear documento PDF
    doc = SimpleDocTemplate(ruta, pagesize=A4)
    elementos = []

    # Estilos
    estilos = getSampleStyleSheet()

    # Título
    elementos.append(
        Paragraph("Informe Financiero Personal", estilos["Title"])
    )
    elementos.append(Spacer(1, 12))

    # Fecha de generación
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M")
    elementos.append(
        Paragraph(
            f"Fecha de generación: {fecha_actual}",
            estilos["Normal"]
        )
    )
    elementos.append(Spacer(1, 12))

    # Resumen financiero
    resumen = obtener_resumen()
    elementos.append(
        Paragraph(
            f"Ingresos: {resumen['ingresos']:.2f} €<br/>"
            f"Gastos: {resumen['gastos']:.2f} €<br/>"
            f"Balance: {resumen['balance']:.2f} €",
            estilos["Normal"]
        )
    )
    elementos.append(Spacer(1, 20))

    # Obtener movimientos
    movimientos = listar_movimientos()

    # Cabecera de tabla
    datos = [[
        "Fecha",
        "Tipo",
        "Categoría",
        "Cantidad",
        "Descripción"
    ]]

    # Añadir filas
    for _, fecha, cantidad, descripcion, categoria, tipo in movimientos:
        datos.append([
            fecha,
            tipo,
            categoria,
            f"{cantidad:.2f} €",
            descripcion or ""
        ])

    # Crear tabla
    tabla = Table(
        datos,
        colWidths=[70, 60, 90, 70, 180]
    )

    # Estilo de tabla
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        (
            "ROWBACKGROUNDS",
            (0, 1),
            (-1, -1),
            [colors.white, colors.whitesmoke]
        ),
    ]))

    elementos.append(tabla)

    # Generar PDF
    doc.build(elementos)

    return ruta