from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def conectar_banco():
    try:
        return mysql.connector.connect(
            host='localhost',
            database='login',
            user='root',
            password='57221633'
        )
    except Error as e:
        print(f'Erro ao conectar ao banco de dados: {e}')
        return None

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        conn = conectar_banco()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            stored_password = cursor.fetchone()
            conn.close()
            if stored_password and bcrypt.checkpw(password, stored_password[0].encode('utf-8')):
                return render_template('welcome.html')
            else:
                flash('Usuário ou senha não existe!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('As senhas não coincidem!')
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = conectar_banco()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", 
                               (first_name, last_name, email, hashed_password))
                conn.commit()
                flash('Usuário cadastrado com sucesso!')
                return redirect(url_for('login'))
            except mysql.connector.Error as err:
                if err.errno == 1062:
                    flash('Email já cadastrado!')
                else:
                    flash(f'Erro ao cadastrar usuário: {err}')
                return redirect(url_for('register'))
            finally:
                conn.close()
    return render_template('register.html')

@app.route('/home')
def home():
    return 'Você está logado!'

if __name__ == "__main__":
    app.run(debug=True)
