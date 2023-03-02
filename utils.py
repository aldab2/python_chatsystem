host = "localhost"
port = 8082


ALIVE_INTERVAL= 30
KEYWORD_CONNECT = 'connect'
KEYWORD_QUIT = 'quit'
KEYWORD_ALIVE = 'alive'
KEYWORD_LIST = 'list'
KEYWORD_MESSAGE = 'message'



INVALID_KEYWORD = 'invalid keyword'
INVALID_COMMAND = 'invalid command'

DEST_SERVER = "server"


reserverd_words = [KEYWORD_CONNECT,KEYWORD_QUIT,KEYWORD_ALIVE,KEYWORD_LIST,DEST_SERVER,KEYWORD_MESSAGE]
total_commands = [KEYWORD_CONNECT,KEYWORD_QUIT,KEYWORD_ALIVE,KEYWORD_LIST]
client_input_commands = [KEYWORD_QUIT,KEYWORD_LIST]

def get_command_type(commmand:str):
    if len(commmand) != 255: 
        return INVALID_COMMAND
    
    message = commmand[16:].strip().replace(" ","")
    if message in total_commands:
        return message # will be one of the elemtes in the commands array
    return KEYWORD_MESSAGE

    

    

    




def compose_command(src:str,dest:str,message:str):
    if len(src) > 8 or len(dest) > 8 or len(message) > 240:
        return INVALID_COMMAND


    return "{:8s}{:8s}{:239s}".format(dest,src,message)
 



def parse_command(command:str):

    command_type = get_command_type(command)
    #print(command_type)
    if command_type ==  False:
        return INVALID_COMMAND
    dest = command[0:8]
    src= command[8:16]
    message = command[16:]

    return (dest,src,message,command_type)



    


