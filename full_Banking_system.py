record = {
    1234: {
        'name': 'Rakesh Charan',
        'phone': 9876543210,
        'address': 'Laxmi Nagar',
        'addhar_Card': 789778977897,
        'balance': 0,
    },
    4567: {
        'name': 'Sailesh Kumar',
        'phone': 9123456780,
        'address': 'Vani Vihar',
        'addhar_Card': 32133213213,
        'balance': 0,
    },
    7890: {
        'name': 'Ankit Sharma',
        'phone': 9988776655,
        'address': 'Rajendra Nagar',
        'addhar_Card': 123412341234,
        'balance': 500,
    },
    2345: {
        'name': 'Ritu Das',
        'phone': 9001122334,
        'address': 'Salt Lake',
        'addhar_Card': 987698769876,
        'balance': 1500,
    },
    6789: {
        'name': 'Aman Gupta',
        'phone': 8899001122,
        'address': 'Gandhi Nagar',
        'addhar_Card': 564356435643,
        'balance': 300,
    },
    1357: {
        'name': 'Deepak Mishra',
        'phone': 9090909090,
        'address': 'Ashok Vihar',
        'addhar_Card': 765476547654,
        'balance': 1000,
    },
    2468: {
        'name': 'Kriti Sen',
        'phone': 9112233445,
        'address': 'Preet Vihar',
        'addhar_Card': 111122223333,
        'balance': 200,
    },
    3579: {
        'name': 'Nilesh Tiwari',
        'phone': 9223344556,
        'address': 'Karol Bagh',
        'addhar_Card': 444455556666,
        'balance': 250,
    },
    4680: {
        'name': 'Alok Ranjan',
        'phone': 9334455667,
        'address': 'Patia',
        'addhar_Card': 777788889999,
        'balance': 0,
    },
    5791: {
        'name': 'Meena Kumari',
        'phone': 9445566778,
        'address': 'Jayanagar',
        'addhar_Card': 999900001111,
        'balance': 750,
    },
    6812: {
        'name': 'Pooja Singh',
        'phone': 9556677889,
        'address': 'BTM Layout',
        'addhar_Card': 112233445566,
        'balance': 900,
    },
    7923: {
        'name': 'Sourav Pal',
        'phone': 9667788990,
        'address': 'Boring Road',
        'addhar_Card': 223344556677,
        'balance': 600,
    },
    8034: {
        'name': 'Shubham Jha',
        'phone': 9778899001,
        'address': 'Dum Dum',
        'addhar_Card': 334455667788,
        'balance': 1100,
    },
    9145: {
        'name': 'Anushka Mehra',
        'phone': 9889900112,
        'address': 'Alambagh',
        'addhar_Card': 445566778899,
        'balance': 100,
    },
    1023: {
        'name': 'Rahul Dev',
        'phone': 9990011223,
        'address': 'DLF Phase 3',
        'addhar_Card': 556677889900,
        'balance': 0,
    },
    1124: {
        'name': 'Isha Sharma',
        'phone': 9001122334,
        'address': 'Kondapur',
        'addhar_Card': 667788990011,
        'balance': 1800,
    },
    1225: {
        'name': 'Mohd. Arif',
        'phone': 9112233445,
        'address': 'Malviya Nagar',
        'addhar_Card': 778899001122,
        'balance': 2500,
    },
    1326: {
        'name': 'Nidhi Rathi',
        'phone': 9223344556,
        'address': 'Model Town',
        'addhar_Card': 889900112233,
        'balance': 400,
    },
    1427: {
        'name': 'Aditya Saxena',
        'phone': 9334455667,
        'address': 'Kharghar',
        'addhar_Card': 990011223344,
        'balance': 1700,
    },
    1528: {
        'name': 'Sanya Arora',
        'phone': 9445566778,
        'address': 'MG Road',
        'addhar_Card': 101112131415,
        'balance': 2000,
    }
}




def main(user_pin):
    if user_pin in record:
        print(f"welcome {record[user_pin]['name']}")

        class Bank:
            name = "SBI"
            main_branch = 'Navi_Mumbai'
            branch_manager = "Ashish Solanki"
            branch_IFSC = "SBI121001"

            def __init__(self, name, phone, address, addhar_Card, balance):
                self.__name = name
                self.__phone = phone
                self.__address = address
                self.__addhar_Card = addhar_Card
                self.__balance = balance

            def deposit(self, amount):
                self.__balance += amount
                record[user_pin]['balance'] = self.__balance

            def withdrawal(self, amount):
                if amount <= self.__balance:
                    self.__balance -= amount
                    record[user_pin]['balance'] = self.__balance
                    self.__statment1()
                else:
                    self.__statment2()

            def check_balance(self):
                return (f"\n*********************\nCurrent Balance is ₹{self.balance:.2f}\n*********************")

            @staticmethod
            def __statment1():
                print("Transaction Successful")

            @staticmethod
            def __statment2():
                print("Insufficient Balance")

        c1 = Bank(
            record[user_pin]['name'],
            record[user_pin]['phone'],
            record[user_pin]['address'],
            record[user_pin]['addhar_Card'],
            record[user_pin]['balance']
        )

        while True:
            ask = int(input("\nEnter the Number:\n"
                            "1. Deposit\n"
                            "2. Withdrawal\n"
                            "3. Check Balance\n"
                            "4. Exit\n"
                            "Choose a Number: "))

            if ask == 1:
                depo = int(input("Enter money to deposit: "))
                c1.deposit(depo)
                print(f"\n{record[user_pin]['name']}, your Current Balance is ₹{record[user_pin]['balance']:.2f}")
            elif ask == 2:
                withd = int(input("Enter money to withdraw: "))
                c1.withdrawal(withd)
                print(f"\n{record[user_pin]['name']}, your Current Balance is ₹{record[user_pin]['balance']:.2f}")
            elif ask == 3:
                print(c1.check_balance())
            elif ask == 4:
                print(f"Thank you for choosing {Bank.name}")
                break
            else:
                print("Invalid option, try again.")

    else:
        print("Un-authorise user")


if __name__ == "__main__":
    while True:
        user_pin = int(input("Enter Your Pin: "))
        if user_pin not in record:
            print("Exiting system. Goodbye!")
            break
        main(user_pin)



