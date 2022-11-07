from flask import Flask, render_template, url_for, request
import sqlite3
import random

conn = sqlite3.connect('Booking_portal.db',check_same_thread=False)
c = conn.cursor()
c.execute('PRAGMA foreign_keys = ON')
conn.commit()

app = Flask(__name__)

 

@app.route('/')
@app.route('/home')

def home():
    return render_template("main.html")

@app.route('/rooms',methods=['POST','GET'])
def rooms():
    return render_template("rooms.html")

@app.route('/confirm',methods=['POST','GET'])
def confirm():
    global Book_id
    Book_id = "B" + str(random.randint(1,1000))
    return render_template("book2.html",Book_id=Book_id)

@app.route('/Book_proceed2',methods=['POST','GET'])
def Book_proceed2():
    output_2 = request.form.to_dict()
    global Rooms,persons,Arr_date,Dep_date,avail_room,C_ID
    C_ID = output_2["C_id"]
    Rooms=output_2["Rooms"]
    persons=output_2["number"]
    Arr_date = output_2["date1"]
    Dep_date = output_2["date2"]
    print(Arr_date)
    print(Dep_date)
    print(Rooms)
    c.execute("Select room_no from Room where room_type=:Rooms and room_no not in(Select distinct(room_no) from Booking where (arrival >= :Arr_date and arrival <= :Dep_date) or (departure >= :Arr_date and departure <=:Dep_date) or (arrival >= :Arr_date and departure <=:Dep_date))limit 1",{'Rooms':Rooms,'Arr_date':Arr_date,'Dep_date':Dep_date})
    avail_room = c.fetchall()
    if(avail_room):
        avail_room = avail_room[0][0]
        print(avail_room)
        return render_template("book_confirm.html",Rooms=Rooms,C_id=C_ID,Book_id=Book_id,number=persons,date1=Arr_date,date2=Dep_date,room_no=avail_room)
    else:
        return render_template("book_issue.html")

@app.route('/register',methods=['POST','GET'])
def register():
    global C_ID 
    C_ID = "C" + str(random.randint(1,1000))
    return render_template("bb.html",C_id=C_ID)
   
    
@app.route('/Customer_reg',methods=['POST','GET'])
def Customer_reg():
    output_1 = request.form.to_dict()
    f_name = output_1["F_name"]
    l_name = output_1["L_name"]
    gender = output_1["Gender"]
    age = output_1["Age"]
    nationality = output_1["Nationality"]
    address = output_1["Address"]
    contact = output_1["Contact_no"]
    email = output_1["email"]
    print(age)
    print(C_ID)
    c.execute("Insert into Customer values(:C_id,:F_name,:L_name,:gender,:age,:nation,:address,:email,:contact)",{'C_id':C_ID,'F_name':f_name,'L_name':l_name,'gender':gender,'age':age,'nation':nationality,'address':address,'email':email,'contact':contact})
    conn.commit()
    global Book_id
    Book_id = "B" + str(random.randint(1,1000))
    return render_template("book.html",C_id=C_ID,Book_id=Book_id)


@app.route('/Book_proceed',methods=['POST','GET'])
def Book_proceed():
    output_2 = request.form.to_dict()
    global Rooms,persons,Arr_date,Dep_date,avail_room
    Rooms=output_2["Rooms"]
    persons=output_2["number"]
    Arr_date = output_2["date1"]
    Dep_date = output_2["date2"]
    print(Arr_date)
    print(Dep_date)
    print(Rooms)
    c.execute("Select room_no from Room where room_type=:Rooms and room_no not in(Select distinct(room_no) from Booking where (arrival >= :Arr_date and arrival <= :Dep_date) or (departure >= :Arr_date and departure <=:Dep_date) or (arrival >= :Arr_date and departure <=:Dep_date))limit 1",{'Rooms':Rooms,'Arr_date':Arr_date,'Dep_date':Dep_date})
    avail_room = c.fetchall()
    if(avail_room):
        avail_room = avail_room[0][0]
        print(avail_room)
        return render_template("book_confirm.html",Rooms=Rooms,C_id=C_ID,Book_id=Book_id,number=persons,date1=Arr_date,date2=Dep_date,room_no=avail_room)
    else:
        return render_template("book_issue.html")

@app.route('/Book_confirm',methods=['POST','GET'])
def Book_confirm():
    c.execute("Insert into Booking values(:Book_id,:C_id,:room_no,:Arr_date,:Dep_date,:number)",{'Book_id':Book_id,'C_id':C_ID,'room_no':avail_room,'Arr_date':Arr_date,'Dep_date':Dep_date,'number':persons})
    conn.commit()
    return render_template('book_success.html')

@app.route('/Billing',methods=['POST','GET'])
def Billing():
    return render_template('Billing.html')

@app.route('/Billing2',methods=['POST','GET'])
def Billing2():
    output_3 = request.form.to_dict()
    global Cust_id,Book_id
    Cust_id = output_3["C_id"]
    Book_id = output_3["Book_no"]
    print(Cust_id)
    print(Book_id)
    c.execute("Select Bill_no from Booking where Bill_no = :Book_id and C_id=:Cust_id",{'Book_id':Book_id,'Cust_id':Cust_id})
    output_4 = c.fetchall()
    if(output_4):
        c.execute("Select room_no,room_type,rent from Room where room_no is (Select room_no from Booking where Bill_no = :Book_id and C_id=:Cust_id)",{'Book_id':Book_id,'Cust_id':Cust_id})
        room_info = c.fetchall()
        global room_no, room_rent, room_type, arr,days,total,gst
        room_no = room_info[0][0]
        room_type = room_info[0][1]
        room_rent = room_info[0][2]
        print(room_no)
        print(room_rent)
        print(room_type)
        c.execute("Select arrival,ROUND(JULIANDAY(departure) - JULIANDAY(arrival)) as days_stayed from Booking where Bill_no = :Book_id",{'Book_id':Book_id})
        Book_info = c.fetchall()
        arr = Book_info[0][0]
        days = Book_info[0][1]
        print(arr)
        print(days)
        gst = 0.1*room_rent
        print(gst)
        total = (int(days) * room_rent) + gst
        print(total)
        return render_template('Billing2.html',Book_id = Book_id,arr = arr,room_type = room_type,rate = room_rent,gst=gst,days=days,total=total)
    else:
        return render_template('Billing_issue.html')

@app.route('/Generate_Bill',methods=['POST','GET'])
def Generate_Bill():
    output_4 = request.form.to_dict()
    payment = output_4["payment"]
    print(payment)
    c.execute("Select f_name,l_name from Customer where C_id is (Select C_id from Booking where Bill_no = :Book_id)",{'Book_id':Book_id})
    name = c.fetchall()
    fname = name[0][0]
    lname = name[0][1]
    name = fname + "_" + lname
    c.execute("Insert into Billing values(:Book_id,:arr,:room_type,:rate,:gst,:days,:total,:payment)",{'Book_id':Book_id,'arr':arr,'room_type':room_type,'rate':room_rent,'gst':gst,'days':days,'total':total,'payment':payment})
    conn.commit()
    c.execute("Select * from Billing")
    print(c.fetchall())
    return render_template('print_bill.html',Book_id = Book_id,name = name,arr = arr,room_type = room_type,rate = room_rent,gst=gst,days=days,total=total,payment=payment)

@app.route('/result',methods=['POST', 'GET'])
def result():
    output = request.form.to_dict()
    print(output)
    name = output["name"]
    #print(name)
    #c.execute("select * from Hotel")
    #print(c.fetchall())
    c.execute("Select Hotel_name from Hotel where Hotel_name=:Hotel_name",{'Hotel_name' : name})
    hotel_name = c.fetchall()
    if(hotel_name):
        print(hotel_name[0][0])
        return render_template('book.html', name = hotel_name[0][0])
    else:
        return render_template('book_issue.html')
    




if __name__ == "__main__":
    app.run(debug=True)