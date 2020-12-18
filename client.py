import socket
import time
import pyautogui

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = 'DISCONNECT!'
SERVER = '192.168.0.122'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def spectate():
    spectate_button = pyautogui.locateCenterOnScreen('spectate.png')
    if spectate_button:
        pyautogui.moveTo(spectate_button)
        pyautogui.click()
        pyautogui.click(spectate_button)
        print('SUCCESS YOU ARE NOW SPECTATING THE GAME')
    else:
        print('Failure to locate spectate button.')


def send(msg):
    global client

    try:

        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        return_msg = client.recv(2048).decode(FORMAT)
        print(f'Masters says, "{return_msg}"')
        waiting = True
        while waiting:
            command_msg = client.recv(2048).decode(FORMAT)
            if command_msg == 'spectate':
                print('Master has commanded me to spectate.')
                spectate()
                waiting = False
    except:
        print('Failure to connect.')
        time.sleep(.1)
        print('Attempting reconnect.')
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect(ADDR)
        except:
            pass


while True:
    send('Armed and waiting for command to spectate!')
    time.sleep(.1)
