import socket

class Network():
    def __init__(self, server_addr, server_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = f'{server_addr}'
        self.port = f'{server_port}'
        self.addr = (self.server, self.port)
        self.connected = False
        
        self.id = self.connect()
        self.pos = (0, 0)
        print(self.id)
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            recieved = self.client.recv(2048).decode()
            if recieved:
                self.connected = True
            return recieved
        except  socket.error as e:
            self.connected = False
            print(e)
            return e
        
    def send(self, data):
        try:
            self.client.send(str.encode(data))  
            return self.client.recv(2048).decode()
        except  socket.error as e:
            print(e)
            return e
        