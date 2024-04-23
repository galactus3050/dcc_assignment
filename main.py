from os import name
from flask import Flask, redirect, url_for, request, Response, render_template
from flask_mysqldb import MySQL
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'testing123'
app.config['MYSQL_PASSWORD'] = 'pwd'
app.config['MYSQL_DB'] = 'comeon'

mysql = MySQL(app)
def fetchdata():
    cursor=mysql.connection.cursor()
    cursor.execute('select distinct `name_of_purchaser` from purchase_details')
    name_of_purchaser=cursor.fetchall()
    cursor.close()
    cursor=mysql.connection.cursor()
    cursor.execute('select distinct `name_of_party` from redemption_details')
    name_of_party=cursor.fetchall()
    cursor.close()
    return name_of_purchaser,name_of_party
option_names=["Sr No.","Reference No (URN)","Journal Date","Date of Purchase","Date of Expiry","Name of the Purchaser","Prefix","bond_number","Denominations","Issue Branch Code","Issue Teller","Status"]
@app.route('/', methods = ["POST", "GET"])
def main_page():
    name_of_purchaser,name_of_party=fetchdata()
    return render_template("index.html", name_of_purchaser=name_of_purchaser, name_of_party=name_of_party)


@app.route('/a_1', methods = ["POST", "GET"])
def a_1():
    if request.method == "POST":
        print("HI")
        print(request.method)
        print(request.form["query"])  

        print("TEST")

        cursor = mysql.connection.cursor()
        cursor.execute("select * from purchase_details where `bond_number`= %s", (request.form["query"],))
        data = cursor.fetchall()
        cursor.close()


    else:
        data = []
    name_of_purchaser,name_of_party=fetchdata()
    return render_template("index.html", a_1_data = data,name_of_purchaser=name_of_purchaser, name_of_party=name_of_party)

@app.route('/a_2', methods = ["POST", "GET"])
def a_2():
    name_of_purchaser, name_of_party = fetchdata()
    if request.method == "POST":
        print("HI")
        value = request.form.get('Company')  # Use get() method to avoid KeyError
        print(value)

        print("TEST")
        cursor = mysql.connection.cursor()
        cursor.execute("select `bond_number`,`Denominations`,`dop` from purchase_details where `name_of_purchaser`=%s ", (value,))  # Use 'value' instead of 'request.form["company"]'

        data1 = cursor.fetchall()
        d={}
        for i in range(len(data1)):
            d[data1[i][2]]=d.get(data1[i][2],0)+data1[i][1]
        cursor.close()
        years=list(d.keys())
        amount=list(d.values())
        
    else:
        data1 = []
        years = []
        amount = []
    name_of_purchaser, name_of_party = fetchdata()
    return render_template("index.html", a_2_data=data1, years=years, amount=amount, name_of_purchaser=name_of_purchaser, name_of_party=name_of_party)


@app.route('/a_3', methods = ["POST", "GET"])
def a_3():
    name_of_purchaser, name_of_party = fetchdata()
    if request.method == "POST":
        print("HI")
        value = request.form.get('Company')  # Use get() method to avoid KeyError
        print(value)

        print("TEST")
        cursor = mysql.connection.cursor()
        cursor.execute("select * from redemption_details where `name_of_party`=%s ", (value,))  # Use 'value' instead of 'request.form["company"]'

        data2 = cursor.fetchall()
        cursor.close()
    else:
        data2 = []
    name_of_purchaser, name_of_party = fetchdata()
    return render_template("index.html", a_3_data=data2, name_of_purchaser=name_of_purchaser, name_of_party=name_of_party)

@app.route('/a_4', methods = ["POST", "GET"])
def a_4():
    name_of_purchaser, name_of_party = fetchdata()
    if request.method == "POST":
        print("HI")
        value = request.form.get('Company1')
        print(value)
        print("TEST")
        cursor = mysql.connection.cursor()
        cursor.execute("select `name_of_purchaser`, sum(`Denominations`) as Total_Amount from purchase_details where `bond_number` in (select `bond_number` from redemption_details where `name_of_party` = %s) group by `name_of_purchaser`", (value,))
        data3 = cursor.fetchall()
        cursor.close()
    else:
        data3 = []
    name_of_purchaser, name_of_party = fetchdata()
    return render_template("index.html", a_4_data=data3, name_of_purchaser=name_of_purchaser, name_of_party=name_of_party)

@app.route('/a_5', methods = ["POST", "GET"])
def a_5():
    name_of_purchaser, name_of_party = fetchdata()
    if request.method == "POST":
        print("HI")
        value = request.form.get('Company1')
        print(value)
        print("TEST")
        cursor = mysql.connection.cursor()
        cursor.execute("select `name_of_party`, sum(`Denominations`) as Total_Amount from redemption_details where `bond_number` in (select `bond_number` from purchase_details where `name_of_purchaser` = %s) group by `name_of_party`", (value,))
        data4 = cursor.fetchall()
        cursor.close()
    else:
        data4 = []
    name_of_purchaser, name_of_party = fetchdata()
    return render_template("index.html", a_5_data=data4, name_of_purchaser=name_of_purchaser, name_of_party=name_of_party)


if __name__ == '__main__':
   app.run(host="0.0.0.0", port="80", debug = True) 