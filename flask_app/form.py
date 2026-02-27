from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'sachin@686',
    'database': 'HTMLFORM'
}

def get_db_connection():
    """Establishes a database connection."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@app.route('/')
def index():
    """Renders the form page."""
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    """Handles form submission and inserts data into the database."""
    if request.method == 'POST':
        name=request.form['username']
        
        email = request.form['email']

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
            val = (name, email)
            cursor.execute(sql, val)
            conn.commit()
            cursor.close()
            conn.close()
            return redirect(url_for('display_users'))
    return redirect(url_for('index'))

@app.route('/users')
def display_users():
    """Fetches all users from the database and displays them."""
    conn = get_db_connection()
    users = []
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, email FROM users")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
    return render_template('display.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)