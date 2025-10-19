"""
CP372 Programming Assignment
TCP Server Implementation 
-----------------------------
Ella Figueiredo     169061130
Noah Samarita       169030051

"""

import socket
import threading
from datetime import datetime


MAX_CLIENTS = 3
FILE_PATH = None
clients = {} #create client cache; should have address, start time, and end time be recorded
client_count = 0

'''
This function will handle the individual connections
'''
def client_handling(client_socket, addr, client_name):
    global client_count
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"{client_name} connected")

    if client_name not in clients:
        clients[client_name] = {"info": [] } #add client to cache

    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clients[client_name]["info"].append({"address": {addr}, "connected_at": {start_time}, "disconnected_at": {None}})

    while True:
        data = client_socket.recv(1024).decode() #receive (up to 1024 bytes)

        #receive data from client
        ''' loop through and check the following;
            if "exit" --> record end time, send goodbye message back to client, break
            if "status" --> send the content in the client cache through the client socket
            if "list" --> check if folder for files exists; if no it creates one
                        -->if files exist within that folder; list the names
                        --> if not; say no files available
                    --> send file list to client
            if file is requested --> send requested file to client
            else --> send data ACK back to client 
        '''
        if data.lower() == "exit":
            print(f"{client_name} disconnected")
            clients[client_name]["info"].append({"address": addr, "connected_at": start_time, "disconnected_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            client_count -=1
            break

        elif data.lower() == "status":
            status = []
            for name, info in clients.items():
                status.append(f"{name}: {info}")

            status_str = "\n".join(status)
            client_socket.send(status_str.encode())

        else:
            print(f"Received: {data}")
            client_socket.send(f"{data} ACK".encode())


    client_socket.close() 


'''
This function is to handle new connection and distribute them to where they need to go
'''
def start_server():
    global client_count
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    
    server_socket.listen(3) #listen; instead of 1 set as MAX_CLIENTS
    print(f"Server is listening on {socket.gethostbyname(socket.gethostname())}") #add address

    while True:

        client_socket, addr = server_socket.accept() #accept; gives the information about the connection

        client_count += 1
        if client_count > 3:
            client_socket.send("full".encode())
            client_count -=1
            client_socket.close()
            continue
        else:
            client_name = f"Client{client_count}"
            client_socket.send(f"You are {client_name}".encode())
    

            thread = threading.Thread(target=client_handling, args=(client_socket,addr,client_name))
            thread.start()

            print(f"Connection from {addr}") #update this line to say "Client(num) connected from {addr}??"
            

if __name__ == '__main__':
    start_server()


