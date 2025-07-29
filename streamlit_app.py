import os
import json
import importlib
import streamlit as st

# --- Session State Initialization ---
# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'user_object' not in st.session_state:
    st.session_state.user_object = None
# ------------------------------------

# Setup paths
bank_map = {
    "SBI": "sbi",
    "BoB": "bob",
    "PNB": "pnb",
    "Canara": "canara",
    "Union": "union"
}
base_path = os.path.dirname(__file__)
folder_path = os.path.join(base_path, 'data_store')
os.makedirs(folder_path, exist_ok=True)

st.title("🏦 Simple Banking System")

# Only show menu options if not logged in
if not st.session_state.logged_in:
    menu = st.sidebar.radio("Choose Option", ["New Customer", "Existing Customer"])
else:
    # If logged in, display welcome message and logout button
    st.sidebar.write(f"Welcome, {st.session_state.user_data['first_name']}!")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.session_state.user_object = None
        st.rerun() # Rerun to reflect logout state and show login menu
    menu = "Existing Customer" # Force the main view to "Existing Customer" if logged in

# ========== NEW CUSTOMER ==========
# This section will only be visible if 'New Customer' is selected AND user is not logged in
if menu == "New Customer" and not st.session_state.logged_in:
    st.header("Register New Customer")
    bank_name = st.selectbox("Choose Your Bank", list(bank_map.keys()), key="new_customer_bank_select")
    first_name = st.text_input("First Name", key="new_customer_first_name")
    last_name = st.text_input("Last Name", key="new_customer_last_name")
    email_id = st.text_input("Email", key="new_customer_email")
    phone_number = st.text_input("Phone Number", key="new_customer_phone_number")
    aadhar = st.text_input("Aadhar Number", key="new_customer_aadhar")
    pan = st.text_input("PAN Number", key="new_customer_pan")
    pin = st.text_input("Create 4-digit PIN", type="password", key="new_customer_pin")
    re_pin = st.text_input("Re-enter PIN", type="password", key="new_customer_re_pin")

    if st.button("Create Account", key="create_account_button"):
        # Basic input validation
        if not (first_name and last_name and email_id and phone_number and aadhar and pan and pin and re_pin):
            st.error("❌ Please fill in all fields.")
            st.stop()
        if not phone_number.isdigit() or len(phone_number) != 10:
            st.error("❌ Phone Number must be 10 digits.")
            st.stop()
        if not aadhar.isdigit() or len(aadhar) != 12:
            st.error("❌ Aadhar Number must be 12 digits.")
            st.stop()
        if not pin.isdigit() or len(pin) != 4:
            st.error("❌ PIN must be a 4-digit number.")
            st.stop()

        # Check for PIN in all files
        pin_exists = False
        for bank_key in bank_map:
            path = os.path.join(folder_path, f"{bank_key}.txt")
            if os.path.exists(path):
                with open(path, "r") as f:
                    try:
                        users = json.load(f)
                        if pin in users:
                            pin_exists = True
                            break
                    except json.JSONDecodeError: # Handle empty or malformed JSON files
                        continue

        if pin != re_pin:
            st.error("❌ PINs do not match.")
        elif pin_exists:
            st.error("❌ PIN already used in another bank.")
        else:
            file_path = os.path.join(folder_path, f"{bank_name}.txt")
            if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                with open(file_path, "r") as f:
                    try:
                        all_users = json.load(f)
                    except json.JSONDecodeError:
                        all_users = {} # File exists but is empty or invalid JSON
            else:
                all_users = {} # File does not exist or is empty

            user_data = {
                "bank_name": bank_name,
                "first_name": first_name,
                "last_name": last_name,
                "email_id": email_id,
                "phone_number": int(phone_number),
                "aadhar_card": int(aadhar),
                "pan_card": pan,
                "balance": 0,
                "pin": pin
            }
            all_users[pin] = user_data
            with open(file_path, "w") as f:
                json.dump(all_users, f, indent=4)
            st.success("✅ Account created successfully!")

# ========== EXISTING CUSTOMER ==========
elif menu == "Existing Customer":
    if not st.session_state.logged_in:
        st.header("Existing Customer Login")
        pin = st.text_input("Enter your 4-digit PIN", type="password", key="login_pin_input")

        if st.button("Login", key="login_button"):
            if not pin.isdigit() or len(pin) != 4:
                st.error("❌ Please enter a valid 4-digit PIN.")
                st.stop()

            found = False
            user_data = None
            user_object = None

            for bank_key_upper, bank_key_lower in bank_map.items():
                file_path = os.path.join(folder_path, f"{bank_key_upper}.txt")
                if not os.path.exists(file_path) or os.path.getsize(file_path) == 0:
                    continue

                with open(file_path, "r") as f:
                    try:
                        all_users = json.load(f)
                    except json.JSONDecodeError:
                        continue # Skip malformed JSON files

                if pin in all_users:
                    found = True
                    user_data = all_users[pin]
                    bank_name_for_module = user_data["bank_name"].lower() # Use stored bank_name

                    try:
                        module = importlib.import_module(f"bank_classes.{bank_name_for_module}")
                        BankClass = getattr(module, bank_name_for_module.upper())
                        user_object = BankClass(user_data)
                    except Exception as e:
                        st.error(f"❌ Error loading bank class for {user_data['bank_name']}: {e}")
                        # Clear potential partial login state
                        st.session_state.logged_in = False
                        st.session_state.user_data = None
                        st.session_state.user_object = None
                        st.stop() # Stop execution if bank class loading fails

                    # If the user.match_pin(pin) was intended for a different validation
                    # than the dict key, it would go here. Otherwise, it's redundant.
                    # Example: if not user_object.match_pin(pin): ...

                    st.success(f"✅ Welcome back, {user_data['first_name']}!")
                    st.session_state.logged_in = True
                    st.session_state.user_data = user_data # Store current user's data
                    st.session_state.user_object = user_object # Store the instantiated bank object
                    st.rerun() # Rerun immediately to display the banking options
                    break # Break loop once user is found and logged in

            if not found:
                st.error("❌ No account found with this PIN.")
    else: # User is already logged in
        st.header(f"Account Dashboard - {st.session_state.user_data['first_name']}")

        # Retrieve user object and data from session state
        user = st.session_state.user_object
        user_data_from_session = st.session_state.user_data

        action = st.radio("Choose Action", ["Deposit", "Withdraw", "Check Balance"], key="choose_action_radio")

        amount = 0 # Initialize amount
        if action != "Check Balance":
            amount = st.number_input("Enter Amount", min_value=0.0, step=100.0, key="amount_input") # Use float for money

        if st.button("Submit Action", key="submit_action_button"):
            if action == "Deposit":
                user.deposit(amount)
                st.success(f"✅ ₹{amount:,.2f} deposited successfully.")
            elif action == "Withdraw":
                if user.withdraw(amount):
                    st.success(f"✅ ₹{amount:,.2f} withdrawal successful.")
                else:
                    st.error("❌ Insufficient balance.")

            # After any transaction, update the user data in session state
            # and save the entire bank's data back to the file
            st.session_state.user_data = user.data # 'user.data' should now have the updated balance

            file_path = os.path.join(folder_path, f"{user_data_from_session['bank_name'].upper()}.txt")
            if os.path.exists(file_path):
                with open(file_path, "r") as f:
                    try:
                        all_users = json.load(f)
                    except json.JSONDecodeError:
                        all_users = {} # Handle case where file might have become corrupt/empty
                all_users[user_data_from_session['pin']] = st.session_state.user_data # Update with the latest data from session state
                with open(file_path, "w") as f:
                    json.dump(all_users, f, indent=4)
            else:
                 st.error("❌ Bank data file not found for saving balance. Please contact support.")

            # Rerun the app to reflect updated balance immediately after transaction
            st.rerun()

        if action == "Check Balance":
            st.info(f"💰 Current Balance: ₹{st.session_state.user_data['balance']:,.2f}") # Display balance from session state