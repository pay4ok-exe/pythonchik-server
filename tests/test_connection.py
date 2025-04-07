# test_connection.py
import pyodbc

# Try different connection strings until one works
connection_strings = [
    # Format 1: Default instance using localhost
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost;DATABASE=Pythonchick;Trusted_Connection=yes;",
    
    # Format 2: Named instance using localhost
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=localhost\\pay4ok;DATABASE=Pythonchick;Trusted_Connection=yes;",
    
    # Format 3: Using dot for local server
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=.;DATABASE=Pythonchick;Trusted_Connection=yes;",
    
    # Format 4: Using machine name
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=PAY4OK;DATABASE=Pythonchick;Trusted_Connection=yes;",
    
    # Format 5: Using full instance name
    "DRIVER={ODBC Driver 17 for SQL Server};SERVER=pay4ok\\pay4ok;DATABASE=Pythonchick;Trusted_Connection=yes;",
]

success = False

for i, conn_str in enumerate(connection_strings):
    print(f"Trying connection string {i+1}...")
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT @@SERVERNAME")
        row = cursor.fetchone()
        print("✅ Connection successful!")
        print(f"Server: {row[0]}")
        conn.close()
        print(f"Working connection string: {conn_str}")
        success = True
        break
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        print()

if not success:
    print("All connection attempts failed.")