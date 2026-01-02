import streamlit as st
import pandas as pd
from database.db import get_connection
from models.order_model import (
    mark_orders_paid,
    add_payment,
    get_paid_amount,
    finalize_order_if_paid
)
from utils.bill_generator import generate_customer_bill
import tempfile


def show_unpaid_billing():
    st.title("🧾 Unpaid Billing & Settlement")

    # ================= FETCH UNPAID ORDERS =================
    conn = get_connection()
    df = pd.read_sql("""
        SELECT
            o.id,
            o.customer_type,
            COALESCE(o.doctor_name, o.staff_name, o.patient_name) AS customer_name,
            o.room_number,
            o.created_at,
            o.total,

            COALESCE(SUM(p.amount), 0) AS paid_amount,
            (o.total - COALESCE(SUM(p.amount), 0)) AS balance,

            GROUP_CONCAT(
                oi.item_name || ' x' || oi.qty,
                ', '
            ) AS items
        FROM orders o
        JOIN order_items oi ON o.id = oi.order_id
        LEFT JOIN payments p ON o.id = p.order_id
        WHERE o.payment_status = 'UNPAID'
        GROUP BY o.id
        ORDER BY customer_name, o.created_at
    """, conn)
    conn.close()

    if df.empty:
        st.success("No unpaid bills 🎉")
        return

    # ================= SORT OPTIONS =================
    st.subheader("Sort Unpaid Bills")

    sort_by = st.selectbox(
        "Sort By",
        ["Customer Name", "Amount", "Date"],
        key="unpaid_sort"
    )

    if sort_by == "Customer Name":
        df = df.sort_values("customer_name")
    elif sort_by == "Amount":
        df = df.sort_values("balance", ascending=False)
    else:
        df = df.sort_values("created_at")

    # ================= SELECT CUSTOMER =================
    st.subheader("Unpaid Customers")

    customers = df["customer_name"].unique()

    selected_customer = st.selectbox(
        "Select Customer",
        customers,
        key="unpaid_customer"
    )

    cust_df = df[df["customer_name"] == selected_customer]

    # ================= CUSTOMER BILL =================
    st.markdown(f"### 🧑 {selected_customer}")

    st.dataframe(
        cust_df[
            ["created_at", "items", "total", "paid_amount", "balance", "room_number"]
        ],
        use_container_width=True
    )

    total_due = cust_df["balance"].sum()
    st.metric("Total Outstanding", f"₹{total_due:.2f}")

    st.divider()

    # ================= PDF BILL =================
    st.subheader("🖨️ Generate Customer Bill")

    if st.button("📄 Download Bill (PDF)"):
        orders_data = []
        for _, row in cust_df.iterrows():
            orders_data.append({
                "date": row["created_at"],
                "items": row["items"],
                "total": row["total"],
                "paid": row["paid_amount"],
                "balance": row["balance"]
            })

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            generate_customer_bill(
                filename=tmp.name,
                customer_name=selected_customer,
                customer_type=cust_df.iloc[0]["customer_type"],
                room_number=cust_df.iloc[0]["room_number"],
                orders=orders_data
            )

            with open(tmp.name, "rb") as f:
                st.download_button(
                    label="⬇️ Download PDF",
                    data=f,
                    file_name=f"{selected_customer}_bill.pdf",
                    mime="application/pdf"
                )

    st.divider()

    # ================= FULL SETTLEMENT =================
    st.subheader("✅ Full Settlement")

    full_payment_mode = st.radio(
        "Payment Mode (Full)",
        ["Cash", "UPI"],
        horizontal=True,
        key="full_payment_mode"
    )

    if st.button("Mark ALL as Paid", type="primary"):
        for _, row in cust_df.iterrows():
            if row["balance"] > 0:
                add_payment(row["id"], row["balance"], full_payment_mode)
                finalize_order_if_paid(row["id"])

        st.success("All dues settled successfully")
        st.rerun()

    st.divider()

    # ================= PARTIAL PAYMENT =================
    st.subheader("💳 Partial Payment")

    partial_payment_mode = st.radio(
        "Payment Mode (Partial)",
        ["Cash", "UPI"],
        horizontal=True,
        key="partial_payment_mode"
    )

    amount = st.number_input(
        "Amount to Pay Now",
        min_value=0.0,
        step=10.0
    )

    if st.button("➕ Add Partial Payment"):
        if amount <= 0:
            st.error("Enter a valid amount")
            return

        remaining = amount

        for _, row in cust_df.iterrows():
            if remaining <= 0:
                break

            if row["balance"] <= 0:
                continue

            pay = min(row["balance"], remaining)
            add_payment(row["id"], pay, partial_payment_mode)
            finalize_order_if_paid(row["id"])
            remaining -= pay

        st.success("Partial payment recorded successfully")
        st.rerun()
