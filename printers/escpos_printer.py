# COMMENT this file if printer not connected
from escpos.printer import Usb

def print_token(token, customer, cart):
    printer = Usb(0x04b8, 0x0202)  # Change vendor/product ID if needed
    printer.text("HOSPITAL CANTEEN\n")
    printer.text(f"Token No: {token}\n")
    printer.text(f"Customer: {customer}\n\n")
    for item, qty, _ in cart:
        printer.text(f"{item} x {qty}\n")
    printer.cut()
