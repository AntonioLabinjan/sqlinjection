from flask import Flask, request, redirect, render_template_string
import sqlite3

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template_string('''
        <h1>Login</h1>
        <form action="/login" method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        <br>
        <h1>Sign Up</h1>
        <form action="/signup" method="POST">
            Username: <input type="text" name="username"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Sign Up">
        </form>
    ''')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # SQL injection vulnerable query
    c.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()
    
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # SQL injection vulnerable query
    c.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
    user = c.fetchone()
    conn.close()
    
    if user:
        return f"Welcome {username}!"
    else:
        return "Login failed!"

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
