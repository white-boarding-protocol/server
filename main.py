from ipaddress import ip_address
from session.session import Session

if __name__ == "__main__":
    server = Session(ip_address= "localhost", port_number= 5555)
    client = server.wait_for_connection()
    server.transfer_data("hello client!", client)
    print("From client: "+ server.recv_data(client).decode())
    server.close_client_connection(client)
    server.close_server()
