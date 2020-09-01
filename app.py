from flask import Flask, render_template, request
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'foodtracker'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/add_food', methods=['POST', 'GET'])
def add_food():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = protein + carbohydrates + fat
        cur.execute('''INSERT INTO foods (name, protein, carbohydrates, fat, calories)
         VALUES (%s, %s, %s, %s, %s)''', [name, protein, carbohydrates, fat, calories])
        mysql.connection.commit()

    cur.execute('SELECT name, protein, carbohydrates, fat, calories FROM foods')
    result = cur.fetchall()
    return render_template('add_food.html', result=result) 



@app.route('/detail', defaults={'date': datetime.now().date()})
@app.route('/detail/<date>', defaults={'date': datetime.now()})
def detail(date):
    new_date = datetime.strftime(date, '%B %d, %Y')
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, name FROM foods ORDER BY name')
    foods = cur.fetchall()
    return render_template('detail.html', date=new_date, foods=foods)
    
if __name__ == "__main__":
    app.run(debug=True)