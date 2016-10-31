import socket
from termcolor import colored

target_host = '127.0.0.1'
target_port = 1200

# CREATE A SOCKET OBJECT
# Parameters used to identify an UDP Socket, see documentation

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# I added this line, because without it i won't be able to receive nothing
client.bind((target_host, target_port))

# Using UDP socket it is not a need to establish a connection, UDP is CONNECTIONLESS ( TCP establishes a channel)

# SEND SOME DATA

client.sendto('AAABBBCCC', (target_host, target_port))

# RECEIVE SOME DATA
# We are receiving some data on port that we binded, without a connection we need to know not only received data but
# also the sender (address, port) couple
data, addr = client.recvfrom(4096)

print colored('Received Data: ', 'red') + colored(data, 'green') + '\n' + colored('Sender Address/Port: ', 'red') + colored(str(addr), 'green')

# NB
# Exception handling is missing in this code, remember that it is a MUST
#
# YOU MUST HANDLE EXCEPTION