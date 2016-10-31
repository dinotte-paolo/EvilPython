import socket

target_host = 'www.google.it'
target_port = 80

# CREATE A SOCKET OBJECT
# Create a socket object
# AF_INET indicates we use standard IPv4 address or hostname
# SOCK_STREAM indicates it is a TCP client
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# CONNECT THE CLIENT
# see connect method in original documentation (couple formed by host and port)
client.connect((target_host, target_port))

# SEND SOME DATA
client.send('GET / HTTP/1.1\r\nHost: google.it\r\n\r\n')

# RECEIVE SOME DATA
response = client.recv(4096)

print response

# NB
# Exception handling is missing in this code, remember that it is a MUST
#
# YOU MUST HANDLE EXCEPTION