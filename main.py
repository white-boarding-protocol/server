import ssl
import asyncio
import session.session

if __name__ == "__main__":
    
    # TODO: Later to be replaced with enc layer function
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('./cert/cert.pem', './cert/key.pem')

    # Session layer

    asyncio.run(session(ip_address= "localhost", port_number= 5555, context= context))

    # server = Threaded_Server(ip_address= "localhost", port_number= 5555, context= context)

    # server.listen_for_clients()

    # TEST
    # client = server.wait_for_connection()
    # server.transfer_data("hello client!", client)
    # print("From client: "+ server.recv_data(client).decode())
    # server.close_client_connection(client)
    # server.close_server()
