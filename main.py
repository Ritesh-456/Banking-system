# main.py
import os
import json
import importlib

# Available banks
bank_map = {
    1: 'sbi',
    2: 'bob',
    3: 'pnb',
    4: 'canara',
    5: 'union'
}

# Setup data store
base_path = os.path.dirname(__file__)
folder_path = os.path.join(base_path, 'data_store')
os.makedirs(folder_path, exist_ok=True)

# Step 1: Ask if new or existing customer
account_type = input("Are you a new customer? (yes/no): ").strip().lower()

# ------------------------ NEW CUSTOMER ------------------------
if account_type == 'yes':
    # Ask for bank choice
    new_customer = int(input(
        "Choose your Bank:\n"
        "1. SBI\n"
        "2. BoB\n"
        "3. PNB\n"
        "4. Canara\n"
        "5. Union\n"
        "Enter number (1-5): "
    ))

    bank_key = bank_map.get(new_customer)
    if not bank_key:
        print("❌ Invalid option.")
        exit()

    file_path = os.path.join(folder_path, f"{bank_key.upper()}.txt")
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            try:
                all_users = json.load(f)
            except json.JSONDecodeError:
                all_users = {}
    else:
        all_users = {}

    # Collect new user data
    user_data = {
        "bank_name": bank_key.upper(),
        "first_name": input("First Name: "),
        "last_name": input("Last Name: "),
        "email_id": input("Email: "),
        "phone_number": int(input("Phone Number: ")),
        "aadhar_card": int(input("Aadhar Number: ")),
        "pan_card": input("PAN Number: "),
        "balance": 0
    }

    pin = input("Create 4-digit PIN: ")
    re_pin = input("Re-enter PIN to confirm: ")

    if pin == re_pin:
        if pin in all_users:
            print("❌ PIN already used. Try again.")
        else:
            all_users[pin] = user_data
            with open(file_path, "w") as f:
                json.dump(all_users, f, indent=4)
            print("✅ Account created successfully.")
    else:
        print("❌ PINs do not match.")


# ------------------------ EXISTING CUSTOMER ------------------------


elif account_type == 'no':
    bank_input = input("Enter your bank name (sbi/bob/pnb/canara/union): ").strip().lower()

    if bank_input not in bank_map.values():
        print("❌ Invalid bank name.")
        exit()

    file_path = os.path.join(folder_path, f"{bank_input.upper()}.txt")
    if not os.path.exists(file_path):
        print("❌ No customer data found for this bank.")
        exit()

    try:
        module = importlib.import_module(f"bank_classes.{bank_input}")
        BankClass = getattr(module, bank_input.upper())
    except Exception as e:
        print(f"❌ Error loading bank class: {e}")
        exit()

    with open(file_path, "r") as f:
        try:
            all_users = json.load(f)
        except json.JSONDecodeError:
            all_users = {}

    pin = input("Enter your 4-digit PIN: ")

    if pin not in all_users:
        print("❌ Invalid PIN. No such account found.")
        exit()

    user_data = all_users[pin]

    # Instantiate the bank class and match pin
    user = BankClass(user_data)
    if not user.match_pin(pin):
        print("❌ PIN mismatch. Access denied.")
        exit()

    print(f"\n✅ Welcome back, {user_data['first_name']}!")

    # Options loop
    while True:
        print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            amt = int(input("Enter amount to deposit: "))
            user.deposit(amt)
        elif choice == '2':
            amt = int(input("Enter amount to withdraw: "))
            user.withdraw(amt)
        elif choice == '3':
            user.check_balance()
        elif choice == '4':
            break
        else:
            print("❌ Invalid option.")

    # Save updated data
    all_users[pin] = user.data
    with open(file_path, "w") as f:
        json.dump(all_users, f, indent=4)
