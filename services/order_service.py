from models.order_model import save_order, save_order_items
from services.inventory_service import deduct_stock
from utils.token_generator import generate_token

def place_order(customer, cart, details, payment_mode):
    token = generate_token()
    total = sum(qty * price for _, qty, price in cart)

    payment_status = "PAID" if payment_mode in ["Cash", "UPI"] else "UNPAID"

    order_id = save_order(
        token=token,
        customer=customer,
        total=total,
        payment_mode=payment_mode,
        payment_status=payment_status,
        doctor_name=details.get("doctor_name"),
        patient_name=details.get("patient_name"),
        room_number=details.get("room_number"),
        staff_name=details.get("staff_name")
    )

    save_order_items(order_id, cart)

    return token
