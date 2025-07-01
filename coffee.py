from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3, os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  


def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL)''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = c.fetchone()
        conn.close()
        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            return redirect('/dashboard')
        return "Invalid credentials"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        except sqlite3.IntegrityError:
            return "Username already exists"
        conn.close()
        return redirect('/dashboard')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

@app.route('/order', methods=['POST'])
def order():
    if 'user_id' not in session:
        return jsonify({'message': 'Please login to place an order'})
    data = request.get_json()
    coffee = data.get('coffee')
    return jsonify({'message': f'Thank you for ordering {coffee}!'})

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        return redirect('/login')
    return render_template('cart.html')

if __name__ == '__main__':
    app.run(debug=True)



