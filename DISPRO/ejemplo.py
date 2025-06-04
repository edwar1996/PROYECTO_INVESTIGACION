import pyodbc

conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=(localdb)\\baselocal;DATABASE=Dispro;UID=baselocal;PWD=baselocal1085'
)
cursor = conn.cursor()
cursor.execute("SELECT TOP 5 * FROM proceso_2")
for row in cursor.fetchall():
    print(row)
