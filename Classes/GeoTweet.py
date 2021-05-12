class GeoTweet:
    def __init__(s, id):
        s.id = id
        s.lat = None
        s.lon = None
        s.place = None
        s.geo_type = None
        s.country = None

    def saveCountry(s, c):
        q = (s.country, s.id)
        c.execute("""UPDATE tweets SET country = ?
                        WHERE id=?""", q)
