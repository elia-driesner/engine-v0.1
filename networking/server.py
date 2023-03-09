import socket
from _thread import *
import sys

class Server():
    def __init__(self):
        self.server = '192.168.0.139'
        print(self.server)
        self.port = 5555  
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = ''
        self.running = True
        self.data_size = 1
        self.current_players = 0
        
        self.pos = [(0, 0), (0, 0)]
    
    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1])

    def make_pos(self, tuple):
        return str(tuple[0]) + "," + str(tuple[1])
        
    def run(self):
        try:
            self.s.bind((self.server, self.port))
        except socket.error as e:
            print(str(e))
            
        self.s.listen(2)
        self.status = 'Server started, waiting for connection'
        print(self.status)
        
        while self.running:
            self.conn, self.addr = self.s.accept()
            
            start_new_thread(self.threaded_client, (self.conn, self.current_players))
    
    def threaded_client(self, conn, player):
        reply = ''
        _run = True
        print('client connected')
        conn.send(str(player).encoded())
        
        while _run:
            try:
                data = conn.recv(2048).decode()
                print(data)
                if data != 'test':
                    data = self.read_pos(data)
                else:
                    conn.sendall(str.encode('tested'))
                self.pos[player] = data
                print(data)
                
                if not data:
                    self.status = 'Client disconnected'
                    self.current_players -= 1
                    _run = False
                    break
                else:
                    if player == 0:
                        reply = self.pos[1]
                    elif player == 1:
                        reply = self.pos[0]
                    print('recieved: ', data)
                    print('sending: ', reply)
                
                conn.sendall(str.encode(self.make_pos(reply)))
            except:
                break
        print('Client disconnected')
        conn.close()
          
test_server = Server()
test_server.run()