import redis
import json


class RedisConnector:

    def __init__(self, hostname, port, password=None):
        self.redis = redis.Redis(host=hostname, port=port, password=password, db=1)

    def put(self, key, value):
        json_value = ""
        if value:
            json_value = json.dumps(value)
        self.redis.set(key, json_value)

    def get(self, key):
        value = self.redis.get(key)
        if value:
            json_value = value.decode("utf-8")
            return json.loads(json_value)
        else:
            return None


if __name__ == "__main__":
    rc = RedisConnector("localhost", 6379)
    rc.put("abc","bipin")
    print( rc.get("abc") )
    print( rc.get("random") )

    thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
    }
    rc.put("dict-test", thisdict)
    print( rc.get("dict-test") )
