from optparse import Values
import pprint
import sqlite3
import json,requests
from textwrap import indent
from requests import request
from json import JSONDecodeError

conn = sqlite3.connect('''Davaleba.db''')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS series(
             GENRES ,
             NAMES ) ''')

conn.commit()


#### დავალებ ###
# დავალება შეფასებითი 3 აღწერა.

# რექუესთით წამოიღოს მონაცემები სერიალებზე ამ ლინკიდან https://api.tvmaze.com/search/shows?q=South PARK

# სადაც წერია South PARK უნდა იცვლებოდეს კონსოლიდან შეტანილი სახელით და მერე ეს წამოღებული ჯეისონი უნდა დაპარსოთ
# მანახოთ კონსოლში მონაცემები და თუ დავეთანხმე, შეინახოთ ბაზაში. თუ მონაცემები არ არსებობს გამომიტანეთ თავიდან შეიყვანეთ
# სახელი. უნდა შემეძლოს რამოდენიმე ჟანრის ძებნა. მაგალითად Horror უნდა ამოყაროს ყველა რაც გვაქ.



class ExistedDB:
    def __init__(self):
        pass
    
    def genre_to_db(self):
        #დავპარსე უკვე არსებული საიტი საიდანაც წამოვიღე ჟანრები და სახელები ფილმის , შევიტანე ბაზაში.
        self.url1 = 'https://api.tvmaze.com/search/shows?q=genres'
        self.result = requests.get(self.url1)
        self.jsonstring = self.result.json()
        #წამოღებული ინფორმაციიდან 2 ლაინი ავიღე, ჟანრი და სახელი, შევიტანე ბაზაში.
        for i in range(len(self.jsonstring)):
            c.execute('''INSERT INTO series VALUES(?,?)''', (self.jsonstring[i]['show']['genres'][0], self.jsonstring[i]['show']['name']))
            conn.commit()

    
    # ეს მეთოდი ემსახურება შემდეგს, --> South Park იცვლება ჩვენს მიერ შეყვანილი სერიალით ან ნებისმიერი რამით კონსოლით.
    def change_serie(self):
        self.url = 'https://api.tvmaze.com/search/shows?q=South PARK'
        self.result1 = requests.get(self.url)
        self.jsonstring1 = self.result1.json()

        
        self.changer = input("Change serie South Park: ")
       
        
        self.jsonstring1[0]["show"]["name"] = self.changer #სახელი შეიცვლება, ჩვენს მიერ შეყვანილით./
        print(json.dumps(self.jsonstring1,indent=4))
    
class DatabaseAdder(ExistedDB): # ეს კლასი არის შვილობილი კლასი ExistedDb-ს , და ამატებს მონაცემებს ბაზაში.
    def __init__(self):
        pass

    def adder(self):
        super().change_serie()
        accept = input("Would You Like To Insert This Information Into The Database? \nYes or No: ").lower() #ჩვენი სურვილისამებრ ვამატებთ ბაზაში ფილმს.
                            
        if accept == "yes":#შეგვყავს დამატებით ჟანრი , იმ სერიალის რასაც ვამატებთ.
            gen = input("Input Genre of this film: ")
            c.execute('''INSERT INTO series VALUES(?,?)''',(gen,self.jsonstring1[0]["show"]["name"]))
            conn.commit()
            print("Thanks, Have a good day")
        else:
            print("Okay! Goodbye")
        
class AllSeries(): #ამ კლასით , ვეძებთ სასურველ ჟანრს.
    def __init__(self):
        pass

    def series(self):
        error = 0
        
        k = []
        
        self.show = input("Which genre do you want to see: ")
        
        c.execute('''select * from series''')
        # conn.commit()
        for i in c.fetchall():
            k.append(i)
            if self.show == i[0]:
                print(f"{i[0]}: {i[1]}")     
            else:
                error+=1
        
        
        if error == len(k):
            print("Incorret, Try again")
            self.series()
       
            
class Repeater(DatabaseAdder):#ამ კლასით ვიმეორებთ გვინდა თუ არა თავიდან გამეორება ოპერაციის.
    def __init__(self):
        pass
    def repeater(self):
        repeat = input("Do you want to repeat?: ").lower()
        if repeat == "yes":
            DatabaseAdder.adder(self)
        elif repeat == "no":
            print("Thanks, Good Bye")
        else:
            print("Incorrect!, Try Again.")
            self.repeater()
    





database_adder = DatabaseAdder()
database_adder.adder()
series = AllSeries()
series.series()
repeat = Repeater()
repeat.repeater()
conn.close() 