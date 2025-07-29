class UNION:
    def __init__(self, user_data):
        self.data = user_data
        self.pin = user_data.get("pin")  # ✅ fix here

    def match_pin(self, entered_pin):
        return str(entered_pin) == self.pin

    def deposit(self, amount):
        self.data["balance"] += amount
        print(f"💰 ₹{amount} deposited successfully.")

    def withdraw(self, amount):
        if self.data["balance"] >= amount:
            self.data["balance"] -= amount
            print(f"💸 ₹{amount} withdrawn successfully.")
        else:
            print("❌ Insufficient balance.")

    def check_balance(self):
        print(f"💼 Your current balance is ₹{self.data['balance']}.")
