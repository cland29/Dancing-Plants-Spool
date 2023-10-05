import socket
import threading


def main():
    print("hello world")

    PORT = 5050
    SERVER = socket.gethostbyname(socket.gethostname())
    ADDR = (SERVER, PORT)
    print(SERVER)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    start_server()

def handle_client(conn, addr):
    pass

def start_server():
    pass





if __name__ == "__main__":
    main()