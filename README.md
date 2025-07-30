# 💳 SBI Bank System with Streamlit UI

A simple Object-Oriented Banking System that allows users to create and manage bank accounts via a **Streamlit web interface**. Data is securely stored in `.txt` files using JSON format. This app supports **account creation**, **deposit**, **withdrawal**, and **balance check** for multiple banks.

---

## 📂 Project Structure

bank_project/
├── streamlit_app.py # Streamlit UI (Frontend)
├── main.py # CLI Version (For testing)
├── data_store/ # Stores user JSON data by bank
│ └── SBI.txt # Example file
├── bank_classes/ # Bank-wise class files
│ ├── __init__.py
│ └── sbi.py # SBI Bank class
├── requirements.txt # Python dependencies
└── README.md # Project documentation
