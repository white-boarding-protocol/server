import redis
import json
import uuid


class RedisConnector:
    """
    Database Service:

    In redis, following structure is used:
    room_id1 -----> [ events_id_X, user1_id, user2_id, ... userN_id ]
    events_id_X ------> [ event1, event2, event3, ..... eventN ]
    user1_id ------> { "status": "in_queue", "joined": 1988712312 }
    """

    def __init__(self, hostname, port, password=None):
        """
        Default constructor
        :param hostname: hostname of redis
        :param port: redis server port
        :param password: redis server password
        """
        self.redis = redis.Redis(host=hostname, port=port, password=password, db=1)

    def get_host(self, room_id):
        # get the host id, which is the value at 1 index
        host_id = self.get_items_from_list(room_id, 1, 2)[0]
        # get the detail of the host
        return self.get(host_id)

    def get_users(self, room_id, include_host=True):
        # get all the user ids belonging to this room.
        user_id_list = self.get_items_from_list(room_id, 1 if include_host else 2, -1)
        # map all the user ids to the user details
        if user_id_list:
            return list(map(lambda u: self.get(u), user_id_list))
        else:
            return []

    def get_events(self, room_id):
        # get the event id of this room and fetch all the list values
        return self.get_items_from_list(self.get_event_id(room_id))

    def get_event_id(self, room_id):
        # get event id - the value in 0 index
        return self.get_items_from_list(room_id, 0, 1)[0]

    def get_items_from_list(self, key, from_index=0, to_index=-1):
        values = self.redis.lrange(key, from_index, to_index)
        if values:
            return list(map(lambda v: json.loads(v), values))
        else:
            return None

    def create_room(self, host):
        room_id = uuid.uuid1()
        self.redis.lpush(room_id, uuid.uuid1()) # insert a random id as events_id
        self.insert_user(room_id, host) # add host the next

    def insert_event(self, room_id, events):
        events_id = self.get_event_id(room_id)
        if not events_id:
            events_id = uuid.uuid1()
        self.redis.lpush(events_id, *events)

    def insert_user(self, room_id, user):
        user_id = uuid.uuid1()
        self.put(user_id, user)
        self.redis.rpush(room_id, user)

    def put(self, key, value):
        """
        Insert value in the redis db
        :param key: key
        :param value: dictionary value
        :return: None
        """
        json_value = ""
        if value:
            json_value = json.dumps(value)
        self.redis.set(key, json_value)

    def get(self, key):
        """
        Get value from redis
        :param key: key
        :return: dictionary value
        """
        value = self.redis.get(key)
        if value:
            json_value = value.decode("utf-8")
            return json.loads(json_value)
        else:
            return None


if __name__ == "__main__":
    rc = RedisConnector("localhost", 6379)
    rc.put("abc", "bipin")
    print(rc.get("abc"))
    print(rc.get("random"))

    thisdict = {
        "brand": "Ford",
        "model": "Mustang",
        "year": 1964
    }
    rc.put("dict-test", thisdict)
    print(rc.get("dict-test"))
