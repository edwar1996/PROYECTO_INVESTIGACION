import pyodbc

# Función para intentar conectar a la base de datos
def get_db_connection():
    try:
        conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                              'SERVER=(localdb)\\baselocal;'
                              'DATABASE=Dispro;'
                              'UID=baselocal;'
                              'PWD=baselocal1085')
        print("Conexión exitosa a la base de datos")
        return conn
    except pyodbc.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Función para probar la conexión
def test_connection():
    conn = get_db_connection()
    if conn:
        conn.close()  # Cierra la conexión si es exitosa
    else:
        print("No se pudo establecer una conexión con la base de datos.")

# Ejecutar la prueba de conexión
test_connection()
