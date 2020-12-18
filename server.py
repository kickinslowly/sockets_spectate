import socket
import threading
import pyautogui

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
conns = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def spectate():
    spectate_button = pyautogui.locateCenterOnScreen('spectate.png', confidence=.7)
    if spectate_button:
        pyautogui.moveTo(spectate_button)
        pyautogui.click()
        pyautogui.click(spectate_button)
        print('SUCCESS YOU ARE NOW SPECTATING THE GAME')
    else:
        print('Failure to locate spectate button.')


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)

                print(f'[{addr}] {msg}')
                conn.send('Msg received'.encode(FORMAT))
        except:
            if conn in conns:
                conns.remove(conn)
                conn.close()
                break


def command():
    while True:
        global conns
        input()
        for i in conns:
            i.send('spectate'.encode(FORMAT))
        spectate()


def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER}')
    command_thread = threading.Thread(target=command, args=())
    command_thread.start()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        conns.append(conn)
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")
        print(len(conns))
        print(conns)


print('[STARTING] server is starting.....')
start()
