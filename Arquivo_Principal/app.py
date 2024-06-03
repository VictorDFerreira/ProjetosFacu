from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database connection function using mysql.connector
def get_db_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='57221633',  # Change to your MySQL password
            database='login2'
        )
    except Error as e:
        print("Error connecting to MySQL", e)
        return None

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/inicio', methods=['GET', 'POST'])
def inicio():
    conn = get_db_connection()
    appointments = []
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, period, time, services FROM appointments")
        appointments = cursor.fetchall()
        cursor.close()
        conn.close()

    return render_template('inicio.html', appointments=appointments)

@app.route('/home', methods=['GET', 'POST'])
def agendamento():
    if request.method == 'POST':
        date = request.form['date']
        period = request.form['period']
        time = request.form['time']
        services = ', '.join(request.form.getlist('service'))

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO appointments (date, period, time, services) VALUES (%s, %s, %s, %s)", 
                           (date, period, time, services))
            conn.commit()
            cursor.close()
            conn.close()
<<<<<<< Updated upstream
            return render_template('confirmar.html', date=date, time=time, services=services.split(', '))
=======
        return redirect(url_for('inicio'))

>>>>>>> Stashed changes
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
            stored_password = cursor.fetchone()
            conn.close()
            if stored_password and bcrypt.checkpw(password, stored_password[0].encode('utf-8')):
<<<<<<< Updated upstream
                return render_template ('home.html')
=======
                return render_template('inicio.html')
>>>>>>> Stashed changes
            else:
                flash('Invalid username or password')
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
            flash('Passwords do not match!')
            return redirect(url_for('register'))

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO users (first_name, last_name, email, password) VALUES (%s, %s, %s, %s)", 
                               (first_name, last_name, email, hashed_password))
                conn.commit()
                flash('User registered successfully!')
                return redirect(url_for('login'))
            except mysql.connector.Error as err:
                flash(f'Error registering user: {err}')
                return redirect(url_for('register'))
            finally:
                conn.close()
    return render_template('register.html')

# Função para deletar um agendamento
@app.route('/delete_appointment/<int:appointment_id>', methods=['POST'])
def delete_appointment(appointment_id):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
            conn.commit()
            flash('Agenda deletada com sucesso!')
        except mysql.connector.Error as err:
            flash(f'Error deleting appointment: {err}')
        finally:
            cursor.close()
            conn.close()
    return redirect(url_for('inicio'))

# Função para editar um agendamento
@app.route('/edit_appointment/<int:appointment_id>', methods=['GET', 'POST'])
def edit_appointment(appointment_id):
    conn = get_db_connection()
    if conn is not None:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, period, time, services FROM appointments WHERE id = %s", (appointment_id,))
        appointment = cursor.fetchone()
        cursor.close()
        conn.close()

    if request.method == 'POST':
        date = request.form['date']
        period = request.form['period']
        time = request.form['time']
        services = ', '.join(request.form.getlist('service'))

        conn = get_db_connection()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE appointments
                SET date = %s, period = %s, time = %s, services = %s
                WHERE id = %s
            """, (date, period, time, services, appointment_id))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Agenda editada com sucesso!')
            return redirect(url_for('inicio'))

    return render_template('edit_appointment.html', appointment=appointment)

if __name__ == "__main__":
    app.run(debug=True)
