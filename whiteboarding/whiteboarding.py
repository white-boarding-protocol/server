import asyncio
import json
import logging
import netifaces

from events.exceptions import InvalidEvent, Disconnected
from security.encrypted_session_server import EncryptedSessionServer
from services.redis_connector import RedisConnector
from singleton.singleton import Singleton
from whiteboarding.exceptions import InvalidConfig


class Whiteboarding(metaclass=Singleton):
    CONFIG_PATH = "config.json"
    CONFIG_MANDATORY_FIELDS = ["ssl_enabled", "port_number", "interface"]
    SSL_REQUIRED_FIELDS = ["ssl_cert_path", "ssl_key_path"]

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.error_message = None
        self._config = self._load_config()

        self._config['handler'] = self.handle_client
        self.session_server = EncryptedSessionServer(**self._config)
        self.redis_connector = RedisConnector("localhost", 6379)

        self._online_users = {}
        self._online_users_lock = asyncio.Lock()

    def _load_config(self):
        with open(self.CONFIG_PATH, "r") as file:
            config = json.load(file)

        if self._is_config_valid(config):
            config['ip_address'] = netifaces.ifaddresses(config.pop('interface')).get(netifaces.AF_INET)[0].get('addr')

            self.logger.info("Config file successfully loaded")
            return config
        else:
            self.logger.error(self.error_message)
            raise InvalidConfig(self.error_message)

    def _is_config_valid(self, config):
        for mandatory_key in self.CONFIG_MANDATORY_FIELDS:
            if mandatory_key not in config:
                self.error_message = f"{mandatory_key} not included in the config file"
                return False

            if mandatory_key == 'ssl_enabled' and type(config['ssl_enabled']) != bool:
                self.error_message = f"{mandatory_key} value should be boolean"

        if config['ssl_enabled']:
            for mandatory_key in self.SSL_REQUIRED_FIELDS:
                if mandatory_key not in config:
                    self.error_message = f"{mandatory_key} not included in the config file when ssl is enabled"
                    return False

        return True

    async def start(self):
        await self.session_server.start_server()

    @staticmethod
    async def handle_client(client_socket):
        from events.masterevent import MasterEvent

        is_online = True
        while is_online:
            client_msg = await json.loads(client_socket.recv())
            event = MasterEvent.deserialize(client_msg)
            try:
                event.exec()
            except InvalidEvent:
                # TODO send invalid msg
                await client_socket.send(json.dumps({"message": "Invalid data"}))
            except Disconnected:
                is_online = False

    def add_online_user(self, user_id, client_socket):
        with self._online_users_lock:
            self._online_users[user_id] = client_socket

    def remove_online_user(self, user_id):
        with self._online_users_lock:
            self._online_users.pop(user_id)
