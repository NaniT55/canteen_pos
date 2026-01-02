import streamlit as st
import pandas as pd
from database.db import get_connection

def show_reports():
    st.title("📊 Reports")

    tab1, tab2 = st.tabs([
        "💰 Daily Cash + UPI Summary",
        "📅 Monthly Unpaid Billing"
    ])

    # ==========================
    # TAB 1: DAILY CASH + UPI
    # ==========================
    with tab1:
        st.subheader("Daily Cash + UPI Summary")

        conn = get_connection()
        df = pd.read_sql("""
            SELECT
                DATE(created_at) AS day,
                SUM(CASE WHEN payment_mode = 'Cash' THEN total ELSE 0 END) AS cash_total,
                SUM(CASE WHEN payment_mode = 'UPI' THEN total ELSE 0 END) AS upi_total,
                SUM(total) AS total_sales
            FROM orders
            WHERE payment_status = 'PAID'
            GROUP BY DATE(created_at)
            ORDER BY day DESC
        """, conn)
        conn.close()

        if df.empty:
            st.info("No paid transactions found.")
        else:
            st.dataframe(df, use_container_width=True)

            st.markdown("### 🔢 Totals (All Days)")
            col1, col2, col3 = st.columns(3)

            col1.metric("Total Cash", f"₹{df['cash_total'].sum():.2f}")
            col2.metric("Total UPI", f"₹{df['upi_total'].sum():.2f}")
            col3.metric("Grand Total", f"₹{df['total_sales'].sum():.2f}")

    # ==========================
    # TAB 2: MONTHLY UNPAID
    # ==========================
    with tab2:
        st.subheader("Monthly Unpaid Billing")

        conn = get_connection()
        df_unpaid = pd.read_sql("""
            SELECT
                strftime('%Y-%m', created_at) AS month,
                customer_type,
                doctor_name,
                staff_name,
                patient_name,
                room_number,
                SUM(total) AS unpaid_amount
            FROM orders
            WHERE payment_status = 'UNPAID'
            GROUP BY
                month,
                customer_type,
                doctor_name,
                staff_name,
                patient_name,
                room_number
            ORDER BY month DESC
        """, conn)
        conn.close()

        if df_unpaid.empty:
            st.info("No unpaid bills found.")
        else:
            st.dataframe(df_unpaid, use_container_width=True)

            st.markdown("### 💸 Total Unpaid Amount")
            st.metric(
                "Outstanding Balance",
                f"₹{df_unpaid['unpaid_amount'].sum():.2f}"
            )
