from socket import *
import datetime as dt
class Client:
    client_id = ""
    socket_conneciton :  socket
    last_alive : dt.datetime


    def __init__(self, id:str, cleint_socket : socket,last_alive: dt.datetime) -> None:
        self.client_id = id
        self.socket_conneciton = cleint_socket
        self.last_alive = last_alive
        