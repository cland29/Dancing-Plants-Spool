import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "10.10.1.84"#"192.168.1.125"
ADDR = (SERVER, PORT)

def main():
    print("Trying to connect!")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    send(client, "Hello World!")
    for i in range(10):
        send(client, "GetPosition")
    send(client, DISCONNECT_MESSAGE)

def send(client, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode())




if __name__ == "__main__":
    main()