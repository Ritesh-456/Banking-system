# main.py
import os
import json
import importlib

bank_map = {
    1: 'sbi',
    2: 'bob',
    3: 'pnb',
    4: 'canara',
    5: 'union'
}

base_path = os.path.dirname(__file__)
folder_path = os.path.join(base_path, 'data_store')
os.makedirs(folder_path, exist_ok=True)

new_customer = int(input(
    "Welcome! Choose your Bank:\n"
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


choice = input("Do you want to Create a New Account? (yes/no): ").lower()
file_path = os.path.join(folder_path, f"{bank_key.upper()}.txt")

# Load existing data
if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    with open(file_path, "r") as f:
        try:
            all_users = json.load(f)
        except json.JSONDecodeError:
            all_users = {}
else:
    all_users = {}


if choice == 'yes':
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

    pin = input("Create a 4-digit PIN: ")
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
elif choice == 'no':
    pin = input("Enter your 4-digit PIN: ")

    if pin not in all_users:
        print("❌ PIN not found.")
        exit()

    user_data = all_users[pin]

    # Dynamically import class
    try:
        module = importlib.import_module(f"bank_classes.{bank_key}")
        BankClass = getattr(module, bank_key.upper())
        user = BankClass(user_data)
    except Exception as e:
        print(f"❌ Could not load bank class: {e}")
        exit()

    while True:
        print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Exit")
        option = input("Choose an option: ")

        if option == '1':
            amt = int(input("Amount to deposit: "))
            user.deposit(amt)
        elif option == '2':
            amt = int(input("Amount to withdraw: "))
            user.withdraw(amt)
        elif option == '3':
            user.check_balance()
        elif option == '4':
            break
        else:
            print("❌ Invalid Option.")

    # Save back data after session
    all_users[pin] = user.data
    with open(file_path, "w") as f:
        json.dump(all_users, f, indent=4)
else:
    print("❌ Invalid choice. Exiting.")
