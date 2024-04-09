import os
import MySQLdb as mysql

DEFAULT_CONFIG = {
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME", "localidades"),
    "port": int(os.getenv("DB_PORT", "3306"))
}

Error = mysql.Error

def connect(config = DEFAULT_CONFIG) -> mysql.Connection:  
    """
        Realiza la conexión a una base de datos, y devuelve la instancia de conexión.
    """
    return mysql.connect(**config)
     

