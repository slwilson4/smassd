class Mention:
    def __init__(s, tweet_id, m_json):
        s.tweet_id = tweet_id
        s.user_id = m_json['id']
        s.screen_name = m_json['screen_name']

    def save(s, c):
        q = (
            s.tweet_id, s.user_id, s.screen_name
        )
        c.execute(
            """REPLACE INTO mentions
            (tweet_id, user_id, screen_name)
            VALUES(?,?,?)""", q)
