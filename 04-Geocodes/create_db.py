import sqlite3

conn = sqlite3.connect("data/data.db")
c = conn.cursor()
c.execute('''CREATE TABLE tweets (
            id BIGINT,
            created DATETIME,
            text VARCHAR,
            user_id BIGINT,
            screen_name VARCHAR,
            lat FLOAT,
            lon FLOAT,
            place_id VARCHAR,
            geo_type VARCHAR,
            country VARCHAR
          )''')
c.execute('''CREATE UNIQUE INDEX idx_id ON tweets(id)''')
c.execute('''CREATE TABLE places (
            id VARCHAR,
            place_type VARCHAR,
            name VARCHAR,
            country_code VARCHAR,
            lat_1 FLOAT,
            lon_1 FLOAT,
            lat_2 FLOAT,
            lon_2 FLOAT,
            country VARCHAR
          )''')
c.execute('''CREATE UNIQUE INDEX idx_place_id ON places(id)''')
conn.commit()
conn.close()
