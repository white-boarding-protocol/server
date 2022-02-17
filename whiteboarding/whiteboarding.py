import json
import logging

from whiteboarding.exceptions import InvalidConfig


class Whiteboarding:
    CONFIG_PATH = "/etc/whiteboarding/config.json"
    CONFIG_MANDATORY_FIELDS = ["enable_ssl", "listen_port"]
    SSL_REQUIRED_FIELDS = ["cert_path", "key_path"]

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.error_message = None
        self.config = self.load_config()

    def load_config(self):
        with open(self.CONFIG_PATH, "r") as file:
            config = json.load(file)

        if self.is_config_valid(config):
            self.logger.info("Config file successfully loaded")
            return config
        else:
            self.logger.error(self.error_message)
            raise InvalidConfig(self.error_message)

    def is_config_valid(self, config):
        for mandatory_key in self.CONFIG_MANDATORY_FIELDS:
            if mandatory_key not in config:
                self.error_message = f"{mandatory_key} not included in the config file"
                return False

            if mandatory_key == "enable_ssl" and type(config["enable_ssl"]) != bool:
                self.error_message = f"{mandatory_key} value should be boolean"

        if config["enable_ssl"]:
            for mandatory_key in self.SSL_REQUIRED_FIELDS:
                if mandatory_key not in config:
                    self.error_message = f"{mandatory_key} not included in the config file when ssl is enabled"
                    return False

        return True
