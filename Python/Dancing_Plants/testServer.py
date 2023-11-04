import random
import socket
import threading
import time
import math
import matplotlib.pyplot as plt
import select

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

setpoint_lock = threading.Lock()
setpoint = 0




def main():
    print("hello world")

    print(SERVER)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)

    print("[Starting] Server is starting")
    start_server(server)


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    x_val = [10] * 50
    y_val = [0] * 50

    connected = True
    count = 0
    '''
    while connected:
        count += 1
        conn.send(str(count).encode(FORMAT))
        time.sleep(0.002)
    '''
    while connected:

        for i in range(720):
            pos = get_send_setpoint()
            num = f"{pos:06}"
            print(f"{i}: Sending {num}")
            conn.send(f"{num},".encode(FORMAT))
            time.sleep(0.02)
        conn.send((DISCONNECT_MESSAGE + ",").encode(FORMAT))
        '''
        for i in range(720):
            pos = int(-math.cos(i * math.pi/180*2) * 300 + 400)
            num = f"{pos:06}"
            print(f"{i}: Sending {num}")
            conn.send(f"{num},".encode(FORMAT))
            time.sleep(0.02)
        conn.send((DISCONNECT_MESSAGE + ",").encode(FORMAT))
        '''

        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:

            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if (msg == "GetPosition"):
                '''
                send_back = input()
                if not send_back.isdigit():
                    print("Please enter a numeric number")
                    send_back = input()

                conn.send(str(send_back).encode(FORMAT))

                '''

                conn.send(str(-200 + 200 * math.sin((time.time() % 18) / 9 * math.pi)).encode(FORMAT))



            else:
                print(f"[{addr}] {msg}")
                if msg == DISCONNECT_MESSAGE:
                    connected = False
                conn.send(f"Msg received {count}".encode(FORMAT))
                count += 1

    conn.close()

def setpoint_thread():
    print("Starting setpoint changing thread")
    while True:
        time.sleep(2)
        print("Setting to 500")
        set_send_setpoint(500)
        time.sleep(2)
        print("Setting to 100")
        set_send_setpoint(100)


def start_server(server: socket):
    server.listen()
    print(f"[LISTENING] SERVER is listening on {SERVER}")

    setpoint_changing_thread = threading.Thread(target=setpoint_thread)
    setpoint_changing_thread.start()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

def get_send_setpoint():
    setpoint_lock.acquire()
    temp = setpoint
    setpoint_lock.release()
    return temp

def set_send_setpoint(new_setpoint):
    setpoint_lock.acquire()
    global setpoint
    setpoint = new_setpoint
    setpoint_lock.release()
def run_pyqt_interface():
    pass
    # print()


if __name__ == "__main__":
    main()