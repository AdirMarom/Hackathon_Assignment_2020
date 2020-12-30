import socket
import threading
import sys
import os
import time
import random
from multiprocessing.connection import Listener
from select import select
from socket import *

SERVER_PORT = 2080
client_IP = gethostbyname(gethostname())
sorce_port=13117

class Client():
    def __init__(self,team_name):
        self.teamName = team_name
        self.receievedData = False
        self.udp_socket = socket(AF_INET, SOCK_DGRAM)
        self.tcp_socket = socket(AF_INET,SOCK_STREAM)

    def listenToBroadcast(self):
        # Creates a thread to start listening for broadcasts.
        thread = threading.Thread(target=self.listen)
        thread.start()

    def listen(self):
        #s = socket(AF_INET,SOCK_DGRAM)
        print( "Client started, listening for offer requests...")

        # Binds client to listen on port self.port. (will be 13117)
        try:
            self.udp_socket.bind(('', sorce_port))
        except:
            self.listen()
        # Receives Message
        message= self.udp_socket.recvfrom(1024)
        # Message Teardown.
        # magic_cookie = message[:4]
        # message_type = message[4]
        port_tcp = message[0][5:]
        server_port=int.from_bytes(port_tcp, byteorder='big', signed=False)
        m=message[1][0]
        self.connectTCPServer(server_port,m)

    def on_press(self,key):
        print('{0} pressed'.format(key))
        key_str = str(key)
        key_byte = key_str.encode("utf-8")
        self.tcp_socket.sendall(key_byte)

    def on_release(self,key):
        print('{0} release'.format(key))
        if key == key.esc:
            # Stop listener
            return False




    def connectTCPServer(self,port_tcp,m):
        s = socket(AF_INET,SOCK_STREAM)
        # connect to tcp server
        #maybe because we are in ubuntu

        s.connect(('127.0.1.1', port_tcp))
        # Sending team name
        s.send(bytes(self.teamName, encoding='utf8'))

        #with Listener(on_press=self.on_press) as listener:
         #   # listener.join()
          #  data = self.tcp_socket.recv(1024)
           # listener.stop()
            #print("\n\n" + data.decode("utf-8"))


       # # Receive data from Server
        data = str(s.recv(1024), 'utf-8')
        print(data)

#
       # # Setting blocking to false, Data to none and removing key presses representation
        data = None
        s.setblocking(False)
        #capture characters without press enter?
        os.system("stty raw -echo")
        while True:
       #     # if data is recieved it will stop and print, else it will send every key press to the server.
            try:
                data = s.recv(1024)
            except:
                pass
            if data:
                os.system("stty -raw echo")
                data = str(data, 'utf-8')
                print(data)
                break
            else:
                rlist,_,_= select([sys.stdin],[],[],0.1)
                if rlist:
                    print("got here")
                    s.send("dor")
                    c = sys.stdin.readline()
                    s.send(bytes(c, encoding='utf8'))
        s.close()