class Place:
    def __init__(s, id):
        s.id = id

    def loadJSON(s, p_json):
        s.place_type = p_json['place_type']
        s.name = p_json['full_name']
        s.country_code = p_json['country_code']
        s.lat_1 = p_json['bounding_box']['coordinates'][0][0][1]
        s.lat_2 = p_json['bounding_box']['coordinates'][0][2][1]
        s.lon_1 = p_json['bounding_box']['coordinates'][0][0][0]
        s.lon_2 = p_json['bounding_box']['coordinates'][0][2][0]

    def insert(s, c):
        q = (
            s.id, s.place_type, s.name, s.country_code,
            s.lat_1, s.lat_2, s.lon_1, s.lon_2, s.country
        )
        c.execute(
            """REPLACE INTO places
            (id, place_type, name, country_code,
            lat_1, lat_2, lon_1, lon_2, country)
            VALUES(?,?,?,?,?,?,?,?,?)""", q)
