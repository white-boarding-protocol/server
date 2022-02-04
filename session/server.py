import threading
from session.session import Session

class Threaded_Server:
    
    client_threads = []

    def __init__(self, **kwargs):
        self._ip_address = kwargs.get('ip_address')
        self._port_number = kwargs.get('port_number')
        self._ssl_context = kwargs.get('context')
        # Start a new session
        self._session = Session(ip_address= self._ip_address, port_number= self._port_number, context= self._ssl_context)
    
    def listen_for_clients(self):
        # Listen and accept forever.
        while True:
            try:
                client = self._session.wait_for_connection()
                client_thread = threading.Thread(target= self.handle_client, args= (client.get("client_address"), client.get("client_socket")))
                self.client_threads.append(client_thread)
                client_thread.start()
            except:
                self._session.close_server()
        

    def handle_client(self, client_address, client_socket):
        print("INFO: Started a new server thread for client " + str(client_address))
        while True:
            try:
                data = self._session.recv_data(client_socket)
                if data:
                    print(threading.current_thread().getName() +" received data from client: "+str(data) +" from client: " + str(client_address))
                    self._session.transfer_data("Hello client "+ str(client_address), client_socket)
            except:
                self._session.close_client_connection({"client_address": client_address, "client_socket":client_socket})

