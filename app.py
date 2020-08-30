from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'foodtracker'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/add_food', methods=['POST', 'GET'])
def add_food():
    if request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT name, protein, carbohydrates, fat FROM foods')
        result = cur.fetchall()
        print(result[0][0])
        return render_template('add_food.html')
    



@app.route('/detail')
def detail():
    return render_template('detail.html')
    
if __name__ == "__main__":
    app.run(debug=True)