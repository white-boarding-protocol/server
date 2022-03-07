import ssl
import logging

from session.session_server import SessionServer


class EncryptedSessionServer:
    def __init__(self, **kwargs):
        self._ssl_enabled = kwargs.get("ssl_enabled")
        self._ssl_cert_path = kwargs.get("ssl_cert_path")
        self._ssl_key_path = kwargs.get("ssl_key_path")
        self._websocket_server = None

        self._handler = kwargs.get('handler')
        self._ip_address = kwargs.get('ip_address')
        self._port_number = kwargs.get('port_number')
        self._logger = logging.getLogger("Security")

    def get_ssl_context(self):
        if self._ssl_enabled:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            ssl_context.load_cert_chain(certfile=self._ssl_cert_path, keyfile=self._ssl_key_path)
            self._logger.info("SSL context loaded")
            return ssl_context
        self._logger.info("SSL context skipped")
        return None

    async def start_server(self):
        self._websocket_server = SessionServer(handler=self._handler, ip_address=self._ip_address,
                                               port_number=self._port_number, context=self.get_ssl_context())
        await self._websocket_server.start_server()
