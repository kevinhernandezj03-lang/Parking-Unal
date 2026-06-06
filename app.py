from flask import Flask, render_template, request
import sqlite3
import random
from datetime import datetime

app = Flask(__name__)

# =========================
# PAGINA REGISTRO
# =========================

@app.route('/')
def home():
    return render_template('registro.html')


# =========================
# REGISTRAR USUARIO
# =========================

@app.route('/registro', methods=['POST'])
def registrar():

    nombre = request.form['nombre']
    carnet = request.form['carnet']
    placa = request.form['placa']
    tipo_vehiculo = request.form['tipo_vehiculo']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO usuarios
        (nombre, carnet, placa, tipo_vehiculo)

        VALUES (?, ?, ?, ?)
    """, (nombre, carnet, placa, tipo_vehiculo))

    conn.commit()
    conn.close()

    return render_template(
        'registro.html',
        mensaje='✅ Usuario registrado exitosamente'
    )


# =========================
# PAGINA LECTOR
# =========================

@app.route('/lector')
def lector():
    return render_template('lector.html')


# =========================
# VALIDAR CARNET O TICKET
# =========================

@app.route('/validar', methods=['POST'])
def validar():

    codigo = request.form['codigo']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # =========================
    # BUSCAR USUARIO POR CARNET
    # =========================

    c.execute("""
        SELECT *
        FROM usuarios
        WHERE carnet = ?
    """, (codigo,))

    usuario = c.fetchone()

    # =========================
    # SI ES USUARIO REGISTRADO
    # =========================

    if usuario:

        c.execute("""
            SELECT *
            FROM registros
            WHERE carnet = ?
            AND estado = 'dentro'
        """, (codigo,))

        registro = c.fetchone()

        # ENTRADA
        if not registro:

            c.execute("""
                INSERT INTO registros
                (carnet, hora_entrada, estado)

                VALUES (?, ?, ?)
            """, (
                codigo,
                hora,
                'dentro'
            ))

            mensaje = '✅ Entrada registrada |  Abriendo barrera automáticamente'

        # SALIDA
        else:

            c.execute("""
                UPDATE registros

                SET hora_salida = ?,
                    estado = 'fuera'

                WHERE id = ?
            """, (
                hora,
                registro[0]
            ))

            mensaje = '✅ Salida registrada |  Abriendo barrera automáticamente'

        conn.commit()
        conn.close()

        return render_template(
            'lector.html',
            mensaje=mensaje
        )

    # =========================
    # BUSCAR TICKET VISITANTE
    # =========================

    c.execute("""
        SELECT *
        FROM visitantes

        WHERE ticket = ?
        AND estado = 'dentro'
    """, (codigo,))

    visitante = c.fetchone()

    if visitante:

        c.execute("""
            UPDATE visitantes

            SET hora_salida = ?,
                estado = 'fuera'

            WHERE id = ?
        """, (
            hora,
            visitante[0]
        ))

        conn.commit()
        conn.close()

        return render_template(
            'lector.html',
            mensaje='✅ Salida autorizada por ticket |  Abriendo barrera automáticamente'
        )

    conn.close()

    return render_template(
        'lector.html',
        mensaje='❌ Carnet o ticket no válido'
    )


# =========================
# PAGINA INGRESO MANUAL
# =========================

@app.route('/manual')
def manual():
    return render_template('manual.html')


# =========================
# REGISTRAR VISITANTE
# =========================

@app.route('/manual_ingreso', methods=['POST'])
def manual_ingreso():

    cedula = request.form['cedula']
    placa = request.form['placa']

    ticket = f"QR-{random.randint(100000,999999)}"

    hora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    c.execute("""
        INSERT INTO visitantes
        (
            cedula,
            placa,
            ticket,
            hora_entrada,
            estado
        )

        VALUES (?, ?, ?, ?, ?)
    """, (
        cedula,
        placa,
        ticket,
        hora,
        'dentro'
    ))

    conn.commit()
    conn.close()

    return render_template(
        'manual.html',
        mensaje='✅ Ingreso exitoso, recoja su ticket',
        ticket=ticket
    )


# =========================

if __name__ == '__main__':
    app.run(debug=True)
