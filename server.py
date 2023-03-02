import socket
import threading
import client_object as c
import utils
import time
import datetime as dt


# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        if  isinstance(client, c.Client):
            client.socket_conneciton.send(message)
        else :
            print("Error, Found Corrupted Client... Terminating.")


def remove_client(client : c.Client):
    clients.remove(client)
    client.socket_conneciton.close()
    broadcast('{} left!'.format(client.client_id).encode())
    time.sleep(1)
    broadcast("Active users are {}\n".format(get_active_users()).encode())
    



# Handling Messages From Clients
def handle(client : c.Client):
    while True:
        try:
        
            command = client.socket_conneciton.recv(1024).decode()
            dest,source,message,command = utils.parse_command(command)
            if command == utils.INVALID_COMMAND:
                client.socket_conneciton.send("From Server: Invalid command\n".encode())

            if command == utils.KEYWORD_LIST:
                print("recived list")
                client.socket_conneciton.send("Active users are {}\n".format(get_active_users()).encode())

            if command ==utils.KEYWORD_QUIT:
                remove_client(client)
                break
            if command ==utils.KEYWORD_ALIVE:
                print("Alive recived from clinet:{}".format(client.client_id))
                client.last_alive  = dt.datetime.now()
                client.socket_conneciton.send("From Server: alive updated".encode())

            if command == utils.KEYWORD_MESSAGE:
                dest_client: c.Client = get_client_by_id(dest)
                if dest_client == None:
                    client.socket_conneciton.send("The client {} is not online".format(dest,).encode())
                else :
                    #client.socket_conneciton.send("The message was sent".encode())
                    dest_client.socket_conneciton.send("<{}>:{}".format(client.client_id,message.strip()).encode())
            
        except Exception as e:
            print(e)
            # Removing And Closing Clients
            remove_client(client)
            break

# Receiving / Listening Function
def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store Nickname
        client.send('@INIT,{}'.format(utils.ALIVE_INTERVAL).encode())
        command = client.recv(1024).decode()
        client_id = utils.parse_command(command)[0].strip()
        client_obj = c.Client(client_id,client,last_alive=dt.datetime.now())
        clients.append(client_obj)

        # Print And Broadcast Nickname
        print("Client ID is {}".format(client_id))
        broadcast("{} joined!".format(client_id).encode())
        client.send('Connected to server!'.encode())

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client_obj,))
        thread.start()


def get_active_users():
    return list(map(lambda x: x.client_id,clients))
def get_client_by_id(dest_id:str):
    for client in clients:
        if client.client_id == dest_id.strip():
            return client
    return None


def alive():

    # while alive interval (check last alive and compare with datetime.now())
    # if  last alive > alive_interval --> call remove_cleint

    return
# Starting Server

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((utils.host, utils.port))
server.listen()

# Lists For Clients and Their Nicknames
clients = []

# receive_thread = threading.Thread(target=receive)
# receive_thread.start()


alive_thread = threading.Thread(target=alive)
alive_thread.start()

print("Server is listening...")
receive()

