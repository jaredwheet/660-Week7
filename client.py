# Import socket module 
import socket     
import random 
from certificateAuthority import getKey, validateAuthenticity, getPublicKey

  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 9500 
key = random.randint(0,9)              
  
# connect to the server on local computer 
# s.connect(('127.0.0.1', port)) 
  
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('127.0.0.1', port))
    s.sendall(getKey('Hello World', True).encode('utf-8'))
    data = s.recv(1024)
    stringData = data.decode('utf-8')
    print('Client Received Certificate: ', stringData)

    response = validateAuthenticity(stringData)
    if response == 'server.py':
        print('Authenticated: ', response)
    else:
        print('Error: Unknown server certificate received!')
    
    s.sendall(getKey(str(key), True, getPublicKey()).encode('utf-8'))
    print('Sending: Private Session Key')
    data = s.recv(1024)
    print('Received: ', getKey(data.decode('utf-8'), False, key))

    print('Sending: This is some random data')
    s.sendall(getKey('This is some random data', True, key).encode('utf-8'))

    data = s.recv(1024)
    stringData = data.decode('utf-8')
    print('Received: ', getKey(stringData, False, key))