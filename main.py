from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/payment')
def index1():
    return render_template('payment.html')

@app.route('/result', methods=['POST', 'GET'])
def result():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gymmanagementsystem"
    )

    mycursor = mydb.cursor()

    if request.method == 'POST' and 'confirmpassword' not in request.form:

        singup = request.form
        username = singup['user']
        password = singup['pass']
        mycursor.execute(
            "select * from userregistration where userid='" + username + "' and password='" + password + "'")
        r = mycursor.fetchall()
        count = mycursor.rowcount
        if count == 1 and username == '1':
            headings = ("userid","Name", "PaymentDate", "DueDate", "Amount")
            mycursor.execute("select * from payment")
            data = mycursor.fetchall()
            return render_template("admin.html",data=data,headings=headings)
        elif count == 1 and username != '1':
            return render_template("test.html")
        else:
            return render_template("index.html")


    if request.method == 'POST' and 'confirmpassword' in request.form:
        result = request.form.to_dict()
        firstname = result['firstname']
        lastname = result['lastname']
        email = result['email']
        password = result['password']
        confirmpassword = result['confirmpassword']
        mycursor.execute(
            "insert into userregistration (firstname,lastname,email,password,confirmpassword)values(%s,%s,%s,%s,%s)",
            (firstname, lastname, email, password, confirmpassword))

        mydb.commit()
        mycursor.close()
        return "chl rha hai!"

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
