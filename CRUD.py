import numbers
import sqlite3

data = sqlite3.connect('TESTBANK.DB')

cursor = data.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS user(
                NAME CHAR(20) NOT NULL,
                LAST_NAME CHAR(20))''')

data.commit()

class Bank:
    def init(self, name, last_name):
        self.name = name
        self.last_name = last_name

    def add_user(self):
        self.name = input('Enter your name: ')
        self.last_name = input('Enter your last name: ')
        add_user_into_db = '''INSERT INTO user(NAME,LAST_NAME) VALUES (?, ?)'''
        cursor.execute(add_user_into_db, (self.name, self.last_name))
        data.commit()

    def delete_user(self):
        self.name = input('Enter your name: ')
        self.last_name = input('Enter your last name: ')
        delete_user_from_db = '''DELETE FROM user WHERE NAME = ? AND LAST_NAME = ?'''
        cursor.execute(delete_user_from_db, (self.name, self.last_name))
        data.commit()

    def update_user(self):
        self.name = input('Enter your name: ')
        self.last_name = input('Enter your last name: ')
        self.new_name = input('Enter new name: ')
        self.new_last_name = input('Enter new last name: ')
        update_user_from_db = '''UPDATE user SET NAME = ?, LAST_NAME = ? WHERE NAME = ? AND LAST_NAME = ?'''
        cursor.execute(update_user_from_db, (self.new_name, self.new_last_name, self.name, self.last_name))
        data.commit()

    def details(self):
        cursor.execute('''SELECT * FROM user''')
        print(cursor.fetchall())


    def start(self):
        self.number = input(
            "Select letter of operation (\n R - Show All Information From DB \n I - Add User into db \n D - Delete user from db \n U - Update user from db): ")

        bank = Bank()
        if self.number == 'R' or self.number== 'r':
            bank.details()
            bank.start()

        elif self.number == 'I' or self.number == 'i':
            bank.add_user()
            bank.details()
            bank.start()
        elif self.number== 'D' or self.number == 'd':
            bank.delete_user()
            bank.details()
            bank.start()

        elif self.number == 'U' or self.number== 'u':
            bank.update_user()
            bank.details()
            bank.start()


bank = Bank()
bank.start()