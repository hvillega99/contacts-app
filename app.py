from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "root"
app.config["MYSQL_DB"] = "flaskcontacts"
mysql = MySQL(app)

#root
@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()
    return render_template('index.html',contacts = data)

#agregar
@app.route("/add", methods=["POST"])
def addContact():
    if request.method == 'POST':
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
        (fullname,phone,email))
        mysql.connection.commit()

        return redirect(url_for("index"))
        
#vista de edición
@app.route("/edit/<id>")
def getContact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts WHERE id = {0}'.format(id))
    data = cursor.fetchall()
    return render_template('edit.html',contact = data[0])

#actualizar
@app.route("/update/<id>", methods=["POST"])
def updateContact(id):
    if request.method == 'POST':
        fullname = request.form["fullname"]
        phone = request.form["phone"]
        email = request.form["email"]

        cursor = mysql.connection.cursor()
        cursor.execute("""
        UPDATE contacts 
        SET fullname = %s,
            phone = %s,
            email = %s
        WHERE id = %s
        """,(fullname,phone,email,id))
        mysql.connection.commit()
        return redirect(url_for("index"))

#borrar
@app.route("/delete/<string:id>")
def deleteContact(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(port=3000, debug=True)

