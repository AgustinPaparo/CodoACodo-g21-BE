from conf import get_db


class Property:
    def __init__(
        self,
        id=None,
        propietario_id=None,
        direccion=None,
        tipo=None,
        habitaciones=None,
        banos=None,
        tamano=None,
        cochera=None,
        precio=None,
        estado=None,
        tipo_contrato=None,
        imagenes=None,
    ):
        self.id = id
        self.propietario_id = propietario_id
        self.direccion = direccion
        self.tipo = tipo
        self.habitaciones = habitaciones
        self.banos = banos
        self.tamano = tamano
        self.cochera = cochera
        self.precio = precio
        self.estado = estado
        self.tipo_contrato = tipo_contrato
        self.imagenes = imagenes

    @staticmethod
    def __get_properties_by_query(query):
        db = get_db()
        cursor = db.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()

        properties = []
        for row in rows:
            properties.append(
                Property(
                    id=row[0],
                    propietario_id=row[1],
                    direccion=row[2],
                    tipo=row[3],
                    habitaciones=row[4],
                    banos=row[5],
                    tamano=row[6],
                    cochera=row[7],
                    precio=row[8],
                    estado=row[9],
                    tipo_contrato=row[10],
                    imagenes=row[11],
                )
            )
        cursor.close()
        return properties

    @staticmethod
    def get_all_properties():
        return Property.__get_properties_by_query(
                """
            SELECT * FROM properties
            """
            )

    @staticmethod
    def get_property_by_id(id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM properties WHERE id = %s", (id,))
        row = cursor.fetchone()
        cursor.close()

        if row:
            return Property(
                id=row[0],
                propietario_id=row[1],
                direccion=row[2],
                tipo=row[3],
                habitaciones=row[4],
                banos=row[5],
                tamano=row[6],
                cochera=row[7],
                precio=row[8],
                estado=row[9],
                tipo_contrato=row[10],
                imagenes=row[11],
            )
        return None

    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id:
            # Actualizar propiedad existente
            cursor.execute(
                """
                UPDATE properties
                SET propietario_id = %s, direccion = %s, tipo = %s, habitaciones = %s, 
                    banos = %s, tamano = %s, cochera = %s, precio = %s, estado = %s, 
                    tipo_contrato = %s, imagenes = %s
                WHERE id = %s
                """,
                (
                    self.propietario_id,
                    self.direccion,
                    self.tipo,
                    self.habitaciones,
                    self.banos,
                    self.tamano,
                    self.cochera,
                    self.precio,
                    self.estado,
                    self.tipo_contrato,
                    self.imagenes,
                    self.id,
                ),
            )
        else:
            # Crear nueva propiedad
            cursor.execute(
                """
                INSERT INTO properties 
                (propietario_id, direccion, tipo, habitaciones, banos, tamano, cochera, precio, estado, tipo_contrato, imagenes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    self.propietario_id,
                    self.direccion,
                    self.tipo,
                    self.habitaciones,
                    self.banos,
                    self.tamano,
                    self.cochera,
                    self.precio,
                    self.estado,
                    self.tipo_contrato,
                    self.imagenes,
                ),
            )
            self.id = cursor.lastrowid

        db.commit()
        cursor.close()

    def delete(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM properties WHERE id = %s", (self.id,))
        db.commit()
        cursor.close()

    def get_fotos(self):
        if self.imagenes:
            return self.imagenes
        else:
            return []

    def serialize(self):
        return {
            "id": self.id,
            "propietario_id": self.propietario_id,
            "direccion": self.direccion,
            "tipo": self.tipo,
            "habitaciones": self.habitaciones,
            "baños": self.banos,
            "tamaño": self.tamano,
            "cochera": self.cochera,
            "precio": self.precio,
            "estado": self.estado,
            "tipo_contrato": self.tipo_contrato,
            "imagenes": self.imagenes,
        }
