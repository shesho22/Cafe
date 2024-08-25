# Importación de módulos necesarios
from flask import Flask, request, jsonify, redirect, url_for, make_response
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename
from mysql.connector import connect, Error
from werkzeug.security import generate_password_hash, check_password_hash

# Inicialización de la aplicación Flask
app = Flask(__name__)

# Configuración de CORS para permitir solicitudes desde el origen especificado
CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})

# Configuración de la carpeta para subir archivos y la base de datos
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Configuración de la base de datos con SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:algomuyseguro56789@localhost/juegos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Configuración para la conexión directa a la base de datos
db_config = {
    'user': 'root',
    'password': 'algomuyseguro56789',
    'host': 'localhost',
    'database': 'juegos_db'
}

# Función para verificar la conexión a la base de datos
def check_database_connection():
    try:
        with connect(**db_config) as conn:
            if conn.is_connected():
                return True
    except Error as err:
        print(f"Error: {err}")
        return False

# Función para verificar la sesión del usuario (simulada)
def verificar_sesion():
    return 'token' in request.cookies

# Verificar si el archivo tiene una extensión permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# Función para guardar imágenes en el servidor
def guardar_imagenes(files, referencia_id, tipo):
    imagenes_rutas = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            imagenes_rutas.append(file_path)
            nueva_imagen = Imagen(ruta=file_path)
            
            # Asociar la imagen con el tipo de referencia adecuado
            if tipo == 'juego_mesa':
                nueva_imagen.id_juego_mesa = referencia_id
            elif tipo == 'consola':
                nueva_imagen.id_consola = referencia_id
            elif tipo == 'juego_consola':
                nueva_imagen.id_juego_consola = referencia_id
            
            db.session.add(nueva_imagen)
    
    db.session.commit()
    return imagenes_rutas

# Modelo para usuarios
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Modelo para juegos de mesa
class JuegoDeMesa(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    genero = db.Column(db.String(50))
    instrucciones = db.Column(db.Text)
    
    def convertir(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'genero': self.genero,
            'instrucciones': self.instrucciones,
            'imagenes': [imagen.ruta for imagen in Imagen.query.filter_by(id_juego_mesa=self.id).all()]
        }

# Modelo para consolas
class Consola(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    marca = db.Column(db.String(50))
    detalles = db.Column(db.Text)
    estado = db.Column(db.String(50))
    
    def convertir(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'marca': self.marca,
            'detalles': self.detalles,
            'estado': self.estado,
            'imagenes': [imagen.ruta for imagen in Imagen.query.filter_by(id_consola=self.id).all()]
        }

# Modelo para juegos de consola
class JuegoDeConsola(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(255))
    detalles = db.Column(db.Text)
    estado = db.Column(db.String(50))
    id_consola = db.Column(db.Integer, db.ForeignKey('consola.id'))
    genero = db.Column(db.String(50))
    
    def convertir(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'detalles': self.detalles,
            'estado': self.estado,
            'id_consola': self.id_consola,
            'genero': self.genero,
            'imagenes': [imagen.ruta for imagen in Imagen.query.filter_by(id_juego_consola=self.id).all()]
        }

# Modelo para imágenes
class Imagen(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ruta = db.Column(db.String(255), nullable=False)
    id_juego_mesa = db.Column(db.Integer, db.ForeignKey('juego_de_mesa.id'))
    id_juego_consola = db.Column(db.Integer, db.ForeignKey('juego_de_consola.id'))
    id_consola = db.Column(db.Integer, db.ForeignKey('consola.id'))
    
    def convertir(self):
        return {
            'id': self.id,
            'ruta': self.ruta,
            'id_juego_mesa': self.id_juego_mesa,
            'id_juego_consola': self.id_juego_consola,
            'id_consola': self.id_consola
        }

# Rutas de la aplicación

# Ruta para obtener todos los recursos
@app.route('/api/todos', methods=['GET'])
def obtener_todos():
    juegos_mesa = JuegoDeMesa.query.all()
    consolas = Consola.query.all()
    juegos_consola = JuegoDeConsola.query.all()
    
    # Convertir cada objeto en un diccionario y devolver como JSON
    resultados = {
        'juegos_mesa': [juego_mesa.convertir() for juego_mesa in juegos_mesa],
        'consolas': [consola.convertir() for consola in consolas],
        'juegos_consola': [juego_consola.convertir() for juego_consola in juegos_consola]
    } 
    return jsonify(resultados), 200

# Ruta de inicio
@app.route('/')
def inicio():
    return 'Página de inicio'

# Ruta para cerrar sesión
@app.route('/cerrar_sesion', methods=['POST'])
def cerrar_sesion():
    resp = make_response('Sesión cerrada exitosamente.')
    resp.set_cookie('token', '', expires=0)  # Elimina la cookie de sesión
    return resp

# Ruta protegida que requiere sesión activa
@app.route('/ruta-protegida')
def ruta_protegida():
    if not verificar_sesion():
        return redirect(url_for('inicio'))
    return 'Contenido protegido'

# Ruta para registrar un nuevo usuario
@app.route('/api/registrar_usuario', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if Usuario.query.filter_by(username=username).first():
        return jsonify({'error': 'El nombre de usuario ya existe'}), 400

    nuevo_usuario = Usuario(username=username)
    nuevo_usuario.set_password(password)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({'mensaje': 'Usuario registrado exitosamente'}), 201

# Ruta para iniciar sesión
@app.route('/api/iniciar_sesion', methods=['POST'])
def iniciar_sesion():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    usuario = Usuario.query.filter_by(username=username).first()
    if usuario and usuario.check_password(password):
        resp = make_response(jsonify({'mensaje': 'Sesión iniciada exitosamente'}), 200)
        resp.set_cookie('token', 'some_session_token')  # Simula la asignación de un token de sesión
        return resp

    return jsonify({'error': 'Nombre de usuario o contraseña incorrectos'}), 401

# Ruta para probar la conexión a la base de datos
@app.route('/test_connection', methods=['GET'])
def test_connection():
    if check_database_connection():
        return jsonify({'mensaje': 'Conexión a la base de datos exitosa.'}), 200
    else:
        return jsonify({'mensaje': 'Error al conectar con la base de datos.'}), 500

# Rutas para los juegos de mesa
@app.route('/api/juegos_mesa', methods=['GET'])
def obtener_juegos_mesa():
    juegos_mesa = JuegoDeMesa.query.all()
    return jsonify([juego.convertir() for juego in juegos_mesa]), 200

@app.route('/api/juegos_mesa', methods=['POST'])
def registrar_juego_mesa():
    if not verificar_sesion():
        return redirect(url_for('inicio'))
    data = request.get_json()
    nuevo_juego = JuegoDeMesa(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        genero=data.get('genero'),
        instrucciones=data.get('instrucciones')
    )
    db.session.add(nuevo_juego)
    db.session.commit()
    return jsonify({'mensaje': 'Juego de mesa registrado exitosamente'}), 201

@app.route('/api/juegos_mesa/<int:juego_id>', methods=['DELETE'])
def eliminar_juego_mesa(juego_id):
    if not verificar_sesion():
        return redirect(url_for('inicio'))
    juego = JuegoDeMesa.query.get_or_404(juego_id)
    db.session.delete(juego)
    db.session.commit()
    return jsonify({'mensaje': 'Juego de mesa eliminado exitosamente'}), 200

# Rutas para las consolas
@app.route('/api/consolas', methods=['GET'])
def obtener_consolas():
    consolas = Consola.query.all()
    return jsonify([consola.convertir() for consola in consolas]), 200

@app.route('/api/consolas', methods=['POST'])
def registrar_consola():
    if not verificar_sesion():
        return redirect(url_for('inicio'))
    data = request.get_json()
    nueva_consola = Consola(
        nombre=data.get('nombre'),
        marca=data.get('marca'),
        detalles=data.get('detalles'),
        estado=data.get('estado')
    )
    db.session.add(nueva_consola)
    db.session.commit()
    return jsonify({'mensaje': 'Consola registrada exitosamente'}), 201

@app.route('/api/consolas/<int:consola_id>', methods=['DELETE'])
def eliminar_consola(consola_id):
    if not verificar_sesion():
        return redirect(url_for('inicio'))
    consola = Consola.query.get_or_404(consola_id)
    db.session.delete(consola)
    db.session.commit()
    return jsonify({'mensaje': 'Consola eliminada exitosamente'}), 200

# Rutas para los juegos de consola
@app.route('/api/juegos_consola', methods=['GET'])
def obtener_juegos_consola():
    juegos_consola = JuegoDeConsola.query.all()
    return jsonify([juego.convertir() for juego in juegos_consola]), 200

@app.route('/api/juegos_consola', methods=['POST'])
def registrar_juego_consola():
    if not verificar_sesion():
        return redirect(url_for('inicio'))
    data = request.get_json()
    nuevo_juego_consola = JuegoDeConsola(
        nombre=data.get('nombre'),
        descripcion=data.get('descripcion'),
        detalles=data.get('detalles'),
        estado=data.get('estado'),
        id_consola=data.get('id_consola'),
        genero=data.get('genero')
    )
    db.session.add(nuevo_juego_consola)
    db.session.commit()
    return jsonify({'mensaje': 'Juego de consola registrado exitosamente'}), 201

@app.route('/api/juegos_consola/<int:juego_id>', methods=['DELETE'])
def eliminar_juego_consola(juego_id):
    if not verificar_sesion():
        return redirect(url_for('inicio'))
    juego_consola = JuegoDeConsola.query.get_or_404(juego_id)
    db.session.delete(juego_consola)
    db.session.commit()
    return jsonify({'mensaje': 'Juego de consola eliminado exitosamente'}), 200

# Ruta para subir imágenes
@app.route('/api/subir_imagenes', methods=['POST'])
def subir_imagenes():
    if not verificar_sesion():
        return redirect(url_for('inicio'))

    files = request.files.getlist('imagenes')
    tipo = request.form.get('tipo')
    referencia_id = request.form.get('referencia_id')

    imagenes_guardadas = guardar_imagenes(files, referencia_id, tipo)
    return jsonify({'imagenes_guardadas': imagenes_guardadas}), 201

# Inicio del servidor Flask
if __name__ == '__main__':
    app.run(debug=True)
