import sqlite3


conn = sqlite3.connect('Bank.db')

c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS user(
            NAME CHAR(20) NOT NULL ,
            SURNAME CHAR(20),
            GMAIL TEXT,
            AGE INTEGER,
            PASSWORD TEXT,
            BALANCE FLOAT DEFAULT 0)''')

conn.commit()


class User:
    def init(self,name,surname,gmail,age,password,balance):
        pass

    def register(self):
        print("Welcome to the Geo Bank Registration!")
        self.name = input("Name: ")
        self.surname = input("Surname: ")
        self.gmail = input("Gmail: ")
        self.age = int(input("Age: "))
        self.password = input("Password: ")
        c.execute('''INSERT INTO user(NAME,SURNAME,GMAIL,AGE,PASSWORD,BALANCE) VALUES(?,?,?,?,?,?)'''
        ,(self.name,
          self.surname,
          self.gmail+'@gmail.com',
          self.age,
          self.password,
          0))
        conn.commit()
        print("Registration Successful!")
        ask = input("Do you want to login? (y/n) ").lower()
        if ask == "y":
            self.auth()
        else:
            print("Bye!")
            conn.close()


    def auth(self):
        c.execute('''SELECT * FROM user ''')
        conn.commit()
        self.gmail = input("Gmail: ")
        self.password = input("Password: ")
        dat = c.execute('''select gmail,password from user where gmail = ? and password = ?''',(self.gmail,self.password))
        conn.commit()
        for_auth = False
        if len(dat.fetchall()) > 0:
            print("Logged in!")
            c.execute('''select name,surname,balance from user where gmail = ? and password = ?''',(self.gmail,self.password))
            conn.commit()
            for row in c.fetchall():
                print("Welcome to the Geo Bank",row[0],row[1],"Your balance is:", row[2],"₾")
                for_auth = True
            if for_auth:
                self.operation_ask()
        else:
            print("Failed to login!")
            self.auth()
        c.execute('''SELECT * FROM user ''')
        conn.commit()

    def ask(self):
        answer = input("Register or Login? (R/L): ").lower()
        if answer == "r":
            self.register()
        elif answer == "l":
            self.auth()
        else:
            print("Try Again!")
            self.ask()
    def withdraw(self):
        withdraw = float(input("How much do you want to withdraw? "))
        c.execute('''select balance from user where gmail = ? and password = ?''',(self.gmail,self.password))
        conn.commit()
        for row in c.fetchall():
            if withdraw > 0 and withdraw <= row[0]:
                c.execute('''update user set balance = balance - ? where gmail = ? and password = ?''',(withdraw,self.gmail,self.password))
                conn.commit()
                c.execute('''select balance from user where gmail = ? and password = ?''',(self.gmail,self.password))
                conn.commit()
                for i in c.fetchall():
                    print("Your balance is:",i[0],"₾")
            else:
                print("Invalid amount!")
                self.operation_ask()
    def deposit(self):
        c.execute('''update user set balance = balance + ? where gmail = ? and password = ?''',(float(input("How much do you want to deposit? ")),self.gmail,self.password))
        conn.commit()
        c.execute('''select balance from user where gmail = ? and password = ?''',(self.gmail,self.password))
        conn.commit()
        for row in c.fetchall():
            print("Your balance is:",row[0],"₾")
    def transfer(self):
        transfer_to = input("Transfer to: ")
        transfer_amount = float(input("How much do you want to transfer? "))
        c.execute('''select balance from user where gmail = ?''', (transfer_to,))
        if len(c.fetchall()) > 0:
            c.execute('''select balance from user where gmail = ?''',(self.gmail,))
            for row in c.fetchall():
                if transfer_amount > 0 and transfer_amount <= row[0]:
                    c.execute('''update user set balance = balance - ? where gmail = ? and password = ?''',(transfer_amount,self.gmail,self.password))
                    conn.commit()
                    c.execute('''update user set balance = balance + ? where gmail = ?''',(transfer_amount,transfer_to))
                    conn.commit()
                    c.execute('''select balance from user where gmail = ? and password = ?''',(self.gmail,self.password))
                    conn.commit()
                    print("%s transfered to %s" % (transfer_amount, transfer_to))
                    for i in c.fetchall():
                        print("Your balance is:",i[0],"₾")
                else:
                    print("Invalid amount!")
                    self.operation_ask()
        else:
            print("Invalid User, Try Again..")
            self.transfer()

    def operation_ask(self):
        while True:
            ask = input("Which operation do you want to do? \nWithdraw \nDeposit \nTransfer \n: ").lower()
            if ask == "withdraw":
                self.withdraw()
            elif ask == "deposit":
                self.deposit()
            elif ask == "transfer":
                self.transfer()
            elif ask == "exit":
                exit()
            elif ask == "logout":
                self.ask()
            else:
                print("Try Again!")
                self.operation_ask()

a = User()
a.ask()
