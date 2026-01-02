def get_price(item, customer_type):
    """
    item = (
        id,
        name,
        category,
        price_doctor_staff,
        price_patient,
        price_visitor,
        is_enabled
    )
    """
    _, _, _, p_ds, p_patient, p_visitor, _ = item

    if customer_type in ["Doctor", "Staff"]:
        return p_ds
    elif customer_type == "Patient":
        return p_patient
    else:
        return p_visitor