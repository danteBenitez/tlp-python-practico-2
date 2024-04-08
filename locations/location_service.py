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
                        cp VARCHAR(255),
                        id_prov_mstr VARCHAR(255)
                    ) 
                """
            )
            self.db_connection.commit()
        except Database.DatabaseError as err:
            self.db_connection.rollback()
            print(f"Error al crear tabla localidades: {err}")
            raise err
    
    def insert_many(self, locations: list[tuple]):
        """
            Inserta `locations` en la tabla correspondiente.

            :param locations: La lista de localidades a insertarse como tuplas.
                El orden de los atributos es el siguiente:
                    - provincia
                    - id
                    - localidad
                    - cp
                    - id_prov_mstr
            :type locations: list[Location]
            :raises: :class:`MySQLdb.Error`
        """
        try:
            # Obtener un cursor para realizar una consulta
            cursor: Database.cursors.Cursor = self.db_connection.cursor()

            # Nótese que realizar una inserción con `executemany` tiende a tener mejor rendimiento
            # para operaciones que afectan múltiples registros.
            # Véase: https://mysqlclient.readthedocs.io/user_guide.html#cursor-objects
            cursor.executemany(
                """
                    INSERT INTO localidades (provincia, id, localidad, cp, id_prov_mstr)
                    VALUES (%s, %s, %s, %s, %s)
                """, locations)

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
        cursor.execute("""SELECT DISTINCT provincia FROM localidades ORDER BY provincia""")
        return list(cursor.fetchall())

    def filter_by_province(self, province: str):
        """
            Realiza una consulta que filtra las localidades según la provincia.

            :param attribute: Nombre de la provincia.
            :type attribute: str

            :raises :class:`MYSQLDb.Error`
            :returns Una tupla.
                El primer elemento es el cursor con los resultados de la consulta. 
                Permite llamar `fetchone` o `fetchtall` para obtenerlos uno a uno,
                o en conjunto.
                El segundo es el número de registros encontrados.
            :rtype (`MySQLdb.cursors.Cursor`, int)
        """
        cursor: Database.cursors.Cursor = self.db_connection.cursor()
        rows_affected = cursor.execute(
            """
                SELECT * FROM localidades WHERE provincia = %s;
            """,
            (province,)
        )
        return cursor, rows_affected


