# Actividad propuesta.

El objetivo de este trabajo práctico es desarrollar un programa en Python que lea un archivo
CSV que contiene información sobre las provincias argentinas y sus respectivas localidades. 
Posteriormente, se debe insertar esta información en una tabla de una base de datos, donde las
columnas de la tabla coincidan con los campos del CSV. Una vez importados los datos a la base de datos, se deben realizar las siguientes actividades:
Agrupación y Exportación por Provincia:
- Agrupar las localidades por provincia. 
- Exportar cada grupo de localidades en un archivo de CSV separado.
- Cada archivo CSV debe representar una provincia y contener la lista de sus
localidades.

## Criterios de Evaluación:

- **Correcta Lectura del CSV**:
Verificar que el programa lee correctamente el archivo CSV de las provincias argentinas con
sus localidades. 
- **Creación de Tabla en la Base de Datos**:
Asegurar que se crea una tabla en la base de datos con las columnas adecuadas y que los
datos se inserten correctamente. 
- **Manipulación de Datos**:
Evaluar cómo se manipulan los datos una vez que están en la base de datos, especialmente la
agrupación por provincia. 
- **Exportación a CSV**:
Verificar que se crean los archivos de CSV correctamente, uno por provincia, y que contienen
la lista de localidades correspondientes. 
- **Cantidad de Localidades en CSV**:
Comprobar que al final de cada archivo de CSV se incluye la cantidad de localidades
correspondientes a esa provincia. Uso de motor de base datos:
Se debe usar el motor de MariaDB el cual viene incorporado en el paquete XAMPP.
- **Eficiencia del Código**:
Evaluar la eficiencia del código en términos de velocidad de ejecución y uso de recursos. 
- **Manejo de Errores**:
Considerar cómo maneja el programa posibles errores durante la lectura del archivo, inserción en la base de datos, exportación a CSV, etc. 
- **Documentación y Claridad del Código**:
Revisar si el código está bien documentado y es claro para entender la lógica de
programación utilizada.

## Requisito indispensable

El programa debe tener la capacidad de crear la tabla de base de datos cada vez que se
ejecuta el script, es decir, si existe, debe ser eliminada y recreada.

## Presentación del trabajo práctico

La presentación del trabajo práctico debe realizarse en un repositorio de GitHub, el cual debe
ser público para su posterior revisión y evaluación.

# Sobre el proyecto

## Requisitos

- `python3` y `pip` instalados.
- Librería de manejo de entornos virtuales `venv`.
- Servidor de base de datos compatible con [MySQLdb](https://github.com/PyMySQL/mysqlclient).

## Pasos

- Crear un entorno con `venv`.

```bash
$ venv env
# o
$ python3 -m venv env
```

- Activar entorno.

```bash
$ ./env/Scripts/activate
# o
$ source ./env/bin/activate
```

- Instalar dependencias.

```bash
$ pip install -r requirements.txt
```
- Antes de ejecutar el script, asegúrese que el servidor de base de datos está escuchando peticiones.

- Puede configurar los datos usados para la conexión con las siguientes variables de entorno:

```
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_NAME=
DB_PORT=
```

- Ejecutar script:

```bash
$ python3 __init__.py
```