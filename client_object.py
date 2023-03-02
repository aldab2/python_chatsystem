from socket import *
class Client:
    client_id = ""
    socket_conneciton :  socket


    def __init__(self, id:str, cleint_socket : socket) -> None:
        self.client_id = id
        self.socket_conneciton = cleint_socket
        