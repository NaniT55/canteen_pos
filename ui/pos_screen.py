import streamlit as st
from models.menu_model import get_menu
from services.order_service import place_order
from utils.pricing import get_price
from utils.thermal_receipt import generate_thermal_receipt
from collections import defaultdict
from config import APP_MODE
import tempfile
import base64
import streamlit.components.v1 as components


def show_pos():
    st.title("🍽️ Canteen POS")

    # ================= CUSTOMER TYPE =================
    customer = st.selectbox(
        "Customer Type",
        ["Doctor", "Patient", "Staff", "Visitor"],
        key="pos_customer_type"
    )

    # ================= CUSTOMER DETAILS =================
    st.subheader("Customer Details")

    details = {
        "doctor_name": None,
        "patient_name": None,
        "room_number": None,
        "staff_name": None
    }

    if customer == "Doctor":
        details["doctor_name"] = st.text_input("Doctor Name")

    elif customer == "Patient":
        details["patient_name"] = st.text_input("Patient Name")
        details["room_number"] = st.text_input("Room Number")

    elif customer == "Staff":
        details["staff_name"] = st.text_input("Staff Name")

    # ================= PAYMENT =================
    st.subheader("Payment")

    payment_mode = st.radio(
        "Payment Method",
        ["Cash", "UPI", "Unpaid"],
        horizontal=True
    )

    st.divider()

    # ================= MENU =================
    st.subheader("Menu")

    menu = get_menu(only_enabled=True)
    if not menu:
        st.warning("No items available for sale")
        return

    cart = []
    menu_by_category = defaultdict(list)

    for item in menu:
        menu_by_category[item[2]].append(item)

    for category, items in menu_by_category.items():
        st.markdown(f"### {category}")

        for item in items:
            item_id = item[0]
            name = item[1]
            price = get_price(item, customer)

            qty = st.number_input(
                f"{name} (₹{price})",
                min_value=0,
                step=1,
                key=f"qty_{item_id}"
            )

            if qty > 0:
                cart.append((name, qty, price))

    st.divider()

    # ================= CART SUMMARY =================
    if cart:
        st.subheader("🧾 Order Summary")

        total = sum(qty * price for _, qty, price in cart)
        for name, qty, price in cart:
            st.write(f"{name} × {qty} = ₹{qty * price}")

        st.metric("Total Amount", f"₹{total:.2f}")
        st.divider()

    # ================= GENERATE TOKEN =================
    if st.button("Generate Token", type="primary", use_container_width=True):

        if not cart:
            st.error("Please select at least one item")
            return

        if payment_mode == "Unpaid" and customer == "Visitor":
            st.error("Visitors must pay immediately")
            return

        if customer == "Doctor" and not details["doctor_name"]:
            st.error("Doctor name required")
            return

        if customer == "Patient" and (not details["patient_name"] or not details["room_number"]):
            st.error("Patient name and room number required")
            return

        if customer == "Staff" and not details["staff_name"]:
            st.error("Staff name required")
            return

        # ---- PLACE ORDER ----
        token = place_order(customer, cart, details, payment_mode)
        st.success(f"✅ Token Generated: {token}")

        # ---- PREPARE RECEIPT ----
        total_amount = sum(qty * price for _, qty, price in cart)
        paid = total_amount if payment_mode in ["Cash", "UPI"] else 0
        balance = total_amount - paid

        receipt_items = [
            {"name": name, "qty": qty, "price": price}
            for name, qty, price in cart
        ]

        customer_name = (
            details.get("doctor_name")
            or details.get("staff_name")
            or details.get("patient_name")
            or "Visitor"
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            generate_thermal_receipt(
                filename=tmp.name,
                customer_name=customer_name,
                customer_type=customer,
                room_number=details.get("room_number"),
                items=receipt_items,
                total=total_amount,
                paid=paid,
                balance=balance
            )

            st.session_state["receipt_path"] = tmp.name
            st.session_state["ready_to_print"] = True

    # ================= PRINT SECTION =================
    if st.session_state.get("ready_to_print"):

        st.subheader("🖨️ Print Receipt")

    if APP_MODE == "CLOUD":
        st.info("Printing disabled in demo mode (Cloud deployment)")
    else:
        if st.button("PRINT THERMAL RECEIPT", type="secondary"):
            with open(st.session_state["receipt_path"], "rb") as f:
                pdf_bytes = f.read()

            pdf_base64 = base64.b64encode(pdf_bytes).decode()

            components.html(
                f"""
                <iframe
                    src="data:application/pdf;base64,{pdf_base64}"
                    style="display:none;"
                    onload="this.contentWindow.print();">
                </iframe>
                """,
                height=0,
            )


        if st.button("🧾 New Order"):
            st.session_state.clear()
            st.rerun()
