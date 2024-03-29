import socket

class Network():
    def __init__(self, server_addr, server_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = f'{server_addr}'
        self.port = server_port
        self.addr = (self.server, self.port)
        self.connected = False
        
        self.id = self.connect()
        self.pos = (0, 0)
        print(self.id)
        
    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1]), int(str[2])

    def make_pos(self, tuple):
        return str(tuple[0]) + "," + str(tuple[1]) + "," + str(tuple[2])
        
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
        
# n = Network('192.168.56.110', 5555)
# while True:
#     pos = (0, 0, 0)  
#     if int(n.id) == 1:
#         pos = (0, 0, 1)  
#     else:
#         pos = (100, 100, 2)      
#     pos = (pos[0], pos[1], n.id)
#     print(n.send(n.make_pos(pos)))
