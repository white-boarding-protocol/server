import redis
import json
import uuid
from events.constants import UserStatus


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

    """
        Room Interfaces:
        - create room
        - remove room
        - get host user details
    """

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
        # remove all events
        event_ids = self.get_room_event_ids(room_id)
        for id in event_ids:
            self.redis.delete(id)
        # remove event reference
        self.redis.delete(self._get_event_reference(room_id))
        # remove the room
        self.redis.delete(room_id)

    def get_host(self, room_id):
        """
        :param room_id: room id
        :return: user id of the host of the room
        """
        # get the host id, which is the value at 1 index
        host_id = self._get_items_from_list(room_id, 1, 2, False)[0]
        # get the detail of the host
        return self.get_user(host_id)

    """
        User Interfaces:
        - create new user
        - insert user to room
        - update user
        - remove user form room
        - delete user
        - get user details
        - get list of user ids
        - get list of user details
        - get list of queuing user details
        - remove user from room
    """

    def create_user(self, user_id, user):
        self._put(user_id, user)

    def insert_user(self, room_id, user_id):
        self.redis.rpush(room_id, user_id)

    def update_user(self, user_id, new_user):
        self._put(user_id, new_user)

    def remove_user_from_room(self, room_id, user_id):
        # todo: remove user id from the main list as well
        pass

    def delete_user(self, user_id):
        self.redis.delete(user_id)

    def get_user(self, user_id):
        return self.redis.get(user_id)

    def get_room_user_ids(self, room_id, include_host=True):
        return self._get_items_from_list(room_id, 1 if include_host else 2, -1, False)

    def get_room_users(self, room_id, include_host=True):
        """
        Get lst of user details belonging to a room
        :param room_id: room id
        :param include_host: if the host should also be included in the list
        :return: list of user details
        """
        # get all the user ids belonging to this room.
        user_id_list = self.get_room_user_ids(room_id, include_host)
        # map all the user ids to the user details
        if user_id_list:
            return list(map(lambda u: self._get(u), user_id_list))
        else:
            return []

    def get_queue_users(self, room_id):
        users = self.get_room_users(room_id)
        return list(map(lambda u: u and u.get["status"] == UserStatus.QUEUING, users))

    """
        Event interfaces:
        - insert event of room
        - edit event
        - remove event
        - get list of event ids belonging to room
        - get list of event details belonging to room
        - get last event id
    """

    def insert_event(self, room_id, event):
        new_event_id = "event_" + str(uuid.uuid1())
        events_id = self._get_event_reference(room_id)
        self.redis.rpush(events_id, new_event_id)
        self._put(new_event_id, event)
        return new_event_id

    def edit_event(self, event_id, new_event):
        self._put(event_id, new_event)

    def remove_event(self, event_id):
        self.redis.delete(event_id)

    def get_event(self, event_id):
        return self._get(event_id)

    def get_room_event_ids(self, room_id):
        return self._get_items_from_list(self._get_event_reference(room_id), 0, -1, False)

    def get_room_events(self, room_id):
        """
        get event details of a room
        :param room_id: room id
        :return: list of event details
        """
        # get the event id of this room and fetch all the list values
        event_id_list = self.get_room_event_ids(room_id)
        # map all the event ids to the event details
        if event_id_list:
            event_details = list(map(lambda u: self._get(u), event_id_list))
            return [e for e in event_details if e is not None]  # filter all None values
        else:
            return []

    def get_last_event_id(self, room_id):
        return self.get_room_event_ids(room_id).pop()

    def _get_event_reference(self, room_id):
        # get event id - the value in 0 index
        return self._get_items_from_list(room_id, 0, 1, False)[0]


    """
    Internal Redis 
    """
    def _put(self, key, value):
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

    def _get(self, key):
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


    def _get_items_from_list(self, key, from_index=0, to_index=-1, parse_json=False):
        values = self.redis.lrange(key, from_index, to_index)
        if values:
            return list(map(lambda v: json.loads(v) if parse_json else v.decode("utf-8"), values))
        else:
            return None
