import socket
from termcolor import colored
import threading

bind_ip = '0.0.0.0'
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# server binding, without this your server instance is useless
server.bind((bind_ip, bind_port))

# backlog parameter see documentation
server.listen(5)

print colored('[*] ', 'red') + colored(str('Listening on %s:%d' % (bind_ip,bind_port)), 'yellow')


# CLIENT-HANDLING THREAD
def handle_client(client_socket):

    # print out what the clients sends
    request = client_socket.recv(1024)
    print colored('[*] ', 'blue') + colored(str('Received: %s' % request), 'yellow')

    # send back a packet
    client_socket.send('ACK!')

    # close socket (BEST PRACTICE)
    client_socket.close()

# MAIN LOOP
while True:

    # we are waiting a message
    client, addr = server.accept()

    print colored('[*] ', 'red') + colored(str('Accepted connection from: %s:%d' % (addr[0], addr[1])), 'yellow')

    # spin up our client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()

# In printing blue is for thread, red is for server

# 1) Instancing and binding server
# 2) Defining a thread invocated to answer
# 3) Listening and answering in loop

# You can use a TCP client to send messagge observing behavior

# NB
# Exception handling is missing in this code, remember that it is a MUST
#
# YOU MUST HANDLE EXCEPTION