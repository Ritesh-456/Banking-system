class PNB:
    def __init__(self, user_data):
        self.data = user_data

    def deposit(self, amount):
        self.data["balance"] += amount
        print(f"₹{amount} deposited. New Balance: ₹{self.data['balance']}")

    def withdraw(self, amount):
        if amount > self.data["balance"]:
            print("❌ Insufficient Balance.")
        else:
            self.data["balance"] -= amount
            print(f"₹{amount} withdrawn. Remaining Balance: ₹{self.data['balance']}")

    def check_balance(self):
        print(f"🔎 Your Balance: ₹{self.data['balance']}")
