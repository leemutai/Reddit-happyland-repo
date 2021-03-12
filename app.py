from flask import Flask
from flask import render_template
from flask import request
import pymysql
from flask import redirect,session

app=Flask(__name__)

@app.route('/')
def homepage():
    return render_template('Home.html')
@app.route('/header')
def header():
    return render_template('header.html')
@app.route('/footer')
def footer():
     return render_template('footer.html')
@app.route('/services')
def services():
    return render_template('services.html')
@app.route('/rooms')
def rooms():
    return render_template('roomsandsuites.html')
@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/registration',methods=['POST','GET'])
def register():
    if request.method=='POST':
        Id_number=request.form['national_id']
        username = request.form['username']
        password = request.form['password']
        email_address= request.form['email']
        location = request.form['location']
        phone_number=request.form['number']


        conn=pymysql.connect("localhost",'root',"",'REDDIT_PROJECT')
        cursor = conn.cursor()
        insert_query = "INSERT INTO registration (Id_Number,Username,Password,Email_Address,Location,Phone_Number) VALUES(%s, %s, %s, %s, %s,%s)"
        try:
            #lets execute the query
            cursor.execute(insert_query,(Id_number,username,password,email_address,location,phone_number))

            #commit/apply changes to db
            conn.commit()
            return render_template('Registration.html', msg='Registration successful')
        except:
            conn.rollback()
            return render_template('Registration.html', msg='Registration failed')
    else:
        return render_template("Registration.html")

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        conn=pymysql.connect("localhost","root", "", "REDDIT_PROJECT")
        cursor= conn.cursor()
        select_query="SELECT Username, Password   FROM registration WHERE Username =%s AND Password =%s"
        cursor.execute(select_query, (username,password))
        if cursor.rowcount==0:
            return render_template('login.html', error_msg='No account found,Login Failed')
        elif cursor.rowcount==1:
            return redirect('/registration')
            #return render_template('login.html',success_msg='Account found,Login Successful')
        else:
            return render_template('login.html', error='oops!!something went wrong')
    else:
        return render_template('login.html')


@app.route('/checkin',methods=['POST','GET'])
def checkin():
    if request.method=='POST':
        FullNames=request.form['fullname']
        email_address = request.form['email']
        phone = request.form['phone']
        nationality=request.form['nationality']
        address= request.form['address']
        checkin_Date = request.form['date']
        checkin_Time = request.form['time']
        Room_No=request.form['room']
        checkout_Date = request.form['checkoutdate']
        checkin_time = request.form['checkouttime']


        conn=pymysql.connect("localhost",'root',"",'REDDIT_PROJECT')
        cursor = conn.cursor()
        insert_query = "INSERT INTO Checkin (Fullnames,Email_Address,Phone,Nationality,Address,Checkin_date," \
                       "checkin_time,room_no,checkout_date,checkout_time,Checkinstatus) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cursor.execute(insert_query,(FullNames,email_address,phone,nationality,address,checkin_Date,checkin_Time,Room_No,checkout_Date, checkin_time,True))

            #commit/apply changes to db
        conn.commit()
        return render_template('Checkin.html', msg='Checkin successful')
        # except:
        #     conn.rollback()
        #     return render_template('Checkin.html', msg='Checkin failed')
    else:
        return render_template("Checkin.html")


@app.route("/search", methods=['POST','GET'])
def search():
    if request.method=='POST':
        Id_Number=request.form['national_id']
        conn = pymysql.connect("localhost",'root',"",'REDDIT_PROJECT')
        cursor = conn.cursor()

        sql_query = "SELECT * FROM registration WHERE Id_Number=%s"
        cursor.execute(sql_query, (Id_Number))
        if cursor.rowcount < 1:
            return render_template('search.html', msg='No record found, the table is empty')
        else:
            row=cursor.fetchone()
            return render_template('search.html', row=row)
    else:
        return render_template('search.html')

@app.route('/checkout',methods=['POST','GET'])
def checkout():
    if request.method=='POST':
        phone= request.form['number']
        conn = pymysql.connect ("localhost",'root',"" , 'REDDIT_PROJECT')
        cursor=conn.cursor()

        sql_query="UPDATE Checkin SET Checkinstatus=%s WHERE Phone=%s"
        cursor.execute(sql_query , (False,phone))
        conn.commit()
        if cursor.rowcount < 1:
            return render_template('checkout.html', msg='No record found, the table is empty')
        else:
           # row = cursor.fechtone()
            return render_template('checkout.html', msg='You have been checked out')
    else:
        return render_template('checkout.html')


@app.route('/viewcheckin')
def view():
    conn=pymysql.connect("localhost",'root',"",'REDDIT_PROJECT')
    cursor=conn.cursor()

    sql_query="SELECT * FROM Checkin"
    cursor.execute(sql_query)
    if cursor.rowcount<1:
         return render_template('viewcheckin.html',msg='No record found, the table is empty')
    else:
         rows=cursor.fetchall()

         return render_template('viewcheckin.html',rows=rows)

@app.route ('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')








if __name__=='__main__':
    app.run(debug=True)
