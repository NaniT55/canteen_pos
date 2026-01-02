import streamlit as st
from database.db import init_db
from ui.pos_screen import show_pos
from ui.reports_screen import show_reports
from ui.menu_screen import show_menu
from ui.unpaid_billing_screen import show_unpaid_billing


init_db()

st.sidebar.title("Canteen POS")

page = st.sidebar.radio(
    "Navigate",
    [
        "POS",
        "Menu Management",
        "Reports",
        "Unpaid Billing"
    ]
)

if page == "POS":
    show_pos()
elif page == "Menu Management":
    show_menu()
elif page == "Unpaid Billing":
    show_unpaid_billing()
else:
    show_reports()
