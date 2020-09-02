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

@app.route("/", methods=['POST', 'GET'])
def home():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        date = request.form['inputdate']
        cur.execute('INSERT INTO date(date) VALUES(%s)', [date])
        cur.connection.commit()
    cur.execute('''
    SELECT date, SUM(protein), SUM(carbohydrates), SUM(fat), SUM(calories) 
    FROM date 
    LEFT JOIN food_date ON date.id = food_date.date_id
    LEFT JOIN foods ON foods.id = food_id 
    GROUP BY date
    ''')
    sum_result = cur.fetchall()
    for item in sum_result:
        item['newdate'] = datetime.strftime(item['date'], '%B %d, %Y')
    return render_template('home.html', sum_result=sum_result)


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



@app.route('/detail', defaults={'date': datetime.now().date()}, methods=['POST', 'GET'])
@app.route('/detail/<date>', methods=['POST', 'GET'])
def detail(date):
    if type(date) == str:
        date = datetime.strptime(date, '%Y-%m-%d').date()
    cur = mysql.connection.cursor()
    cur.execute('SELECT id FROM date WHERE date = %s', [date])
    date_id = int(cur.fetchone()['id'])
    if request.method == 'POST':
        food_id = request.form['food-select']
        if type(food_id) and type(date_id) == int:
            cur.execute('INSERT INTO food_date(food_id, date_id) VALUES(%s, %s)', [food_id, date_id])
            mysql.connection.commit()
    new_date = datetime.strftime(date, '%B %d, %Y')
    cur.execute('SELECT id, name FROM foods ORDER BY name')
    foods = cur.fetchall()
    cur.execute('''SELECT name, protein, carbohydrates, fat, calories
                    FROM foods JOIN food_date 
                    ON foods.id = food_date.food_id 
                    WHERE food_date.date_id = %s''', [date_id])
    food_on_date = cur.fetchall()
    cur.execute('''SELECT SUM(protein), SUM(carbohydrates), SUM(fat), SUM(calories) 
                    FROM food_date JOIN foods 
                    ON foods.id = food_date.food_id 
                    WHERE food_date.date_id = %s''', [date_id])
    sum_result = cur.fetchone()
    return render_template('detail.html', date=new_date, raw_date=date, foods=foods, food_on_date=food_on_date, sum_result=sum_result)
    
if __name__ == "__main__":
    app.run(debug=True)