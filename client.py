import socket
import threading
import client_object as c
import utils
import time


closed = False
alive_interval = -1
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            message = client.recv(1024).decode()
            if not message:
                global closed
                closed = True
                break
            if message.startswith('@INIT'):
                connect_command= utils.compose_command(utils.DEST_SERVER,client_id,utils.KEYWORD_CONNECT)
                global alive_interval
                alive_interval  = int(message.split(',')[1])
                print("Alive interval is {}".format(alive_interval))
                client.send(connect_command.encode())
                
            

            else:
                print(message)
                continue
                
        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

# Sending Messages To Server
def write():
    while True and not closed:
    
        client_input = input(">> ")
        if client_input == '':
            continue
        command = parse_client_input(client_input)
        if command == utils.KEYWORD_QUIT:
            command = quit()
        if command == utils.KEYWORD_LIST:
            command = list()    
        if command == utils.KEYWORD_MESSAGE:
            command = message(client_input.split()[0],client_input.split(' ', 1)[1])
        
        if command == utils.INVALID_COMMAND:
            continue
    
        
        client.send(command.encode())

    exit()
        
def sleep_for(seconds : int):
    slept_seconds = 0
    while slept_seconds < seconds and not closed :
        time.sleep(1)
        slept_seconds += 1
    



def quit():
    return utils.compose_command(client_id,utils.DEST_SERVER,utils.KEYWORD_QUIT)
def list():
    return utils.compose_command(client_id,utils.DEST_SERVER,utils.KEYWORD_LIST)
def message(dest:str,client_message:str):
    return utils.compose_command(client_id,dest,client_message)

def alive():
    while True and not closed:
        if alive_interval > 0:
            sleep_for(alive_interval)
            if not closed:
                command = utils.compose_command(client_id,utils.DEST_SERVER,utils.KEYWORD_ALIVE)
                print("Sending alive")
                client.send(command.encode())

        

    return utils.compose_command(client_id,utils.DEST_SERVER,utils.KEYWORD_ALIVE)

def parse_client_input(client_input: str):
    words = client_input.split(" ")
    #print(words)
    if words[0].startswith("@") and len(words) == 1:
        command = words[0][1:].lower()
        if command in utils.client_input_commands:
            return command
    elif len(words) >=2 and len(words[0]) <=8 and len(client_input) <= 247: # 247 = 239 + 8
        return utils.KEYWORD_MESSAGE
    print("Invalid Command")
    return utils.INVALID_COMMAND
        

print("Chatbot (client app) cli started")
client_id = input('enter your client id (no more than 8 digits):\n')
while len(client_id) >8:
    client_id = input("incorrect client id, please re-enter\n")




# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((utils.host, utils.port))


# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

alive_thread = threading.Thread(target=alive)
alive_thread.start()










