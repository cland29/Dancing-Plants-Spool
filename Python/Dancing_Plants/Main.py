import random
import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
def main():
    print("hello world")


    print(SERVER)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[Starting] Server is starting")
    start_server(server)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if (msg == "GetPosition"):
                conn.send(str(random.randint(10, 20)).encode(FORMAT));
            else:
                print(f"[{addr}] {msg}")
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                conn.send("Msg received".encode(FORMAT))

    conn.close()


def start_server(server: socket):
    server.listen()
    print(f"[LISTENING] SERVER is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def run_pyqt_interface():
    print()




if __name__ == "__main__":
    main()