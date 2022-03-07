import asyncio
import logging

import websockets


# Represents the session between a client and this server.
class SessionServer:
    def __init__(self, **kwargs):
        """
        Creates a websocket with tls and then listens for connections forever.
        
        Args:
            ip_address (string): Ip to be bound to 
            port_number (int): Port to be bound to
            handler (function): Function to be executed when a new event is received
            logger (Logger): Logger added to the socket for logging
            context (sslContext): Security context for tls, passed down from encryption layer
        Returns:
            new session object that handles client events
        """

        self._ip_address = kwargs.get('ip_address')
        self._port_number = kwargs.get('port_number')
        self._handler = kwargs.get('handler')
        self._ssl_context = kwargs.get('context')
        self._logger = logging.getLogger("Session")

    async def start_server(self):
        async with websockets.serve(self._handler, host=self._ip_address, port=self._port_number,
                                    logger=self._logger, ssl=self._ssl_context):
            print("server started...")
            await asyncio.Future()  # run forever
