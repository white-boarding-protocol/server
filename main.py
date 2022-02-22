import ssl
import asyncio

from events.whiteboard.whiteboard_event import WhiteboardEvent
from session.session_server import SessionServer


async def handler(websocket):
    print("connected")
    await websocket.send("slm")
    print("sent")
    await websocket.close()
    message = await websocket.recv()
    print(message)
    print("close")


if __name__ == "__main__":
    s = WhiteboardEvent(1)
    print(s.__class__)
    # # TODO: Later to be replaced with enc layer function
    # context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # context.load_cert_chain('./cert/cert.pem', './cert/key.pem')
    #
    # # Session layer
    #
    # session = SessionServer(ip_address="127.0.0.1", port_number=5555, context=context, handler=handler)
    # asyncio.run(session.start_server())

    # server = Threaded_Server(ip_address= "localhost", port_number= 5555, context= context)

    # server.listen_for_clients()

    # TEST
    # client = server.wait_for_connection()
    # server.transfer_data("hello client!", client)
    # print("From client: "+ server.recv_data(client).decode())
    # server.close_client_connection(client)
    # server.close_server()
