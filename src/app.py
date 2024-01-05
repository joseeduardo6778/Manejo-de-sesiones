from flask import Flask, render_template, url_for, request, redirect, flash
from config import *
from Usuario import Usuario
from programas import Programas
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash

con_bd = EstablecerConexion()



app = Flask(__name__)
login_manager = LoginManager(app)
app.secret_key="5555"
csrf = CSRFProtect()


def crearTablaUsuarios():
    cursor = con_bd.cursor()
    cursor.execute( """CREATE TABLE IF NOT EXISTS usuarios(
        id serial NOT NULL,
        email character varying(50),
        password character varying,
        nombres character varying(60),
        rol character varying(60),
        CONSTRAINT pk_usuarios_id PRIMARY KEY (id)
        );""")
    con_bd.commit()

def crearTablaProgramas():
    cursor = con_bd.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS programas(
        id serial NOT NULL,
        nombre character varying,
        titulo character varying,
        nivelFormacion character varying,
        metodologia character varying,
        creditos character varying,
        duracion character varying,
        mision character varying,
        vision character varying,
        CONSTRAINT pk_programas_id PRIMARY KEY (id)
        );""")
    con_bd.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user = Usuario(0, request.form['email'], request.form['password'])
        usuario_logeado = Usuario.login(user,con_bd)
        if usuario_logeado != None:
            if usuario_logeado.password:
                login_user(usuario_logeado)
                return redirect(url_for('inicio'))
            else:
                flash("Contraseña incorrecta", "error")
                return render_template('login.html')
        else:
            flash("No existe el usuario","error")
            return render_template('login.html')
    else:
        return render_template('login.html')

@login_manager.user_loader
def cargar_usuario(id):
    return Usuario.obtener_usuario(con_bd, id)


@app.route('/cerrar_sesion')
def cerrar_sesion():
    logout_user()
    return render_template('login.httml')

@app.route('/inicio')
@login_required
def inicio():
    return render_template('inicio.html');
@app.route('/programas_academicos')
@login_required
def programas():
    cursor = con_bd.cursor()
    sql=""" SELECT id, nombre, titulo, nivelFormacion, metodologia, creditos, duracion, mision, vision FROM programas"""
    cursor.execute(sql)
    programas = cursor.fetchall()
    return render_template('programas.html', programas=programas)

@app.route('/register_user', methods = ['GET','POST'])
def addUser():
    if request.method == 'POST':
        user = Usuario(0, request.form['email'], request.form['password'])
        usuario_registrado = Usuario.register(user,con_bd)
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/guardar_programa', methods=['POST'])
def guardarPrograma():
    programas = Programas(0, request.form['nombre'], request.form['titulo'],request.form['nivelFormacion'],request.form['metodologia'],request.form['creditos'],request.form['duracion'],request.form['mision'],request.form['vision'])
    programa_registrado = Programas.register(programas,con_bd)
    return redirect(url_for('programas'))

def error_401(error):
    return render_template('login.html')

def error_404(error):
    return "PAGINA NO ENCONTRADA", 404

if __name__ == '__main__':
    csrf.init_app(app)
    app.register_error_handler(401, error_401)
    app.register_error_handler(404,error_404)
    crearTablaUsuarios()
    crearTablaProgramas()
    app.run(debug=True, port=1111)