from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from datetime import datetime

LINE_WIDTH = 32


def sep():
    return "-" * LINE_WIDTH


def format_item(name, qty, amount):
    """
    LEFT  : Item name + qty (22 chars)
    RIGHT : Amount (10 chars)
    """
    left = f"{name} x{qty}"
    left = left[:22].ljust(22)
    right = f"{amount:.2f}".rjust(10)
    return left + right


def format_total(label, amount):
    left = label.ljust(22)
    right = f"{amount:.2f}".rjust(10)
    return left + right



def generate_thermal_receipt(
    filename,
    customer_name,
    customer_type,
    room_number,
    items,
    total,
    paid,
    balance
):
    doc = SimpleDocTemplate(
        filename,
        pagesize=(80 * mm, 200 * mm),
        leftMargin=6,
        rightMargin=6,
        topMargin=6,
        bottomMargin=6
    )

    center_style = ParagraphStyle(
        "center", alignment=TA_CENTER, fontSize=9, leading=11
    )

    left_style = ParagraphStyle(
        "left", alignment=TA_LEFT, fontSize=8, leading=10
    )

    bold_center = ParagraphStyle(
        "bold_center",
        alignment=TA_CENTER,
        fontSize=10,
        leading=12,
        fontName="Helvetica-Bold"
    )

    bold_left = ParagraphStyle(
        "bold_left",
        alignment=TA_LEFT,
        fontSize=8,
        leading=10,
        fontName="Helvetica-Bold"
    )

    elements = []

    # ---------- HEADER ----------
    elements.append(Paragraph("HOSPITAL CANTEEN", bold_center))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(sep(), center_style))

    elements.append(Paragraph(f"Customer : {customer_name}", left_style))
    elements.append(Paragraph(f"Type     : {customer_type}", left_style))

    if room_number:
        elements.append(Paragraph(f"Room     : {room_number}", left_style))

    elements.append(
        Paragraph(
            f"Date     : {datetime.now().strftime('%d %b %Y %I:%M %p')}",
            left_style
        )
    )

    elements.append(Paragraph(sep(), center_style))

    # ---------- COLUMN HEADER ----------
    elements.append(
        Paragraph(
            "Item".ljust(18) + "Qty".center(4) + "Amt".rjust(10),
            bold_left
        )
    )
    elements.append(Paragraph(sep(), center_style))

    # ---------- ITEMS ----------
    # ---------- ITEMS ----------
    for item in items:
        elements.append(
            Paragraph(
                format_item(
                    item["name"],
                    item["qty"],
                    item["qty"] * item["price"]
                ),
                left_style
            )
        )


    elements.append(Paragraph(sep(), center_style))

    # ---------- TOTALS ----------
    elements.append(Paragraph(format_total("TOTAL", total), bold_left))
    elements.append(Paragraph(format_total("PAID", paid), left_style))
    elements.append(Paragraph(format_total("BALANCE", balance), left_style))


    elements.append(Paragraph(sep(), center_style))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph("THANK YOU", bold_center))
    elements.append(Spacer(1, 8))

    doc.build(elements)
