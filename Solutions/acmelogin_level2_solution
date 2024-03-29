import socket
client_socket = socket.socket() # setup the socket
client_socket.connect(('127.0.0.1', 1337)) # connect
client_socket.recv(2048) # get the banner and do nothing
client_socket.recv(1024) # get the username: that it sends
client_socket.send('give_code'.encode()) # send give_code so we get the code
code = client_socket.recv(8192).decode() # get the code
code = code.split('\n') # split the code into a list
username = ''
password = ''
for line in code: # iterate through the given code looking for the first instance of username and password
    if line.find('username') != -1 and username == '':
        username = line.split('=')[1].replace(' ', '') # split and replace magik
    if line.find('password') != -1 and password == '':
        password = line.split('=')[1].replace(' ', '')
client_socket.recv(1024) # get the username: that it sends
client_socket.send(username.encode()) # send the username we found
client_socket.recv(1024) # get the password: that it sends
client_socket.send(password.encode()) # send the password we found
for x in range(2): # get the next two outputs from the server
    print(client_socket.recv(1024).decode())
