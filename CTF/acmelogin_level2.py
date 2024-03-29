# it is a lot more fun if you don't read the server code before attempting.

import threading
import random
import socket
import string
import time

###################COLORS#################
color_RED = '\033[91m'
color_GRE = '\033[92m'
color_YELL = '\033[93m'
color_BLU = '\033[94m'
color_PURP = '\033[35m'
color_reset = '\033[0m'

SERVER_IP = '127.0.0.1'
PORT_PORT = 1337
ADDR = (SERVER_IP, PORT_PORT)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)

creds_list = []

logo = """
                              ▄
                            ▄▄▄▄▄  
                          ▄▄▄▄▄▄▄▄▄
                       ▗  ▄▄▄▄▄▄▄▄▄  ▖
                      ▄▄▄   ▄▄▄▄▄   ▄▄▄
                    ▄▄▄▄▄▄▄   ▄   ▄▄▄▄▄▄▄
                  ▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄
                ▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄
              ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

                           A C M E
                           SYSTEMS

You can request the code by sending give_code as the username

"""

def change_creds(username, password, session_index): # this will cycle the creds every second
    while True:
        username = ''.join(random.choices(string.ascii_uppercase, k=random.randrange(8, 15)))
        password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randrange(18, 25)))
        creds_list[session_index] = '{}:{}'.format(username, password)
        time.sleep(1)

def handle_client(conn, addr):
    print("\n" + color_BLU + f"[NEW CONNECTION] {addr} connected.\n" + color_reset)

    conn.send(logo.encode())

    username = ''.join(random.choices(string.ascii_uppercase, k=random.randrange(8, 15)))
    password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randrange(18, 25)))

    creds_list.append('{}:{}'.format(username, password))
    session_index = creds_list.index('{}:{}'.format(username, password))

    credthread = threading.Thread(target=change_creds, args=(username, password, session_index))
    credthread.start()

    while True:
        try:
            conn.send('username: '.encode())
            given_username = conn.recv(8192).decode()
            if given_username.endswith('\n'):
                given_username = given_username[:given_username.rfind('\n')]

            print('{}: Gave a username of: "{}"'.format(addr[0].replace('\'', ''), given_username))

            if given_username == 'give_code':
                creds = creds_list[session_index].split(':')
                code = """
def handle_client(conn, addr):
    print("\\n" + color_BLU + f"[NEW CONNECTION] {addr} connected.\\n" + color_reset)

    conn.send(logo.encode())

    username = """ + creds[0] + """
    password = """ + creds[1] + """

    while True:
        try:
            conn.send('username: '.encode())
            given_username = conn.recv(8192).decode()
            if given_username.endswith('\\n'):
                given_username = given_username[:given_username.rfind('\\n')]

            print('{}: Gave a username of: "{}"'.format(addr[0].replace('\\'', ''), given_username))
            
            if given_username == 'give_code':
                print()

            conn.send('password: '.encode())
            given_password = conn.recv(8192).decode()
            if given_password.endswith('\\n'):
                given_password = given_password[:given_password.rfind('\\n')]

            print('{}: Gave a password of: "{}"'.format(addr[0].replace('\\'', ''), given_password))


            if username == given_username and password == given_password:
                print('{}: Got it sending flag'.format(addr[0].replace('\\'', '')))
                conn.send('Successfully Loggedin!\\n'.encode())
                conn.send('Heres your noflag1u'.encode())
                conn.close()
            else:
                conn.send('Invalid Creds\\n'.encode())
                continue


        except Exception as e:
            print(str(e))
            conn.send('What did you just send me?????\\n'.encode())
            conn.close()
            return
"""
                conn.send(code.encode())
                continue

            conn.send('password: '.encode())
            given_password = conn.recv(8192).decode()
            if given_password.endswith('\n'):
                given_password = given_password[:given_password.rfind('\n')]

            print('{}: Gave a password of: "{}"'.format(addr[0].replace('\'', ''), given_password))

            creds = creds_list[session_index].split(':')
            print(creds)

            if creds[0] == given_username and creds[1] == given_password:
                print('{}: Got it sending flag'.format(addr[0].replace('\'', '')))
                conn.send('Successfully Loggedin!\n'.encode())
                conn.send('Heres your flag flag{acmeLoginlvl2110001100011110}'.encode())
                conn.close()
                return
            else:
                conn.send('Invalid Creds\n'.encode())
                continue


        except Exception as e:
            print(str(e))
            conn.send('What did you just send me?????\n'.encode())
            conn.close()
            return


def start():
    server_socket.listen()
    print(color_BLU + f"[LISTENING] Server is listening on {ADDR}" + color_reset)
    while True:
        conn, addr = server_socket.accept()
        try:
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
        except BaseException as e:
            print(color_RED + "[ERROR] " + str(e) + color_reset)
            conn.close()


# this starts the server which calls start() to create the handle client thread
def server_start():
    print("[STARTING] server is starting...")
    try:
        start_thread = threading.Thread(target=start)
        start_thread.start()
    except BaseException as e:
        print(color_RED + "[ERROR] " + str(e) + color_reset)
    time.sleep(1)


def main():
    server_start()


if __name__ == '__main__':
    main()
