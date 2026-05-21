from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# CREAR BASE DE DATOS

def init_db():

    conn = sqlite3.connect('database.db')

    c = conn.cursor()

    c.execute('''

        CREATE TABLE IF NOT EXISTS usuarios (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            cedula TEXT,

            placa TEXT,

            carnet TEXT

        )

    ''')

    conn.commit()

    conn.close()

init_db()

# PAGINA REGISTRO

@app.route('/registro')

def registro_page():

    return render_template('registro.html')

# GUARDAR USUARIO

@app.route('/registro', methods=['POST'])

def registrar_usuario():

    cedula = request.form['cedula']

    placa = request.form['placa']

    carnet = request.form['carnet']

    conn = sqlite3.connect('database.db')

    c = conn.cursor()

    c.execute("""

        INSERT INTO usuarios
        (cedula, placa, carnet)

        VALUES (?, ?, ?)

    """, (cedula, placa, carnet))

    conn.commit()

    conn.close()

    return redirect('/registro')

# INICIAR SERVIDOR

if __name__ == '__main__':

    app.run(debug=True)
