import sqlite3

# Path to the SQLite database
DB_PATH = 'bank.db'

# Connect to the database (it will be created if it doesn't exist)
con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# Create the 'accounts' table if it doesn't already exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id TEXT PRIMARY KEY,
        owner TEXT NOT NULL,
        balance INTEGER NOT NULL,
        FOREIGN KEY(owner) REFERENCES users(email)
    )
''')

# Sample accounts to insert
accounts = [
    ('100', 'alice@example.com', 7500),
    ('190', 'alice@example.com', 200),
    ('998', 'bob@example.com', 1000)
]

# Insert accounts, ignoring any duplicates by primary key
for account_id, owner, balance in accounts:
    cur.execute('''
        INSERT OR IGNORE INTO accounts (id, owner, balance)
        VALUES (?, ?, ?)
    ''', (account_id, owner, balance))

# Commit changes and close the connection
con.commit()
con.close()
