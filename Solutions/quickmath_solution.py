# this is as short as I was able to get it.
# all that this script does is connect to IP on port 1337, capture the banner and then recv each given math problem solve it with eval() and then round()
# sending the answer back after converting from a float/int to a string then to bytes. Finally once you get the flag it prints in an error as eval() cannot understand the flag.
import socket
client_socket = socket.socket()
client_socket.connect(('127.0.0.1', 1337))
client_socket.recv(len('Welcome to the math challenge. You need to answer my 25 math questions rounded to the second decimal place if the answer is not a whole number really quick ok\n'))
while True:
    client_socket.send(str(round(eval(client_socket.recv(2048).decode()), 2)).encode())
