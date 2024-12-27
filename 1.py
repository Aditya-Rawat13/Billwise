import sqlite3

# Create SQLite database for storing user info
conn = sqlite3.connect('data/users.db')
cur = conn.cursor()

# Create the users table if it doesn't exist
cur.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')
conn.commit()
conn.close()

# Create a CSV for expenses if it doesn't exist
import pandas as pd

df = pd.DataFrame(columns=["Company", "Date", "Total", "Category"])
df.to_csv('data/expenses.csv', index=False)
