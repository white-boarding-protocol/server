import socket

# Represents the session between a client and this server.
class Session:
    
    clients_dict = {}
    BUFFER_SIZE = 4096

    def __init__(self, **kwargs):
        """
        Creates a net socket and then wraps it around tls for security
        
        Args:
            ip_address (string): Ip to be bound to 
            port_number (int): port to be bound to
            context (sslContext): security context for tls, passed down from encryption layer.
        Returns:
            new session object
        """        
        self._ip_address = kwargs.get('ip_address')
        self._port_number = kwargs.get('port_number')
        self._ssl_context = kwargs.get('context')
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.bind((self._ip_address, self._port_number))
        print("INFO: Server is bound to IP and port: "+str(self._ip_address)+" ,"+str(self._port_number))

        # Handle ssl connection
        self._server_ssl_socket = self._ssl_context.wrap_socket(self._socket, server_side=True)

    def wait_for_connection(self):
        """
        Listens for connections and accepts clients. 
        Adds the clients to the dict and returns their address.

        Returns:
            client: {"client_address": address, "client_socket": client_socket}
        """
        try:
            print("INFO: Server is listening for a connection")        
            self._server_ssl_socket.listen()
            (client_socket, address) = self._server_ssl_socket.accept()
            self.clients_dict[address]= client_socket
            print("INFO: Added client: "+ str(address))
            return {"client_address": address, "client_socket": client_socket}
        except:
            self._server_ssl_socket.close()
            return
        


    def transfer_data(self, data, client):
        """
        Transfers data to the specified client

        Args:
            data ( type ): The data to be sent
            client (SSLSocket): client socket

        Returns:
            int : amout of bytes sent to the client
        """        
        return client.send(str.encode(data))

    def recv_data(self, client):
        """
        Receives data from the specified client

        Args:
            client (SSLSocket): client socket

        Returns:
            byte object : represents the data received
        """  
        return client.recv(self.BUFFER_SIZE)

    def close_client_connection(self, client):
        """
        Closes the connection for the specified client

        Args:
            client: {"client_address": address, "client_socket": client_socket}

        Returns:
            None
        """
        # Remove client.
        self.clients_dict.pop(client.get("client_address"))
        return client.get("client_socket").close()

    def close_server(self):
        """
        Closes the server socket

        Returns:
            None
        """
        self.clients_dict.clear()
        return self._server_ssl_socket.close()

    def get_clients_addresses(self):
        """
        Returns all client addresses stored in session

        Returns:
            [list]: clients addresses
        """        
        return self.clients_dict.keys()

    def get_clients_sockets(self):
        """
        Returns all client SSLSockets stored

        Returns:
            [SSLSocket]: clients secure sockets
        """        
        return self.clients_dict.items()