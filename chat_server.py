import socket
import select
Header_length=10
port=1234
host='192.168.1.15'

server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)

server_socket.bind((host,port))
server_socket.listen()

socket_list=[server_socket]#list of all clients,server is already placed
clients={}#client socket info will be the key and user data like usernaem will be the value.


def recieve_message(client_socket):
    try:
        message_header=client_socket.recv(Header_length)

        if not len(message_header):
            return False
        message_length = int(message_header.decode('utf-8'))
        return {'header':message_header,'data':client_socket.recv(message_length)}
    
        
    except:
        return False

while True:  
    
    read_sockets,_,exception_sockets = select.select(socket_list,[],socket_list)
    for notified_socket in read_sockets:
        if notified_socket == server_socket:#this means a client just connected to the server so we need to accept the connection and work on it.
            client_socket,client_address=server_socket.accept()
            print('Connection Accepted')
            user=recieve_message(client_socket)
            if user is False:
                continue
            socket_list.append(client_socket)

            clients[client_socket]=user
            print('Accepted new connection from %r %r username: %r'%(client_address[0],client_address[1],user['data'].decode('utf-8')))
        else:
            message=recieve_message(notified_socket)

            if message is False:
                socket_list.remove(notified_socket)
                del clients[notified_socket]
                continue
            user=clients[notified_socket]
            print('Recieved message from %r %r'%(user['data'].decode('utf-8'),message['data'].decode('utf-8')))
            for client_socket in clients:
                if client_socket!=notified_socket:
                    client_socket.send(user['header']+user['data']+message['header']+message['data'])
                                    



















               
