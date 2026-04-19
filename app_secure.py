from flask import Flask, request, render_template_string
import sqlite3
import hashlib
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Secure parameterized query — prevents SQL injection
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            return "Login successful!"
        else:
            return "Invalid credentials"

    return '''
    <form method="post">
        Username: <input type="text" name="username" required><br>
        Password: <input type="password" name="password" required><br>
        <input type="submit" value="Login">
    </form>
    '''

@app.route('/')
def home():
    return '<h1>Secure Web App Demo</h1><a href="/login">Login</a>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
