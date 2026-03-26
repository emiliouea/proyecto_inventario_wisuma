from io import BytesIO
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generar_reporte_productos(productos):
    """Genera un PDF con el listado de productos del inventario."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('titulo', parent=styles['Title'],
                                  alignment=TA_CENTER, fontSize=16, spaceAfter=6)
    sub_style = ParagraphStyle('sub', parent=styles['Normal'],
                               alignment=TA_CENTER, fontSize=10, spaceAfter=12, textColor=colors.grey)

    elementos = []
    elementos.append(Paragraph("Ferretería Senguana", titulo_style))
    elementos.append(Paragraph("Reporte de Inventario de Productos", sub_style))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", sub_style))
    elementos.append(Spacer(1, 0.5*cm))

    # Encabezados
    data = [["#", "Nombre", "Categoría", "Precio ($)", "Stock", "Descripción"]]
    for p in productos:
        data.append([
            str(p.id),
            p.nombre,
            p.categoria,
            f"{p.precio:.2f}",
            str(p.stock),
            (p.descripcion or '')[:40]
        ])

    tabla = Table(data, colWidths=[1*cm, 4.5*cm, 3*cm, 2.5*cm, 2*cm, 4.5*cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (1, 1), (1, -1), 'LEFT'),
        ('ALIGN', (5, 1), (5, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 0.5*cm))

    # Totales
    valor_total = sum(p.precio * p.stock for p in productos)
    resumen_data = [
        ["Total de productos:", str(len(productos))],
        ["Valor total del inventario:", f"${valor_total:.2f}"]
    ]
    resumen = Table(resumen_data, colWidths=[6*cm, 4*cm])
    resumen.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(resumen)

    doc.build(elementos)
    buffer.seek(0)
    return buffer


def generar_reporte_facturas(facturas):
    """Genera un PDF con el listado de facturas."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            rightMargin=2*cm, leftMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle('titulo', parent=styles['Title'],
                                  alignment=TA_CENTER, fontSize=16, spaceAfter=6)
    sub_style = ParagraphStyle('sub', parent=styles['Normal'],
                               alignment=TA_CENTER, fontSize=10, spaceAfter=12, textColor=colors.grey)

    elementos = []
    elementos.append(Paragraph("Ferretería Senguana", titulo_style))
    elementos.append(Paragraph("Reporte de Facturas", sub_style))
    elementos.append(Paragraph(f"Generado: {datetime.now().strftime('%d/%m/%Y %H:%M')}", sub_style))
    elementos.append(Spacer(1, 0.5*cm))

    data = [["#", "Fecha", "Cliente", "Estado", "Total ($)"]]
    for f in facturas:
        data.append([
            str(f.id),
            f.fecha.strftime('%d/%m/%Y') if f.fecha else '',
            f.cliente.nombre if f.cliente else '',
            f.estado,
            f"{f.total:.2f}"
        ])

    tabla = Table(data, colWidths=[1.5*cm, 3.5*cm, 5*cm, 3*cm, 3*cm])
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0d6efd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (2, 1), (2, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f0f4ff')]),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elementos.append(tabla)
    elementos.append(Spacer(1, 0.5*cm))

    total_general = sum(f.total for f in facturas)
    resumen_data = [
        ["Total de facturas:", str(len(facturas))],
        ["Monto total:", f"${total_general:.2f}"]
    ]
    resumen = Table(resumen_data, colWidths=[6*cm, 4*cm])
    resumen.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
    ]))
    elementos.append(resumen)

    doc.build(elementos)
    buffer.seek(0)
    return buffer
