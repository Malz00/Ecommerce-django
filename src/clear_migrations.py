import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')

# Create a cursor to execute SQL commands
cursor = conn.cursor()

# Delete migration history for 'accounts' and 'admin'
cursor.execute("DELETE FROM django_migrations WHERE app = 'accounts';")
cursor.execute("DELETE FROM django_migrations WHERE app = 'admin';")

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Migration history cleared successfully.")
