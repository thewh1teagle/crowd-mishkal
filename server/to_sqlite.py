import sqlite3

# Connect to SQLite (or create the database file if it doesn't exist)
conn = sqlite3.connect('db.sqlite')
cursor = conn.cursor()

# Create the table if it doesn't already exist (with the 'skipped' column added)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS lines (
        line_number INTEGER PRIMARY KEY,
        line TEXT,
        tagged TEXT,
        being_tagged BOOLEAN DEFAULT 0,
        skipped BOOLEAN DEFAULT 0
    )
''')

# Open the file and insert each line into the database
with open('20_000.knesset.txt', encoding='utf-8') as fp:
    for line_number, line in enumerate(fp):
        line = line.strip()
        cursor.execute(
            'INSERT OR REPLACE INTO lines (line_number, line, tagged, being_tagged, skipped) VALUES (?, ?, ?, ?, ?)',
            (line_number, line, None, False, False)
        )

# Commit the changes and close the connection
conn.commit()
conn.close()
