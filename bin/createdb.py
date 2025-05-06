import sqlite3
from passlib.hash import pbkdf2_sha256

# Connect to the SQLite database (creates it if it doesn't exist)
DB_PATH = 'bank.db'
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Create 'users' table with email as the primary key
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        email TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')

# Predefined user credentials (hashed securely)
users = [
    ('alice@example.com', 'Alice Xu', pbkdf2_sha256.hash("123456")),
    ('bob@example.com', 'Bobby Tables', pbkdf2_sha256.hash("123456"))
]

# Insert users if they don't already exist
for email, name, password in users:
    cur.execute('''
        INSERT OR IGNORE INTO users (email, name, password)
        VALUES (?, ?, ?)
    ''', (email, name, password))

# Save changes and close the connection
con.commit()
con.close()
