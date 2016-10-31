#!/usr/bin/env python

import sys
import socket
import getopt
from termcolor import colored
import threading
import subprocess

# GLOBAL VARIABLE
listen = False
command = False
upload = False
execute = ''
target = ''
upload_destination = ''
port = 0
filename  = sys.argv[0].split('/')[-1]
shell_header = '<BHP:#> '
command_list =[
'''
-l --listen	                        - listen on [host]:[port] for
                                      incoming connections''',
'''
-e --execute=file_to_run            - execute the given file upon
                                      receiving a connection''',
'''
-c --command                        - initialize a command shell''',
'''
-u --upload=destination             - upon receiving connection upload a
                                      file and write to [destination]''']
def usage():
    print 'BHP Net Tool\n'

    print "Usage: %s -t target_host -p port" % filename

    print '' .join([str(a) for a in command_list])



def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # read the commandline options

    try:
            opts, args = getopt.getopt( sys.argv[1:],
                                        "hle:t:p:cu:",
                                        ["help","listen","execute","target","port","command","upload"])
    except  getopt.GetoptError as err:
            print str(err)
            usage()

    for o, a in opts:
            if o in ('-h', '--help'):
                usage()
            elif o in ('-l', '--listen'):
                listen = True
            elif o in ('-e', '--execute'):
                execute = a
            elif o in ('-c', '--commandshell'):
                command = True
            elif o in ('-u', '--upload'):
                upload_destination = a
            elif o in ('-t', '--target'):
                target = a
            elif o in ('-p', '--port'):
                port = int(a)
            else:
                assert False, 'Unhandled Option'

    # CLIENT OR SERVER? Basing on input there are different behaviors!

    # CLIENT:   according to well formed parameters, we are going to read an user's input and send it to our
    #           custom function that handles input from an user
    if not listen and len(target) and port > 0:
            client_sender()

    # SERVER:   simple defining a server loop that listens inputs from client side
    if listen:
            server_loop()

def client_sender():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # connect to our target host
        client.connect((target,port))

        while True:

                # once data are sended we are waiting for data back
                recv_len = 1
                response = ''

                # we are receiving data until there are always a response that fills the buffer
                # when we are receiving a data shorter it will be the last part to receive
                # question and if the last is exactely 4096? ( i don't know :( )
                while recv_len:
                        data = client.recv(4096)
                        recv_len = len(data)
                        response += data

                        if recv_len < 4096:
                                break

                print response
                # wait for more input, in python2.*:
                #                       RAW_INPUT:  read input from user as string
                #                       INPUT:      read input from user and try to execute as command (dangerous)
                #                      in python3.*:
                #                       RAW_INPUT:  suppressed
                #                       INPUT:      the same of RAW_INPUT in older python2.*, if you want obtain the same
                #                                   behavior of the older INPUT you need to eval(input())
                #
                # remember that read and try to execute a command inserted by an user can be very dangerous

                #flush_input()

                buffer = raw_input('')
                buffer += '\n'

                # send it off
                client.send(buffer)

    except Exception as e:
        print colored('[*] Exception ', 'red') + colored('exiting', 'yellow')
        print e
        client.close()

def server_loop():
        global target

        # if no target is defined, we listen on all interfaces
        if not len(target):
            target = '0.0.0.0'

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((target,port))
        server.listen(5)

        while True:
                client_socket, addr = server.accept()

                # spin off a thread to handle our new client
                client_thread = threading.Thread(target= client_handler, args=(client_socket,))
                print colored('[*] Connected New Client ', 'green') + colored(str('%s %d' % (target, port)), 'yellow')
                client_thread.start()

def run_command(command):
        # trim the newline
        command = command.rstrip()

        # run the command and get the output back
        try:
                    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell= True)
        except:
                    output = 'Failed to execute command.\r\n'

        #send the output back to the client
        return output

def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):
                #read in all of the bytes and write to our destination
                file_buffer = ''

                # keep reading data until none is available
                while True:
                            data = client_socket.recv(1024)

                            if not data:
                                        break
                            else:
                                        file_buffer += data

                # now we take these bytes and try to write them out
                try:
                            file_descriptor = open(upload_destination, 'wb')
                            file_descriptor.write(file_buffer)
                            file_descriptor.close()

                            # ack to the client for this operation
                            client_socket.send('Successfully saved file to %s\r\n' % upload_destination)
                except:
                            client_socket.send('Failed to save file to %s\r\n' % upload_destination)

    # check for command execution
    if command:
            while True:
                        # show a simple promt like a shell
                        client_socket.send(shell_header)

                        cmd_buffer = ''
                        # now we receive until newline character that ends a command
                        while '\n' not in cmd_buffer:
                                    cmd_buffer += client_socket.recv(1024)

                        print colored('************\n[*] Received Command: ', 'blue') + colored(cmd_buffer, 'green')
                        # execute and get the command output
                        response = run_command(cmd_buffer)

                        print colored('[*] Send Back Response\n************\n\n', 'blue')

                        # send back to the client the response
                        client_socket.send(response)

# Calling the main

def flush_input():
    try:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)
    except ImportError as e:
        import msvcrt
        print e
        while msvcrt.kbhit():
            msvcrt.getch()
main()