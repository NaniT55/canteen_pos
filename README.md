🍽️ Hospital Canteen POS System (Streamlit)

A full-featured Point of Sale (POS) system built using Python & Streamlit for managing hospital canteen operations.
The system supports billing, menu management, unpaid billing, partial payments, reports, and thermal receipt printing.

This project is designed to work in two modes:

🖥️ Local POS mode (real billing & printing)

☁️ Streamlit Cloud demo mode (safe deployment for demos/portfolio)

🚀 Features
🧾 POS Billing

Doctor / Patient / Staff / Visitor billing

Category-wise menu display

Automatic token generation

Cash / UPI / Unpaid payments

Visitor payment enforcement

🖨️ Thermal Receipt (80mm)

Industry-standard 80mm thermal receipt format

Item name on left, price on right

Printable PDF receipts

Browser-based print support (local mode)

💳 Unpaid Billing & Partial Payments

Track unpaid bills per customer

Partial payment support

Mark bills as fully paid

Monthly unpaid billing summary

📦 Menu Management

Categories like Breakfast, Lunch, Snacks, Drinks, etc.

Different pricing for:

Doctors & Staff

Patients

Visitors

Enable / disable items without deleting them

📊 Reports

Daily Cash + UPI summary

Monthly unpaid billing

Transaction history with item details

🏗️ Project Structure
canteen_pos/
│
├── app.py                 # Main entry point
├── config.py              # Environment mode (LOCAL / CLOUD)
├── requirements.txt
│
├── data/
│   └── canteen.db         # SQLite database
│
├── database/
│   └── db.py              # DB connection & initialization
│
├── models/                # DB models
├── services/              # Business logic
├── utils/
│   ├── pricing.py
│   ├── thermal_receipt.py
│
├── ui/
│   └── pos_screen.py      # POS UI
│
└── .streamlit/
    └── config.toml

🖥️ Running Locally (Recommended for Real POS)
1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Run the App
streamlit run app.py

3️⃣ Usage

Designed for continuous daily use

No request limits

Works offline

Ideal for hospital canteen billing

☁️ Streamlit Cloud Deployment (Demo / Portfolio)

This project can be safely deployed on Streamlit Community Cloud in demo mode.

Important Notes

Printing is disabled in cloud mode

SQLite database may reset on redeploy

Intended for demonstration only

Environment Variable

Set this in Streamlit Cloud:

APP_MODE = CLOUD

⚙️ Configuration Modes
Mode	Purpose
LOCAL	Real billing + printing
CLOUD	Demo / portfolio deployment

Configured via config.py.

🖨️ Printing Limitations (Important)

Due to browser security:

Silent printing is not possible

A single Print button click is required

This is standard behavior in all web-based POS systems

🛡️ Why Streamlit is Used

Rapid development

Clean UI

Python-based logic

Perfect for internal tools & small POS systems

Easy to migrate later to FastAPI / React if needed

📌 Use Cases

Hospital canteen billing

College canteen POS

Office cafeteria billing

Demo POS for academic projects

🔮 Future Enhancements

User authentication (Admin / Cashier)

Kitchen order slip

ESC/POS direct silent printing

PostgreSQL for cloud production

Multi-counter support

📄 License

This project is for educational and internal use.
You may extend or modify it as needed.

🙌 Author

Developed as a real-world hospital canteen POS system using Python & Streamlit by Varun Tanniru