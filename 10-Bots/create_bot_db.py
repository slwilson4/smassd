import sqlite3

conn = sqlite3.connect("data/tweets.db")
c = conn.cursor()
c.execute('''CREATE TABLE bot_users (
            user_id BIGINT,
            bot_english FLOAT,
            bot_universal FLOAT
          )''')

c.execute('''CREATE UNIQUE INDEX bot_idx_id ON bot_users(user_id)''')

conn.commit()
conn.close()
