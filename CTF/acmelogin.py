# it is a lot more fun if you don't read the server code before attempting.
# had a lot of fun making this one :)

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
Your Credentials are safely store in the file 'creds_acmeloginctf'
and are checked each time at login for changes

You can request the code by sending give_code as the username

"""

code = """
def handle_client(conn, addr):
    print("\\n" + color_BLU + f"[NEW CONNECTION] {addr} connected.\\n" + color_reset)

    conn.send(logo.encode())

    while True:
        try:

            with open('creds_acmeloginctf', 'r') as f:
                cred_data = f.read()
                f.close()

            cred_data = cred_data.split('\\n')
            while '' in cred_data:
                cred_data.remove('')

            username = cred_data[0]
            password = cred_data[1]


            conn.send('username: '.encode())
            given_username = conn.recv(8192).decode()
            if given_username.endswith('\\n'):
                given_username = given_username[:given_username.rfind('\\n')]

            print('{}: Gave a username of: "{}"'.format(addr[0].replace('\\'', ''), given_username))

            if eval('\\'{}\' == \\'{}\\''.format(username, given_username)):
                conn.send('password: '.encode())

                given_password = conn.recv(8192).decode()

                if given_password.endswith('\\n'):
                    given_password = given_password[:given_password.rfind('\\n')]

                print('{}: Gave a password of: "{}"'.format(addr[0].replace('\\'', ''), given_password))

                if eval('\\'{}\\' == \\'{}\\''.format(password, given_password)):
                    conn.send('Successfully loggedin!\\n'.encode())
                    conn.send('Heres your flag: flag{acmeLog1n1100011010110}\\n'.encode())
                    conn.close()
                    return
                else:
                    conn.send('Invalid Password\\n'.encode())
                    continue
            else:
                conn.send('Invalid Username\\n'.encode())
                continue

        except Exception as e:
            print(str(e))
            import traceback
            traceback.print_exc()
            conn.send('What did you just send me?????\\n'.encode())
            conn.close()
            return
"""

def handle_client(conn, addr):
    print("\n" + color_BLU + f"[NEW CONNECTION] {addr} connected.\n" + color_reset)

    conn.send(logo.encode())

    while True:
        try:

            with open('creds_acmeloginctf', 'r') as f:
                cred_data = f.read()
                f.close()

            cred_data = cred_data.split('\n')
            while '' in cred_data:
                cred_data.remove('')

            username = cred_data[0]
            password = cred_data[1]


            conn.send('username: '.encode())
            given_username = conn.recv(8192).decode()
            if given_username.endswith('\n'):
                given_username = given_username[:given_username.rfind('\n')]

            print('{}: Gave a username of: "{}"'.format(addr[0].replace('\'', ''), given_username))

            if given_username == 'give_code':
                conn.send(code.encode())
                continue

            if eval('\'{}\' == \'{}\''.format(username, given_username)):
                conn.send('password: '.encode())

                given_password = conn.recv(8192).decode()

                if given_password.endswith('\n'):
                    given_password = given_password[:given_password.rfind('\n')]

                print('{}: Gave a password of: "{}"'.format(addr[0].replace('\'', ''), given_password))

                if eval('\'{}\' == \'{}\''.format(password, given_password)):
                    conn.send('Successfully loggedin!\n'.encode())
                    conn.send('Heres your flag: flag{acmeLog1n1100011010110}\n'.encode())
                    conn.close()
                    return
                else:
                    conn.send('Invalid Password\n'.encode())
                    continue
            else:
                conn.send('Invalid Username\n'.encode())
                continue

        except Exception as e:
            print(str(e))
            import traceback
            conn.send('What did you just send me?????\n'.encode())
            conn.send(traceback.format_exc().encode())
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


#this starts the server which calls start() to create the handle client thread
def server_start():
    print("[STARTING] server is starting...")
    try:
        start_thread = threading.Thread(target=start)
        start_thread.start()
    except BaseException as e:
        print(color_RED + "[ERROR] " + str(e) + color_reset)
    time.sleep(1)

def main():
    yn = input('WARNING: This service will render your host vulnerable as long as the ctf script is running.\nYou are solely liable for any damage that occurs by running this tool.\nONLY run it on a secure network or localhost.\nDo you want to proceed y/n: ')
    if yn.lower() == 'y':
        with open('creds_acmeloginctf', 'w') as f: # make the creds file
            our_uname = ''.join(random.choices(string.ascii_uppercase, k=random.randrange(8, 15)))
            our_pass = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=random.randrange(18, 25)))
            f.write('{}\n'.format(our_uname))
            f.write(our_pass)
        server_start()

if __name__ == '__main__':
    main()
