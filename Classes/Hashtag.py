class Hashtag:
    def __init__(s, tweet_id, h_json):
        s.tweet_id = tweet_id
        s.hashtag = h_json['text']

    def save(s, c):
        q = (
            s.tweet_id, s.hashtag
        )
        c.execute(
            """REPLACE INTO hashtags
            (tweet_id, hashtag)
            VALUES(?,?)""", q)
