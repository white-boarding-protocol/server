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
            address: returns the client address (ip_address, port_number). 
        """
        print("INFO: Server is listening for a connection")        
        self._server_ssl_socket.listen()
        (client_socket, address) = self._server_ssl_socket.accept()
        self.clients_dict[address]= client_socket
        print("INFO: Added client: "+ str(address))
        return address


    def transfer_data(self, data, address):
        """
        Transfers data to the specified client.

        Args:
            data ( type ): The data to be sent.
            address (tuple): client address (ip_address, port_number).

        Returns:
            int : amout of bytes sent to the client.
        """        
        return self.clients_dict.get(address).send(str.encode(data))

    def recv_data(self, address):
        """
        Receives data from the specified client.

        Args:
            address (tuple): client address (ip_address, port_number).

        Returns:
            byte object : represents the data received.
        """  
        return self.clients_dict.get(address).recv(self.BUFFER_SIZE)

    def close_client_connection(self, address):
        """
        Closes the connection for the specified client.

        Args:
            address (tuple): The client to close the connection to.

        Returns:
            None.
        """        
        return self.clients_dict.get(address).close()

    def close_server(self):
        """
        Closes the server socket.

        Returns:
            None.
        """        
        return self._server_ssl_socket.close()