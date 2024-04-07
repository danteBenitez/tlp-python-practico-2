import MySQLdb as Database 

class LocationService:
    def __init__(self, connection: Database.Connection):
        self.db_connection = connection
    
    def ensure_initialized(self):
        """
            Crea una tabla `localidades` en la base de datos.
            Si ya existe, la borra y vuelve a crearla.
        """
        try:
            cursor: Database.cursors.Cursor = self.db_connection.cursor()
            # Eliminar la tabla si existe
            cursor.execute("DROP TABLE IF EXISTS localidades")

            # Creamos la tabla
            # Aviso: Como el código postal no está presente en todas las localidades
            # el esquema lo define como opcional.
            cursor.execute(
                """
                    CREATE TABLE localidades (
                        id INT NOT NULL,
                        localidad VARCHAR(255) NOT NULL,
                        provincia VARCHAR(255) NOT NULL,
                        cp INT,
                        id_prov_mstr INT NOT NULL
                    ) 
                """
            )
            self.db_connection.commit()
        except Database.DatabaseError as err:
            self.db_connection.rollback()
            print(f"Error al crear tabla localidades: {err}")
            raise err

    def _normalize_location(self, location: dict[str, str]):
        """
            Transforma una localidad en formato diccionario
            a una tupla para usarse como parámetro a una query.

            :returns Tuple en el formato esperado por una consulta INSERT.
        """
        # El código postal en ocasiones puede estar vacío.
        cp = location["cp"]
        if cp == "":
            cp = None
        else:
            cp = int(cp)
        
        tuple_loc = ( 
            int(location["id"]), 
            location["localidad"], 
            location["provincia"], 
            cp,
            int(location["id_prov_mstr"])
        )
        return tuple_loc

    
    def insert_many(self, locations: list[dict[str, str]]):
        """
            Inserta `locations` en la tabla correspondiente.

            :param locations: La lista de localidades a insertarse
            :type locations: list[Location]
            :raises: :class:`MySQLdb.Error`
        """
        try:
            # Obtener un cursor para realizar una consulta
            cursor: Database.cursors.Cursor = self.db_connection.cursor()
            # Normalizar datos de las localidades para insertar
            # Siguiendo: https://mysqlclient.readthedocs.io/user_guide.html#cursor-objects
            normalized_locations = map(self._normalize_location, locations)

            # Nótese que realizar una inserción con `executemany` tiende a tener mejor rendimiento
            # para operaciones que afectan múltiples registros.
            cursor.executemany(
                """
                    INSERT INTO localidades (id, localidad, provincia, cp, id_prov_mstr)
                    VALUES (%s, %s, %s, %s, %s)
                """, normalized_locations)

            self.db_connection.commit()
        except Database.Error as err:
            self.db_connection.rollback()
            raise err

    def get_provinces(self) -> list[str]:
        """
            Retorna todas las provincias de las localidades de la tabla.

            :raises :class:`MYSQLDb.Error`

            :returns Las provincias como una lista de strings.
        """
        cursor: Database.cursors.Cursor = self.db_connection.cursor()
        cursor.execute("""SELECT provincia FROM localidades GROUP BY provincia""")
        return list(cursor.fetchall())

    def filter_by_province(self, province: str):
        """
            Realiza una consulta que filtra las localidades según la provincia.

            :param attribute: Nombre de la provincia.
            :type attribute: str

            :raises :class:`MYSQLDb.Error`
            :returns El cursor con los resultados de la consulta. 
                Permite llamar `fetchone` o `fetchtall` para obtenerlos uno a uno,
                o en conjunto.
            :rtype `MySQLdb.cursors.Cursor`
        """
        cursor: Database.cursors.Cursor = self.db_connection.cursor()
        cursor.execute(
            """
                SELECT * FROM localidades WHERE provincia = %s;
            """,
            (province,)
        )
        return cursor


