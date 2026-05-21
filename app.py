from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime
import qrcode
import os

app = Flask(__name__)

# Crear BD
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT,
        placa TEXT
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS registros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cedula TEXT,
        placa TEXT,
        hora_ingreso TEXT,
        hora_salida TEXT,
        tipo TEXT
    )''')

    conn.commit()
    conn.close()

init_db()

# HOME
@app.route('/')
def index():
    return render_template('index.html')

# HU1 Registro
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        cedula = request.form['cedula']
        placa = request.form['placa']

        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO usuarios (cedula, placa) VALUES (?, ?)", (cedula, placa))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('registro.html')

# HU2 + HU5 + HU6 Ingreso con carnet
@app.route('/ingreso', methods=['POST'])
def ingreso():
    cedula = request.form['cedula']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM usuarios WHERE cedula=?", (cedula,))
    user = c.fetchone()

    if user:
        hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        c.execute("INSERT INTO registros (cedula, placa, hora_ingreso, tipo) VALUES (?, ?, ?, ?)",
                  (cedula, user[2], hora, "carnet"))
        conn.commit()
        conn.close()

        return "Ingreso autorizado - Barrera abierta"
    else:
        return "Usuario no encontrado"

# HU3 + HU4 Registro manual + QR
@app.route('/manual', methods=['POST'])
def manual():
    cedula = request.form['cedula']
    placa = request.form['placa']

    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("INSERT INTO registros (cedula, placa, hora_ingreso, tipo) VALUES (?, ?, ?, ?)",
              (cedula, placa, hora, "qr"))

    conn.commit()
    conn.close()

    # Generar QR
    data = f"{cedula}-{hora}"
    img = qrcode.make(data)

    path = f"static/qr_{cedula}.png"
    img.save(path)

    return f"QR generado: <img src='/{path}'>"

# HU10 Salida carnet
@app.route('/salida_carnet', methods=['POST'])
def salida_carnet():
    cedula = request.form['cedula']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        UPDATE registros
        SET hora_salida=?
        WHERE cedula=? AND hora_salida IS NULL
    """, (hora, cedula))

    conn.commit()
    conn.close()

    return "Salida registrada - Barrera abierta"

# HU11 Salida QR
@app.route('/salida_qr', methods=['POST'])
def salida_qr():
    cedula = request.form['cedula']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    c.execute("""
        UPDATE registros
        SET hora_salida=?
        WHERE cedula=? AND tipo='qr' AND hora_salida IS NULL
    """, (hora, cedula))

    conn.commit()
    conn.close()

    return "Salida QR registrada"

if __name__ == '__main__':
    app.run(debug=True)
