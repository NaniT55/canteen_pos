from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_LEFT
from reportlab.lib import colors
from datetime import datetime


def generate_customer_bill(
    filename,
    customer_name,
    customer_type,
    room_number,
    orders
):
    # ---------- DOCUMENT ----------
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=30,
        rightMargin=30,
        topMargin=30,
        bottomMargin=30
    )

    styles = getSampleStyleSheet()

    # ---------- CUSTOM STYLES ----------
    left_style = ParagraphStyle(
        name="Left",
        parent=styles["Normal"],
        alignment=TA_LEFT,
        fontSize=9
    )

    right_style = ParagraphStyle(
        name="Right",
        parent=styles["Normal"],
        alignment=TA_RIGHT,
        fontSize=9
    )

    header_style = ParagraphStyle(
        name="Header",
        parent=styles["Normal"],
        alignment=TA_LEFT,
        fontSize=9,
        fontName="Helvetica-Bold"
    )

    title_style = ParagraphStyle(
        name="Title",
        parent=styles["Title"],
        alignment=TA_LEFT
    )

    elements = []

    # ---------- HEADER ----------
    elements.append(Paragraph("Hospital Canteen", title_style))
    elements.append(Spacer(1, 8))

    elements.append(
        Paragraph(
            f"<b>Customer:</b> {customer_name} ({customer_type})",
            styles["Normal"]
        )
    )

    if room_number:
        elements.append(
            Paragraph(
                f"<b>Room:</b> {room_number}",
                styles["Normal"]
            )
        )

    elements.append(
        Paragraph(
            f"<b>Bill Generated:</b> {datetime.now().strftime('%d %b %Y, %I:%M %p')}",
            styles["Normal"]
        )
    )

    elements.append(Spacer(1, 14))

    # ---------- TABLE HEADER ----------
    table_data = [[
        Paragraph("Date", header_style),
        Paragraph("Items", header_style),
        Paragraph("Total (₹)", header_style),
        Paragraph("Paid (₹)", header_style),
        Paragraph("Balance (₹)", header_style),
    ]]

    grand_total = 0
    grand_paid = 0
    grand_balance = 0

    # ---------- TABLE ROWS ----------
    for o in orders:
        # Convert ISO timestamp → readable
        dt = datetime.fromisoformat(o["date"])
        readable_date = dt.strftime("%d %b %Y, %I:%M %p")

        table_data.append([
            Paragraph(readable_date, left_style),
            Paragraph(o["items"], left_style),
            Paragraph(f"{o['total']:.2f}", right_style),
            Paragraph(f"{o['paid']:.2f}", right_style),
            Paragraph(f"{o['balance']:.2f}", right_style),
        ])

        grand_total += o["total"]
        grand_paid += o["paid"]
        grand_balance += o["balance"]

    # ---------- TOTAL ROW ----------
    table_data.append([
        Paragraph("<b>TOTAL</b>", header_style),
        Paragraph("", header_style),
        Paragraph(f"<b>{grand_total:.2f}</b>", right_style),
        Paragraph(f"<b>{grand_paid:.2f}</b>", right_style),
        Paragraph(f"<b>{grand_balance:.2f}</b>", right_style),
    ])

    # ---------- TABLE ----------
    table = Table(
        table_data,
        colWidths=[95, 215, 70, 70, 70],
        repeatRows=1
    )

    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 0.8, colors.black),

        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("BACKGROUND", (0,-1), (-1,-1), colors.whitesmoke),

        ("VALIGN", (0,0), (-1,-1), "TOP"),

        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),

        ("LINEABOVE", (0,-1), (-1,-1), 1.5, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 18))

    elements.append(
        Paragraph(
            "Thank you for your visit!",
            styles["Normal"]
        )
    )

    # ---------- BUILD PDF ----------
    doc.build(elements)
