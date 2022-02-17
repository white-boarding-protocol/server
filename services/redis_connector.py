import redis


class RedisConnector:

    def __init__(self, hostname, port):
        print('Initiating services...')
        self.redis = redis.Redis(host=hostname, port=port, db=1)

    def put(self, key, value):
        self.redis.set(key, value)

    def get(self, key):
        value = self.redis.get(key)
        if value:
            return value.decode("utf-8")
        else:
            return None


if __name__ == "__main__":
    rc = RedisConnector("localhost", 6379)
    rc.put("abc","bipin")
    print( rc.get("abc") )
    print( rc.get("random") )
