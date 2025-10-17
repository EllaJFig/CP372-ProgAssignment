"""
CP372 Programming Assignment
TCP Client Implementation 
-----------------------------
Ella Figueiredo     169061130
Noah Samarita       169030051

"""

import socket

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #create socket
    client_socket.connect(('localhost', 12345))  # Connect to the server

    #loop the next part because the server and client need to keep exchanging messages; break loop if client's message is "exit"
    while True:

        #send message to server
        message = input("Enter message to send: ")
        client_socket.send(message.encode())

        if message.lower() == "exit":
            response = client_socket.recv(1024).decode #get response
            print("Server: {response}") #print outcome
            break
        
        #receive reply
        data = client_socket.recv(1024).decode()
        print(f"Server: {data}")


    
    client_socket.close() #close

if __name__ == '__main__':
    start_client()
