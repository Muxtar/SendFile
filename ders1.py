import socket
import json
import nmap
import sys
import time
from settings import *
import os
import color

class Main():
    def __init__(self):
        self.ip = self.setIp()
        self.port = 0
        self.fileName = 'VarpiNator'
        self.fileSize = 0
        self.settings()
        self.setIp()

    def settings(self):
        self.port = PORT['port']

    def setIp(self):
        return '192.168.1.105'

    @staticmethod
    def test(message):
        #lenMessage = len(message)
        #say = lenMessage*'='

        return f"{color.goby1}{message}{color.end}"

class server(Main):
    def __init__(self):
        super().__init__()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.listen(1)

    def upload(self):
        self.c, self.addr = self.server.accept()
        self.fileName = self.c.recv(1024).decode('utf-8')

        if input(f"{color.goby1}'{self.fileName}' Do you want to continue? [Yes/No]{color.end} ") != 'yes':
            self.c.send(f'0'.encode('utf-8'))
            return False, self.fileName

        self.c.send(f'1'.encode('utf-8'))

        self.uploadFile = open(self.fileName, 'wb')
        self.data = self.c.recv(1024)
        self.fileSize = 1024

        while self.data:
            self.uploadFile.write(self.data)
            self.data = self.c.recv(1024)

        self.uploadFile.close()
        self.server.close()
        return True, self.fileName

class client(Main):
    def __init__(self, fileName, ip):
        super().__init__()
        self.fileName = fileName
        self.client = socket.socket()
        self.client.connect((self.ip, self.port))

    def send(self):
        try:
            self.file = open(self.fileName, 'rb')
            self.readFile = self.file.read()

            self.client.sendall(self.fileName.encode('utf-8'))
            self.myBool = bool(int(self.client.recv(1024).decode('utf-8')))
        
            if self.myBool == True:
                while self.readFile:
                    self.client.sendall(self.readFile)
                    self.readFile = self.file.read()

                self.file.close()
                self.client.close()
                return True, 'Sending successful'

            else:
                return False, 'Your partner did not accept'

        except ConnectionRefusedError:
            return False, "Your partnet not connection"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        
        client1 = client(sys.argv[1], sys.argv[2])
        myBool, message = client1.send()
        print(client1.test(message))
        
    else:
        server().upload()

