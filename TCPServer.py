"""
CP372 Programming Assignment
TCP Server Implementation 
-----------------------------
Ella Figueiredo     169061130
Noah Samarita       169030051

"""

import socket

''' set;
MAX_CLIENTS = 3
FILE_PATH = 

clients = {}
client_count = 0
'''


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    server_socket.bind(('localhost', 12345))  # Bind to localhost on port 12345
    
    server_socket.listen(3) #listen; instead of 1 set as MAX_CLIENTS
    print("Server is listening...") #add address

    #create a client count

    while True:

        client_socket, addr = server_socket.accept() #accept 
        
        #update client count; check if max_client reached; close socket if full
        
        #set client name 
        print(f"Connection from {addr}") #update this line to say "Client(num) connected from {addr}??"

        data = client_socket.recv(1024).decode() #receive (up to 1024 bytes)


        #create client cache; should have address, start time, and end time be recorded


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


        ''' This was the example on how to send a reponse back to the client'''
        if data:
            print(f"Received: {data}")

            #send response back to client
            upcased_data = data.upper()
            client_socket.send(upcased_data.encode())



        #close and update cache
        client_socket.close() 

if __name__ == '__main__':
    start_server()


