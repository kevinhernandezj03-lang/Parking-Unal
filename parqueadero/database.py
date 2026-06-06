import sqlite3

# CONECTAR O CREAR BASE DE DATOS

conn = sqlite3.connect('database.db')

c = conn.cursor()

# =========================
# TABLA USUARIOS
# =========================

c.execute("""

CREATE TABLE IF NOT EXISTS usuarios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT NOT NULL,

    carnet TEXT UNIQUE NOT NULL,

    placa TEXT NOT NULL,

    tipo_vehiculo TEXT NOT NULL

)

""")

# =========================
# TABLA REGISTROS
# USUARIOS REGISTRADOS
# =========================

c.execute("""

CREATE TABLE IF NOT EXISTS registros (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    carnet TEXT NOT NULL,

    hora_entrada TEXT,

    hora_salida TEXT,

    estado TEXT

)

""")

# =========================
# TABLA VISITANTES
# INGRESO MANUAL
# =========================

c.execute("""

CREATE TABLE IF NOT EXISTS visitantes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    cedula TEXT NOT NULL,

    placa TEXT NOT NULL,

    ticket TEXT UNIQUE NOT NULL,

    hora_entrada TEXT,

    hora_salida TEXT,

    estado TEXT

)

""")

# GUARDAR CAMBIOS

conn.commit()

# CERRAR CONEXION

conn.close()

print("Base de datos creada correctamente")