import sqlite3

conn = sqlite3.connect("data/data.db")
c = conn.cursor()
c.execute('''CREATE TABLE geo_users (
            id BIGINT,
            country VARCHAR,
            pct FLOAT
          )''')
conn.commit()
conn.close()
