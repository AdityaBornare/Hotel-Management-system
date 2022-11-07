import sqlite3

conn = sqlite3.connect('Booking_portal.db')
c = conn.cursor()
c.execute('PRAGMA foreign_keys = ON')
conn.commit()
'''
c.execute("""CREATE TABLE Room (
            room_no varchar(10) primary key,  
            room_type text, 
            rent number(10)
            )""")

c.execute("Insert into Room values('1','Double Bed room','2000')")

conn.commit()
c.execute("Select * from Room")

c.execute("""CREATE TABLE Customer (
            C_id Varchar(10) primary key, 
            f_name text, 
            l_name text, 
            gender text, 
            age number(5), 
            nationality text, 
            address text, 
            email varchar(20), 
            contact_no number(10)
            )""")
conn.commit()

c.execute("Insert into Customer values('C1','Aditya','Bornare','Male',19,'Indian','Ravet,pune','adityabornare@gmail.com',9764400859)")
conn.commit()

c.execute("Select * from Customer")

c.execute("""CREATE TABLE Booking (
            Bill_no Varchar(10) primary key, 
            C_id varchar(10),
            room_no varchar(10),
            arrival date, 
            departure date,
            no_of_persons number(2),
            constraint Booking_fk2 foreign key(C_id) references Customer(C_id) on update cascade on delete set null,
            constraint Booking_fk3 foreign key(room_no) references Room(room_no) on update cascade on delete set null
            )""")
conn.commit()

c.execute("Insert into Booking values('1','C1','1','2022-10-29','2022-11-01',4)")
conn.commit()

c.execute("Select * from Booking")

c.execute("""CREATE TABLE Billing (
            Bill_no varchar(10) primary key,
            arrival_date date, 
            room_type text, 
            rate number(10), 
            gst number(10), 
            days_stayed number(10), 
            total number(20), 
            payment_mode text 
            )""")
conn.commit()

c.execute("Insert into Billing values('1','2022-10-29','twin bedroom',2000,150,3,2150,'Cash')")
conn.commit()

c.execute("Select * from Booking")

c.execute("Select * from Customer")
output = c.fetchall()
print(output)

c.execute("Delete from Room")
c.execute("Insert into Room values('2','luxurySuite','2500')")
c.execute("Insert into Room values('3','deluxSuite','3500')")
c.execute("Insert into Room values('4','premiersuite','4000')")
c.execute("Insert into Room values('5','SingleBedroom','3000')")
c.execute("Insert into Room values('6','DoubleBedroom','4000')")
conn.commit()
c.execute("Insert into Room values('7','luxurySuite','2500')")
conn.commit()'''

#c.execute("Insert into Booking values('2','C1','2','2022-10-29','2022-11-03',4)")
#conn.commit()
#c.execute("Select room_no from Room where room_type='luxurySuite' and room_no not in(Select distinct(room_no) from Booking where (arrival >= '2022-11-02' and arrival <= '2022-11-05') or (departure >= '2022-11-02' and departure <='2022-11-05') or (arrival >= '2022-11-02' and departure <= '2022-11-05'))limit 1")
c.execute("Select * from Customer where C_id='C459'")
output1 = c.fetchall()
print(output1)
c.execute("Select * from Booking where C_id='C459'")
output2 = c.fetchall()
print(output2)

c.close()

