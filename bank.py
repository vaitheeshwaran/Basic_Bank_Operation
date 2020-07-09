 #4 variables in that database
import pymysql
import random

class dbcon:
    def __init__(self):
        self.conn = pymysql.connect('localhost', 'root', '', 'bank')
        self.cursor = self.conn.cursor()

class Bank(dbcon):
    def __init__(self):
        super().__init__()

    def account_check(func):
        def inner(self, acc_no):
            Query = "SELECT * FROM Account2 WHERE Account_No = %d" % (acc_no)
            self.cursor.execute(Query)
            User = self.cursor.fetchone()
            if User:
                return func(self, acc_no)
            else:
                print("User Account doesn't exists, \nPlease Exit and create account first\nThen proceed further")
        return inner

    def Delete(self, acc_no):
        Query = "SELECT * FROM Account2 WHERE Account_No = %d" % (acc_no)
        self.cursor.execute(Query)
        User = self.cursor.fetchone()
        if User:
            Check = "SELECT Balance FROM Account2 WHERE Account_No=%d" % acc_no
            self.cursor.execute(Check)
            Amount = self.cursor.fetchone()
            print(Amount[0])
            if (Amount[0] == 0):
                Query = "DELETE FROM Account2 WHERE Account_No = %d" % (acc_no)
                self.cursor.execute(Query)
                self.conn.commit()
                print("Account Deleted Successfully")
            else:
                print("you have {} amount in your account".format(Amount[0]))
                Sug = input("Do you want to withdraw your money (yes/no): ")
                print(Sug)
                if Sug.lower() == "yes":
                    money = Amount[0]
                    Update = "UPDATE Account2 SET Balance = Balance-%d WHERE Account_No = %d" % (money, acc_no)
                    self.cursor.execute(Update)
                    self.conn.commit()
                    Query = "DELETE FROM Account2 WHERE Account_No = %d" % (acc_no)
                    self.cursor.execute(Query)
                    self.conn.commit()
                    print("Account Deleted Successfully")
                elif Sug.lower() == "no":
                    print("you cannot delete account without withdraw your money")
                else:
                    print("You are not gives proper input")
        else:
            print("User Account doesn't exists")

    def Search(self, Phone_no):

        Check = "SELECT Account_No FROM Account2 WHERE Phone=%d" % (Phone_no)
        self.cursor.execute(Check)
        Account = self.cursor.fetchone()
        if Account:
            print("Account numbers for this %d number: %d" % (Phone_no, Account[0]))
        else:
            print("Please provide valid phone number")

    def account_creation(self, acc_no, name, money, Phone_no):
        Query = "SELECT * FROM Account2 WHERE Account_No = %d" % (acc_no)
        self.cursor.execute(Query)
        User = self.cursor.fetchone()
        if User == None:
            self.cursor.execute("INSERT INTO Account2 (Account_No, Name, Balance, Phone) VALUES(%d, '%s', %d, %d)" % (acc_no, name, money, Phone_no))
            self.conn.commit()
            print("User Account Successfully Created")
            print("Your Account Number is %d" % (acc_no))
        else:
            print("User Account Exists, \nThe Account NO:%d" % (acc_no))

    @account_check
    def deposit(self, acc_no):
        money = int(input("Enter the money to deposit: "))
        if (money > 0):
            Update_Query = "UPDATE Account2 SET Balance = Balance+%d WHERE Account_No = %d" % (money, acc_no)
            self.cursor.execute(Update_Query)
            self.conn.commit()
            self.Checkbalance(acc_no)
        else:
            print("Please give proper amount to the withdraw")

    @account_check
    def withdraw(self, acc_no):
        money = int(input("Enter the money to withdraw: "))
        if (money > 0):
            Check = "SELECT Balance FROM Account2 WHERE Account_No=%d" % acc_no
            self.cursor.execute(Check)
            Amount = self.cursor.fetchone()
            if ((Amount[0]-min) >= money):
                Update = "UPDATE Account2 SET Balance = Balance-%d WHERE Account_No = %d" % (money, acc_no)
                self.cursor.execute(Update)
                self.conn.commit()
                self.Checkbalance(acc_no)
            else:
                print("Insufficient Balance")
        else:
            print("Please give proper amount to the deposit")

    def Checkbalance(self, acc_no):
        Select_Query = "Select Balance FROM Account2 WHERE Account_No = %d" % acc_no
        self.cursor.execute(Select_Query)
        Balance = self.cursor.fetchone()
        print("Account Balance: %d" % Balance[0])

    def Transaction(self):
        acc_no = int(input("Enter Account No: "))
        while (1):
            Choice = int(input("Please select following \n1:Withdraw\n2:Deposit\n3:Checkbalance\n4:Exit\n"))

            if Choice == 1:
                obj.withdraw(acc_no)

            elif Choice == 2:
                obj.deposit(acc_no)

            elif Choice == 3:
                obj.Checkbalance(acc_no)

            elif Choice == 4:
                break;
            else:
                print("Please select proper action")
                continue;
obj = Bank()

while (1):
    min=500
    Choice = int(input("Please select the following \n1:Transaction\n2:Account creation\n3:Delete Account\n4:Search Account No\n5:Exit\n"))

    if Choice == 1:
        obj.Transaction()

    elif Choice == 2:
        name = input("Enter Account holder Name in Characters: ")
        name1 = name.lower().replace(" ", "")
        a = len(name1)
        count = 0
        for i in range(0, a):
            if(name1[i].islower()== False):
                break;
            else:
                count += 1
        if(count != a):
            print("Please provide valid name")
            continue;
        Phone_no = int(input("Enter mobile number: "))
        le_ph = len(str(Phone_no))
        if(le_ph == 10):
            money = int(input("Enter the initial money to deposit: "))
            if (money > 0):
                if (money > min):
                    acc_no = random.randrange(1, 10 ** 5)
                    obj.account_creation(acc_no, name, money, Phone_no)
                else:
                    print("Minimum Balance should be %d" %(min))
            else:
                print("Please provide valid money")
                continue;
        else:
            print("Please provide proper phone number: ")
            continue;

    elif Choice == 3:
        acc_no = int(input("Enter the Account number wants to delete: "))
        obj.Delete(acc_no)
    elif Choice == 4:
        Phone_no = int(input("Enter Account holder phone no: "))
        obj.Search(Phone_no)

    elif Choice == 5:
        break

    else:
        print("Please select proper action")
        continue;
