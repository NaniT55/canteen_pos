def get_price(item, customer_type):
    """
    item structure:
    [0] id
    [1] name
    [2] category
    [3] price_doctor_staff
    [4] price_patient
    [5] price_visitor
    [6] stock
    [7] is_enabled
    """

    price_doctor_staff = item[3]
    price_patient = item[4]
    price_visitor = item[5]

    if customer_type in ["Doctor", "Staff"]:
        return price_doctor_staff
    elif customer_type == "Patient":
        return price_patient
    else:  # Visitor
        return price_visitor
