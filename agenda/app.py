from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '57221633'  # Altere para a senha do seu MySQL
app.config['MYSQL_DB'] = 'barbearia'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('schedule.html')

@app.route('/schedule', methods=['POST'])
def schedule():
    date = request.form['date']
    period = request.form['period']
    time = request.form['time']
    services = ', '.join(request.form.getlist('service'))
    
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO appointments (date, period, time, services) VALUES (%s, %s, %s, %s)", (date, period, time, services))
    mysql.connection.commit()
    cur.close()
    
    return render_template('confirmation.html', date=date, time=time, services=services.split(', '))

if __name__ == "__main__":
    app.run(debug=True)



