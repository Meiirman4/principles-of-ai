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

# for register
def create_user(username, password):
    """
    Creates a new user in the database.
    Returns True if successful, False if username already exists.
    """
    try:
        # Note: In a real app, password should be hashed here!
        # For this school project, storing it as-is is okay if your team agreed.
        query = "INSERT INTO users (username, password, level, progress) VALUES (%s, %s, 1, 0)"
        cursor.execute(query, (username, password))
        db.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error registering user: {err}")
        return False

# for login
def get_user(username):
    """
    Finds a user by username.
    Returns the user dictionary {id, username, password...} or None.
    """
    try:
        query = "SELECT * FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        return user
    except mysql.connector.Error as err:
        print(f"Error fetching user: {err}")
        return None