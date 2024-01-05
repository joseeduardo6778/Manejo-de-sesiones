from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin

class Usuario(UserMixin):
    def __init__(self, id, email, password, nombre=""):
        self.id = id
        self.email = email
        self.password = password
        self.nombre = nombre
    def login(self, conexion):
        cursor = conexion.cursor()
        sql = """ SELECT * FROM usuarios WHERE email = '{0}' """.format(self.email)
        cursor.execute(sql)
        fila = cursor.fetchone()
        if fila != None:
            usuario = Usuario(fila[0], fila[1], check_password_hash(fila[2],self.password),fila[3])
            return usuario
        else:
            return None
    def register(self, conexion):
        cursor = conexion.cursor()
        password_encript = generate_password_hash(self.password)
        sql = "INSERT INTO usuarios(email, password, nombres) VALUES (%s, %s, %s)"
        # Usar el método execute con un marcador de posición %s y una tupla para los valores
        cursor.execute(sql, (self.email, password_encript, self.nombre))
        conexion.commit()
    @classmethod
    def obtener_usuario(self, conexion, id):
        cursor = conexion.cursor()
        sql=""" SELECT id, email, nombres FROM usuarios WHERE id = {0}""".format(id)
        cursor.execute(sql)
        fila = cursor.fetchone()
        if fila != None:
            usuario = Usuario(fila[0], fila[1], None, fila[2])
            return usuario
        else:
            return None
        