import redis
import json
import uuid


class RedisConnector:
    """
    Database Service:

    In redis, following structure is used:
    room_id1 -----> [ events_id_X, user1_id, user2_id, ... userN_id ]
    events_id_X ------> [ event1, event2, event3, ..... eventN ]
    event1 --------> {...event json...}
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
        """
        :param room_id: room id
        :return: user id of the host of the room
        """
        # get the host id, which is the value at 1 index
        host_id = self.__get_items_from_list(room_id, 1, 2, False)[0]
        # get the detail of the host
        return self.get(host_id)

    def get_users(self, room_id, include_host=True):
        """
        Get lst of user details belonging to a room
        :param room_id: room id
        :param include_host: if the host should also be included in the list
        :return: list of user details
        """
        # get all the user ids belonging to this room.
        user_id_list = self.__get_items_from_list(room_id, 1 if include_host else 2, -1, False)
        # map all the user ids to the user details
        if user_id_list:
            return list(map(lambda u: self.get(u), user_id_list))
        else:
            return []

    def remove_user_from_room(self, room_id, user_id):
        pass

    def get_user(self, user_id):
        pass

    def get_events(self, room_id):
        """
        get event details of a room
        :param room_id: room id
        :return: list of event details
        """
        # get the event id of this room and fetch all the list values
        event_id_list = self.__get_items_from_list(self.get_event_id(room_id), 0, -1, False)
        # map all the event ids to the event details
        if event_id_list:
            event_details = list(map(lambda u: self.get(u), event_id_list))
            return [e for e in event_details if e is not None] # filter all None values
        else:
            return []

    def get_last_event_id(self, room_id):
        return self.__get_items_from_list(self.get_event_id(room_id), 0, -1, False).pop()

    def get_event_id(self, room_id):
        # get event id - the value in 0 index
        return self.__get_items_from_list(room_id, 0, 1, False)[0]

    def __get_items_from_list(self, key, from_index=0, to_index=-1, parse_json=False):
        values = self.redis.lrange(key, from_index, to_index)
        if values:
            return list(map(lambda v: json.loads(v) if parse_json else v.decode("utf-8"), values))
        else:
            return None

    def create_room(self, host):
        """
        create a new room
        :param host: host id
        :return: new room id
        """
        room_id = "room_" + str(uuid.uuid1())
        events_id = "room-events_" + str(uuid.uuid1())
        self.redis.lpush(room_id, events_id)
        self.insert_user(room_id, host)  # add host the next
        return room_id

    def remove_room(self, room_id):
        pass

    def insert_event(self, room_id, event):
        new_event_id = "event_" + str(uuid.uuid1())

        events_id = self.get_event_id(room_id)
        self.redis.rpush(events_id, new_event_id)
        self.put(new_event_id, event)


    def edit_event(self, event_id, new_event):
        self.put(event_id, new_event)

    def remove_event(self, event_id):
        self.redis.delete(event_id)

    def update_user(self, user_id, new_user):
        pass

    def insert_user(self, room_id, user_id, user):
        self.put(user_id, user)
        self.redis.rpush(room_id, user_id)

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
    host = "session.bipin.1"
    participant1 = "session.part1.1"
    participant2 = "session.part2.1"
    events = [{"key1": "asasdfd"}, {"key2": "adsfsfsdf"}, {"check": "asd"}]

    room_id = rc.create_room(host)
    rc.insert_event(room_id, events)
    rc.insert_user(room_id, participant1)
    rc.insert_user(room_id, participant2)

    print("host = ", rc.get_host(room_id))
    print("users = ", rc.get_users(room_id))
    print("users (excl host) = ", rc.get_users(room_id, False))
    print("event_id = ", rc.get_event_id(room_id))
    print("events = ", rc.get_events(room_id))
