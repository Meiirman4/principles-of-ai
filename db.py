import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "dragon"
}

try:
    db = mysql.connector.connect(**db_config)

    cursor = db.cursor(dictionary=True, buffered=True)
    
    print("✅ Database connected successfully!")

except mysql.connector.Error as err:
    print(f"❌ Error connecting to database: {err}")
    db = None
    cursor = None