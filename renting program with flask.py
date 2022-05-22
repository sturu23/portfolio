import sqlite3
from flask import Flask,request

#####------------ DATABASE FOR USERS---------------------#####
conn = sqlite3.Connection('main.db',check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users(
            USER_ID integer PRIMARY KEY,
            USER_NAME char(9) NOT NULL ,
            USER_PASSWORD char(9) NOT NULL ,
            USER_CREATED_DATE date default current_timestamp)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS companies(
        COMPANY_ID integer PRIMARY KEY,
        COMPANY_NAME text)''')
conn.commit()

c.execute('''CREATE TABLE IF NOT EXISTS places(
        PLACE_ID integer PRIMARY KEY,
        COMPANY_ID integer,
        RENTED_BY integer,
        RENT_PLACE text,
        RENT_PRICE integer,
        PLACE_RENTED bool DEFAULT false,
        RENT_PLACE_CREATED date default current_timestamp,
        FOREIGN KEY(RENTED_BY) REFERENCES users(USER_ID),
        FOREIGN KEY(COMPANY_ID) REFERENCES companies(COMPANY_ID))''')
conn.commit()


app = Flask(__name__)




@app.route('/users',methods=['POST'])
def register():
    name = request.args.get('user_name')
    password = request.args.get('user_password')
    
    if len(name) == 0 or len(password) == 0:
        return {"message":"Failed,Try Again"}  
    c.execute('''INSERT INTO users(USER_NAME,USER_PASSWORD) values(?,?)''',(name,password))
    conn.commit()
    return {"message":"Register Completed!"}




    
@app.route('/companies', methods=['POST'])
def add_company():
    company_name = request.args.get('company_name')

    if len(company_name) == 0:
        return {"message":"Failed,Try Again"}
    c.execute('''INSERT INTO companies(COMPANY_NAME) values(?)''',(company_name,))
    conn.commit()
    return {"message":"Company Registered!"}




@app.route('/places', methods=['POST'])
def add_place():
    company_id = request.args.get('company_id')
    rent_place = request.args.get('rent_place')
    rent_price = request.args.get('rent_price')

    c.execute('''SELECT COMPANY_ID from companies where COMPANY_ID = ?''',(company_id))
    check = c.fetchall()
    for i in check:
        if check[0] == i:
            print(i)
            c.execute('''INSERT INTO places(COMPANY_ID,RENT_PLACE,RENT_PRICE) VALUES(?,?,?)''',(company_id,rent_place,rent_price))
            conn.commit()
            return {"message":"Place Registered!"}

    return {"message":"This company does not exist"}
   



@app.route('/rent', methods=['POST'])
def user_rent():
    place_id = request.args.get('place_id')
    user_id = request.args.get('user_id')

    c.execute('''SELECT PLACE_RENTED from places where PLACE_ID = ?''',(place_id,))
    check = c.fetchall()
    if check[0][0] == 0:
        c.execute('''update places set RENTED_BY =?,PLACE_RENTED=? where PLACE_ID = ? AND PLACE_RENTED = ?''',(user_id,True,place_id,False))
        conn.commit()
        return {"message":"Rented Successfully!"}
    return {"message":"Error!"}    





@app.route('/update-place',methods=['PUT'])
def update():
    place_id = request.args.get('place_id')
    rent_place = request.args.get('rent_place')
    rent_price = request.args.get('rent_price')
    
    c.execute('''SELECT PLACE_RENTED from places where PLACE_ID = ?''',(place_id,))
    check = c.fetchall()
    if check[0][0] == 0:
        c.execute('''UPDATE places set RENT_PLACE =?,RENT_PRICE=? WHERE place_id = ?''',(rent_place,rent_price,place_id))
        conn.commit()
        return {"message":"Place and price updated"}
    return {"message":"This place is rented! You can not"}





@app.route('/delete-place',methods=['DELETE'])
def delete():
    place_id = request.args.get('place_id')

    c.execute('''SELECT PLACE_ID from places where PLACE_ID = ?''',(place_id,))  
    check = c.fetchall()
    for i in check:
        if check[0][0] == i[0]:
            c.execute('''DELETE FROM places where PLACE_ID = ?''',(place_id,))
            conn.commit()
            return {"message":"Deleted successfully!"}

    return {"message":"This place does not exist!"}


#########################################################################################################

@app.route('/delete-rent',methods=['PUT'])
def delete_rent():
    place_id = request.args.get('place_id')
    rented_by = request.args.get('rented_by')
   

    c.execute('''SELECT PLACE_RENTED from places WHERE PLACE_ID =? and RENTED_BY =?''',(place_id,rented_by))
    conn.commit()
    rent = c.fetchall()
    print(rent)

    if rent == []:
        print("Sworia")
    elif rent[0][0] == True:
        c.execute('''UPDATE places set RENTED_BY=?,PLACE_RENTED=? where PLACE_ID =?''',(None,False,place_id))
        conn.commit()
        return {"message":"Rent Removed Successfuly!"}
    return {'message':'Failed'}

##########################################################################################################

@app.route('/get-user-data',methods=['GET'])
def user_data():
    get_users = []
    c.execute('SELECT * FROM users')
    conn.commit()
    all = c.fetchall()
    for row in all:
        get_users.append({"user_id":row[0],"user_name":row[1],"user_password":row[2],"create_time":row[3]})

    return {"data of users":get_users}


@app.route('/get-user-data/<id>',methods=['GET'])
def one_user_data(id):
    get_user = []
    c.execute('''SELECT * from users where USER_ID =?''',(id))
    conn.commit()
    all = c.fetchall()
    for row in all:
        get_user.append({"user_id":row[0],"user_name":row[1],"user_password":row[2],"create_time":row[3]})

    return {"one user data":get_user}


@app.route('/get-companies-data',methods=['GET'])
def company_data():
    get_companies = []
    c.execute('''SELECT * FROM companies''')
    conn.commit()
    all = c.fetchall()
    for row in all:
        get_companies.append({"company_id":row[0],"company_name":row[1]})
    
    return {"companies data":get_companies}

@app.route('/get-companies-data/<company_id>',methods=['GET'])
def one_company_data(company_id):
    get_company = []
    c.execute('''SELECT * FROM companies where COMPANY_ID=?''',(company_id))
    conn.commit()
    all = c.fetchall()
    for row in all:
        get_company.append({"company_id":row[0],"company_name":row[1]})
    
    return {"company data":get_company}

@app.route('/places-data',methods=['GET'])
def all_places_data():
    all_place_data = []
    c.execute('''SELECT * FROM places''')
    all = c.fetchall()
    for row in all:
        all_place_data.append({"place_id":row[0],"company_id":row[1],"rented_by":row[2],"rent_place":row[3],"rent_price":row[4],"place_rented":row[5],"rent_place_created":row[6]})

    return {"places data":all_place_data}

    
    
@app.route('/places-data/<place_id>',methods=['GET'])
def places_data(place_id):
    place_data = []
    c.execute('''SELECT * FROM places where PLACE_ID = ?''',(place_id))
    conn.commit()
    all = c.fetchall()
    for row in all:
        place_data.append({"place_id":row[0],"company_id":row[1],"rented_by":row[2],"rent_place":row[3],"rent_price":row[4],"place_rented":row[5],"rent_place_created":row[6]})

    return {"places data":place_data}
        


@app.route('/rented-place-data',methods=['GET'])
def rented_place_data():
    rented_data = []
    c.execute('''SELECT * FROM places where PLACE_RENTED = 1''')
    conn.commit()
    all = c.fetchall()
    for row in all:
        rented_data.append({"place_id":row[0],"company_id":row[1],"rented_by":row[2],"rent_place":row[3],"rent_price":row[4],"place_rented":row[5],"rent_place_created":row[6]})

    return {"Rented place data":rented_data}
    

@app.route('/rented-place-data/<id>',methods=['GET'])
def one_rented_place_data(id):
    rented_data = []
    c.execute('''SELECT * FROM places where PLACE_RENTED = 1 and PLACE_iD =?''',(id))
    conn.commit()
    all = c.fetchall()
    for row in all:
        rented_data.append({"place_id":row[0],"company_id":row[1],"rented_by":row[2],"rent_place":row[3],"rent_price":row[4],"place_rented":row[5],"rent_place_created":row[6]})
        
    return {"Rented place data":rented_data}

@app.route('/for-rent-places',methods=['GET'])
def for_rent_places():
    rent_places = []
    c.execute('''SELECT * FROM places where PLACE_RENTED = 0''')
    conn.commit()
    all = c.fetchall()
    for row in all:
        rent_places.append({"place_id":row[0],"company_id":row[1],"rented_by":row[2],"rent_place":row[3],"rent_price":row[4],"place_rented":row[5],"rent_place_created":row[6]})

    return {"for rent places data":rent_places}


@app.route('/for-rent-places/<rent_place_id>',methods=['GET'])
def one_for_rent_places(rent_place_id):
    rent_place = []
    c.execute('''SELECT * FROM places where PLACE_RENTED = 0 and  PLACE_ID = ?''',(rent_place_id))
    conn.commit()
    all = c.fetchall()
    for row in all:
        rent_place.append({"place_id":row[0],"company_id":row[1],"rented_by":row[2],"rent_place":row[3],"rent_price":row[4],"place_rented":row[5],"rent_place_created":row[6]})

    return {"one rent place data":rent_place}   

if __name__ == '__main__':
    app.run(debug=True)