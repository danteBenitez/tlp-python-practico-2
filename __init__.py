import sys
import os
import csv
from pathlib import Path
from database import connect, Error as DatabaseError
from locations.location_service import LocationService

LOCATION_INPUT_PATH = "data/localidades.csv"
LOCATION_OUTPUT_PATH = "data/processed/localidades_por_provincia/"

def ensure_output_path_not_exists(path: str):
    if not os.path.exists(path):
        output_path = Path(path)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        # Si la carpeta existe, se emite un aviso y se termina el programa.
        print(
            "La carpeta de datos procesados ya existe. "
            "Por favor, elimínela si quiere repetir la inserción."
        )
        sys.exit(1)

def main():
    """
        Funcionamiento principal del programa.
        Se lee el archivo CSV de localidades, inserta los datos en una base de
        datos, y realiza una consulta para agruparlos por provincia, y luego
        exporta el resultado en varios archivos CSV.
    """
    try:
        ensure_output_path_not_exists(LOCATION_OUTPUT_PATH)

        connection = connect()
        location_service = LocationService(connection)
        location_service.ensure_initialized()
        # print("> Tabla localidades creada...")

        with open(LOCATION_INPUT_PATH) as file:
            parsed = csv.reader(file)
            # Saltear la fila que contiene los nombres de columnas
            parsed.__next__() 
            location_service.insert_many(parsed)

        # print("> Localidades insertadas...")

        provinces = location_service.get_provinces()
        # print("> Listadas provincias")

        for province, in provinces:
            # Crearemos un archivo CSV diferente para cada provincia
            # print(f"> Creando archivo para provincia: {province}")
            file_path = os.path.join(LOCATION_OUTPUT_PATH, f"{province}.csv")

            # Obtenemos las localidades de tal provincia
            locations, rows_affected = location_service.filter_by_province(province)

            # La opción "w" ("write") crea el archivo si no existe.
            with open(file_path, "w") as file:
                # Creamos un escritor para insertar los datos
                # en forma de tupla...
                writer = csv.writer(file)

                # Escribimos el encabezado del CSV
                writer.writerow(("id", "localidad", "provincia", "cp", "id_prov_mstr"))

                location = locations.fetchone()
                while location:
                    writer.writerow(location)
                    location = locations.fetchone()

                writer.writerow(("cantidad_localidades",))
                writer.writerow((rows_affected,))

            # print(f"> Creado archivo para provincia: {province}")

        print("> Procedimiento finalizado sin problemas.")
    except csv.Error as err:
        print(f"Ha ocurrido un error al leer un archivo CSV: {err}.")
    except DatabaseError as err:
        print(f"Ha ocurrido un error en una operación de la base de datos: {err}")
    finally:
        connection.close()

if __name__ == "__main__":
    main()
