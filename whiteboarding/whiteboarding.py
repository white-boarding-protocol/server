import json
import logging
import netifaces

from security.encrypted_session_server import EncryptedSessionServer
from whiteboarding.exceptions import InvalidConfig


class Whiteboarding:
    CONFIG_PATH = "config.json"
    CONFIG_MANDATORY_FIELDS = ["ssl_enabled", "port_number", "interface"]
    SSL_REQUIRED_FIELDS = ["ssl_cert_path", "ssl_key_path"]

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.error_message = None
        self.config = self.load_config()

        self.config['handler'] = self.handle_client
        self.session_server = EncryptedSessionServer(**self.config)

    def load_config(self):
        with open(self.CONFIG_PATH, "r") as file:
            config = json.load(file)

        if self.is_config_valid(config):
            self.logger.info("Config file successfully loaded")
            config['ip_address'] = netifaces.ifaddresses(config.pop('interface')).get(netifaces.AF_INET)[0].get('addr')
            return config
        else:
            self.logger.error(self.error_message)
            raise InvalidConfig(self.error_message)

    def is_config_valid(self, config):
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

    async def handle_client(self, client_socket):
        print("got client")
        await client_socket.send(json.dumps({"message": "hi"}))
        res = await client_socket.recv()
        print(res)
