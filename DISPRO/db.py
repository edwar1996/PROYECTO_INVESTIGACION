import pyodbc

def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                         'SERVER=(localdb)\\baselocal;'
                         'DATABASE=Dispro;'
                         'UID=baselocal;'
                         'PWD=baselocal1085')
    return conn
