import sqlite3

conn = sqlite3.connect("cache_new.db")
c = conn.cursor()
c.execute('''CREATE TABLE cache (
            country VARCHAR,
            lat INT,
            lon INT,
            total INT
          )''')
c.execute('''CREATE UNIQUE INDEX idx_cache ON cache (lat,lon,country)''')
conn.commit()
conn.close()
