import socket
from _thread import *
import sys

class Server():
    def __init__(self):
        self.server = '192.168.110.159'
        print(self.server)
        self.port = 5555  
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.status = ''
        self.running = True
        self.data_size = 1
        self.current_players = 0
        self.players = [{'id': 1, 'name': 'test', 'pos': (0, 0), 'open': True}, {'id': 2, 'name': 'test', 'pos': (0, 0), 'open': True}]
        
        self.player_1_pos = (0, 0, 1)
        self.player_2_pos = (0, 0, 2)
    
    def read_pos(self, str):
        str = str.split(",")
        return int(str[0]), int(str[1]), int(str[2])

    def make_pos(self, tuple):
        return str(tuple[0]) + "," + str(tuple[1]) + "," + str(tuple[2])
        
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
            player = 0
            if self.players[0]['open'] == True:
                player = 1
                self.players[0]['open'] = False
            elif self.players[1]['open'] == True:
                player = 2
                self.players[1]['open'] = False
                
            if player != 0:
                start_new_thread(self.threaded_client, (self.conn, str(player)))
    
    def threaded_client(self, conn, player):
        reply = ''
        _run = True
        print('client connected')
        conn.send(player.encode())
        player = int(player)
        
        while _run:
            try:
                data = conn.recv(2048).decode()
                data = self.read_pos(data)
                
                if not data:
                    self.status = 'Client disconnected'
                    self.current_players -= 1
                    _run = False
                    break
                else:
                    if int(data[2]) == 1:
                        reply = self.player_2_pos
                        self.player_1_pos = data
                    elif int(data[2]) == 2:
                        reply = self.player_1_pos
                        self.player_2_pos = data
                    # print('recieved: ', data)
                    # print('sending: ', reply)
                
                conn.sendall(str.encode(self.make_pos(reply)))
            except  socket.error as e:
                print(e)
                break
        print('Client disconnected')
        self.players[int(player) - 1]['open'] = True
        conn.close()
          
test_server = Server()
test_server.run()