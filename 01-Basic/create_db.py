import sqlite3

conn = sqlite3.connect("data/data.db")
c = conn.cursor()
c.execute('''CREATE TABLE tweets (
            id BIGINT,
            created DATETIME,
            text VARCHAR,
            user_id BIGINT,
            screen_name VARCHAR
          )''')
c.execute('''CREATE UNIQUE INDEX idx_id ON tweets(id)''')
conn.commit()
conn.close()
