import socket
from threading import Thread


def listen_client(client):
    while True:
        try:
            msg = client.recv(1024).decode()
        except Exception as e:
            print(f"Error: {e}")
            client_sockets.remove(client)
        else:
            print(f"Message -  {msg}")
        for client_socket in client_sockets:
            client_socket.send(msg.encode())


hostname = ""
port = 5555
client_sockets = set()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((hostname, port))
server.listen()
print("Server running")
while True:
    client_socket, client_address = server.accept()
    print(f"{client_address} connected")
    client_sockets.add(client_socket)
    t = Thread(target=listen_client, args=(client_socket,))
    t.daemon = True
    t.start()
for cs in client_sockets:
    cs.close()
    print("Threads are closed")
server.close()
