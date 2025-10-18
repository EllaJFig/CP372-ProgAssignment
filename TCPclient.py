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

    #send message to server
    message = input("Enter message to send: ")
    client_socket.send(message.encode())

    #receive reply
    data = client_socket.recv(1024).decode()
    print(f"Received from server: {data}")

    client_socket.close() #close

if __name__ == '__main__':
    start_client()
