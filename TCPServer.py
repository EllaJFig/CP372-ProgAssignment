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
import os

MAX_CLIENTS = 3
FILE_REPO = "file_repo"
clients = {} #creates client cache; should have address, start time, and end time be recorded
client_count = 0

'''
This function will handle the individual connections
'''

def client_handling(client_socket, addr, client_name):
    global client_count

    print(f"{client_name} connected.")
    
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if client_name not in clients:
        clients[client_name] = {"info": [] } #add client to cache
    
    clients[client_name]["info"].append({
        "address": {addr}, 
        "connected_at": {start_time}, 
        "disconnected_at": {None}})
    
    recent_input = None # to keep track of what what the user wants to interact with

    while True:
        data = client_socket.recv(1024).decode()#receive (up to 1024 bytes)

        if not data:
            print(f"{client_name} disconnected.") #this is for disconnecting unexpectedly
            client_count -= 1
            break

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

        #EXIT HANDLING
        if data.lower() == "exit":
            print(f"{client_name} disconnected.")
            clients[client_name]["info"].append({
                "address": addr, 
                "connected_at": start_time, 
                "disconnected_at": 
                datetime.now().strftime('%Y-%m-%d %H:%M:%S')})
            client_socket.send("Disconnected.".encode())
            client_count -=1
            break

        #LIST HANDLING
        elif data.lower() == "list":
            if not os.path.exists(FILE_REPO):
                os.makedirs(FILE_REPO)

            server_files = os.listdir(FILE_REPO)
          
            if len(server_files) == 0:
                client_socket.send("Server File Directory is Empty.".encode())

            else:
                file_list = "\n".join(i for i in server_files)
                format_list = f" \n{file_list}\nReply with the file name + '.txt' to view contents."
                client_socket.send(format_list.encode())

            recent_input = "list"
            
        #STATUS HANDLING
        elif data.lower() == "status":
            status = []
            for name, info in clients.items():
                status.append(f"{name}: {info}")

            status_str = "\n".join(status)
            format_status = f" \n{status_str}"
            client_socket.send(format_status.encode())

            recent_input = "status"

        #FILES HANDLING
        elif data.lower() not in ["list", "status", "exit"]:
            file_path = os.path.join(FILE_REPO, data)

            if os.path.exists(file_path):
                with open(file_path, "r") as x:
                    content = x.read()

                data_content = f"\n'{data}' content:\n\n{content}"
                client_socket.send(data_content.encode())
                
                recent_input = None

            else:
                if recent_input == "list":
                    client_socket.send("- File Invalid, Try Again.".encode())

                else: 
                    client_socket.send(f"{data} ACK".encode())
        
        #GENERAL HANDLING
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
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    server_socket.listen(MAX_CLIENTS) #listen; instead of 1 set as MAX_CLIENTS
   
    print(f"Server is listening on {socket.gethostbyname(socket.gethostname())}") #add address

    while True:
        
        client_socket, addr = server_socket.accept() #accept; gives the information about the connection
        
        if client_count >= MAX_CLIENTS:
            client_socket.send("Server is full. It has reached the limit of 3 clients.".encode())
            client_socket.close()
            continue

        else:
            client_count += 1
            client_name = f"Client{client_count:02}"
            client_socket.send(f"You are {client_name}".encode())
    
        thread = threading.Thread(target=client_handling, args=(client_socket,addr,client_name))
        thread.start()

        print(f"Connection from {addr}") #update this line to say "Client(num) connected from {addr}??"

if __name__ == '__main__':
    start_server()