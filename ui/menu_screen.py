import streamlit as st
import pandas as pd
from models.menu_model import get_menu, add_menu_item

CATEGORIES = [
    "Breakfast", "Lunch", "Dinner", "Soups",
    "Snacks", "Biscuits", "Haldiram Products",
    "Drinks", "Chocolates"
]

def show_menu():
    st.title("🍽️ Menu Management")
    st.markdown("### ➕ Add New Menu Item")

    with st.container():
        col_left, col_right = st.columns([1.2, 1])

        # ---- ITEM DETAILS ----
        with col_left:
            name = st.text_input("Item Name", placeholder="Eg: Idli / Tea / Veg Soup")
            category = st.selectbox(
                                        "Category",
                                        CATEGORIES,
                                        key="add_category"
                                    )


        # ---- PRICING ----
        with col_right:
            st.markdown("**Pricing (₹)**")

            price_ds = st.number_input("Doctor / Staff", min_value=0.0, step=1.0)
            price_patient = st.number_input("Patient", min_value=0.0, step=1.0)
            price_visitor = st.number_input("Visitor", min_value=0.0, step=1.0)

        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("➕ Add Item", type="primary", use_container_width=True):
                if not name.strip():
                    st.error("Item name is required")
                else:
                    add_menu_item(
                        name=name,
                        category=category,
                        p_ds=price_ds,
                        p_patient=price_patient,
                        p_visitor=price_visitor
                    )
                    st.success("Menu item added successfully")
                    st.rerun()

    st.divider()

    # ---- EXISTING MENU ----
    st.markdown("### 📋 Existing Menu Items")

    menu = get_menu(only_enabled=False)

    if not menu:
        st.info("No menu items found.")
        return

    # ---- DISPLAY TABLE (WITHOUT STOCK) ----
    df = pd.DataFrame(
    menu,
    columns=[
        "ID", "Item", "Category",
        "Doctor/Staff ₹", "Patient ₹", "Visitor ₹",
        "Stock", "Enabled"
    ]
    )
    df = df.drop(columns=["Stock"])
    df["Enabled"] = df["Enabled"].map({1: "Yes", 0: "No"})


    st.dataframe(df, use_container_width=True, hide_index=True)

    st.divider()

    # ---- UPDATE SECTION ----
    st.markdown("### ✏️ Update Menu Item")

    # Map for dropdown
    item_map = {
        f"{row[1]} ({row[2]})": row[0]
        for row in menu
    }

    selected_label = st.selectbox(
        "Select Item to Update",
        item_map.keys()
    )

    selected_id = item_map[selected_label]

    # Get selected item row
    selected_item = next(item for item in menu if item[0] == selected_id)

    _, name, category, p_ds, p_patient, p_visitor, _, is_enabled = selected_item
    name = selected_item[1]
    category = selected_item[2]
    p_ds = selected_item[3]
    p_patient = selected_item[4]
    p_visitor = selected_item[5]


    col1, col2 = st.columns([1.2, 1])

    with col1:
        new_name = st.text_input(
                                    "Item Name",
                                    value=name,
                                    key="update_item_name"
                                )

        new_category = st.selectbox(
                                        "Category",
                                        CATEGORIES,
                                        index=CATEGORIES.index(category),
                                        key="update_category"
                                    )


    with col2:
        st.markdown("**Pricing (₹)**")
        new_p_ds = st.number_input(
            "Doctor / Staff",
            value=float(p_ds),
            min_value=0.0,
            step=1.0
        )
        new_p_patient = st.number_input(
            "Patient",
            value=float(p_patient),
            min_value=0.0,
            step=1.0
        )
        new_p_visitor = st.number_input(
            "Visitor",
            value=float(p_visitor),
            min_value=0.0,
            step=1.0
        )

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
    with col_btn2:
        if st.button("💾 Update Item", type="primary", use_container_width=True):
            from models.menu_model import update_menu_item

            update_menu_item(
                                item_id=selected_id,
                                name=new_name,
                                category=new_category,
                                p_ds=new_p_ds,
                                p_patient=new_p_patient,
                                p_visitor=new_p_visitor
                            )


            st.success("Menu item updated successfully")
            st.rerun()

    st.divider()
    st.markdown("### 🔒 Enable / Disable Menu Item")

    item_map = {
        f"{row[1]} ({row[2]})": row[0]
        for row in menu
    }

    selected_label = st.selectbox(
        "Select Item",
        item_map.keys(),
        key="toggle_item_select"
    )

    selected_id = item_map[selected_label]
    selected_item = next(item for item in menu if item[0] == selected_id)

    is_enabled = bool(selected_item[-1])

    toggle = st.radio(
        "Item Status",
        ["Enabled", "Disabled"],
        index=0 if is_enabled else 1,
        horizontal=True
    )

    if st.button("Apply Status Change", use_container_width=True):
        from models.menu_model import toggle_item_status
        toggle_item_status(selected_id, toggle == "Enabled")
        st.success("Item status updated")
        st.rerun()
