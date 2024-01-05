from flask_login import UserMixin
class Programas(UserMixin):
    def __init__(self, id, nombre, titulo, nivelFormacion, metodologia, creditos, duracion, mision,vision):
        self.id = id
        self.nombre = nombre
        self.titulo = titulo
        self.nivelFormacion = nivelFormacion
        self.metodologia = metodologia
        self.creditos = creditos
        self.duracion = duracion
        self.mision = mision
        self.vision = vision
    def register(self,conexion):
        cursor = conexion.cursor()
        sql = "INSERT INTO programas(nombre, titulo, nivelFormacion, metodologia, creditos, duracion, mision, vision) VALUES (%s, %s, %s, %s, %s,%s,%s, %s)"
        # Usar el método execute con un marcador de posición %s y una tupla para los valores
        cursor.execute(sql, (self.nombre,self.titulo,self.nivelFormacion,self.metodologia,self.creditos,self.duracion,self.mision,self.vision))
        conexion.commit()

