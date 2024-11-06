# this hosts a server that will serve math questions over a raw TCP socket on 127.0.0.1 requiring answers in under a second to the second decimal place.

# it is a lot more fun if you don't read the server code before attempting.

import threading
import random
import socket
import time

###################COLORS#################
color_RED = '\033[91m'
color_GRE = '\033[92m'
color_YELL = '\033[93m'
color_BLU = '\033[94m'
color_PURP = '\033[35m'
color_reset = '\033[0m'

SERVER = '127.0.0.1'
PORT = 1337
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print("\n" + color_BLU + f"[NEW CONNECTION] {addr} connected.\n" + color_reset)
    conn.send('Welcome to the math challenge. You need to answer my 25 math questions rounded to the second decimal place if the answer is not a whole number really quick ok\n'.encode())
    correct = 0
    ops = ['/', '*', '-', '+']
    while correct < 25: # they need 10 right

        val1 = random.randrange(25,200) # get a random val for 1
        if random.randrange(0, 3) == 1:
            val1 = '{}.{}'.format(val1, str(random.randrange(1, 999)).zfill(2))
        val2 = random.randrange(25, 200) # get a second random value
        if random.randrange(0, 3) == 1:
            val2 = '{}.{}'.format(val2, str(random.randrange(1, 999)).zfill(2))

        operation = random.choice(ops) # get a random operation
        problem = '{}{}{}'.format(val1, operation, val2) # put it all together
        ans = eval(problem) # solve the problem

        if str(ans).find('.') != -1: # if it is a float we cut it down to two decimal places
            ans = str(round(ans, 2))
        else: # if its not a float just convert to string
            ans = str(ans)

        start_time = time.time() # get the time right as we send the question

        conn.send(problem.encode() + '='.encode()) # send it
        client_ans = conn.recv(2048).decode() # get their response

        elapsed_time = time.time() - start_time  # get the time again

        client_ans = client_ans.replace('\n', '') # remove any trailing chars
        client_ans = client_ans.replace('\r', '')

        print('{}: Our ans: "{}" Their ans: "{}" in {} seconds'.format(addr[0].replace('\'', ''), ans, client_ans, str(round(elapsed_time, 5)))) # print the two to compare

        if str(client_ans) == str(ans): # check if they match
            if elapsed_time < 1: # did they take too long
                correct += 1
                print('{}: They got it right Total points: {}'.format(addr[0].replace('\'', ''), correct))

            else:
                print('{}: They got it right but were too slow, sending close'.format(addr[0].replace('\'', '')))
                conn.send('Too slow'.encode())
                conn.close()
                return

        else:
            print('{}: They got it wrong, closing'.format(addr[0].replace('\'', '')))
            conn.send('Wrong answer the correct answer was "{}"'.format(ans).encode())
            conn.close()
            return

    print('{}: They won, sending flag'.format(addr[0].replace('\'', '')))
    conn.send('Wow you are smart and fast your flag is flag{math_CTF011100010101010110000101}'.encode())
    conn.close()
    return


def start():
    server.listen()
    print(color_BLU + f"[LISTENING] Server is listening on {ADDR}" + color_reset)
    while True:
        conn, addr = server.accept()
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
    server_start()

if __name__ == '__main__':
    main()
