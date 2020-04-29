from flask import Flask,render_template,redirect
from flask import request
from flask_mysqldb import MySQL



app=Flask(__name__)

#configure db
app.config['MYSQL_PORT']=3306
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'Appuser'
app.config['MYSQL_PASSWORD'] = 'sid'
app.config['MYSQL_DB'] = 'StudentDB'

mysql =MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST' and 'submit' in request.form:
        userDetails=request.form
        uid=userDetails['sid']
        name=userDetails['sname']
        age=userDetails['sage']
        dept=userDetails['sdept']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students(id,name,age,dept) VALUES(%s,%s,%s,%s)",(uid,name,age,dept))
        mysql.connection.commit()
        cur.close()
        return redirect('/students')
    elif request.method == 'POST' and 'delete' in request.form:
        userDetails=request.form
        uid=userDetails['sid']
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM students WHERE id=%s",(uid))
        mysql.connection.commit()
        cur.close()
        return redirect('/students')
    return render_template('index.html')

@app.route('/students')
def students():
    cur = mysql.connection.cursor()
    getResult=cur.execute("SELECT * FROM students")
    if getResult > 0:
        userDetails=cur.fetchall()
        return render_template('students.html',userDetails=userDetails)


if __name__ == '__main__':
    app.run(debug=True)

