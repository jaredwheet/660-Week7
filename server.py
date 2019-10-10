import socket
import sys
from certificateAuthority import getKey, validateAuthenticity, getPublicKey

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 9500              # Arbitrary non-privileged port
validated = False
keySent = False
key = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind Failed')
    sys.exit()

print("Socket binded to %s" % (PORT))

s.listen(10)

print('Socket is listening')

while 1:
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            stringData = data.decode('utf-8')
            print('Server Received: ', stringData)

            if validated == False:
                print('Server Translated: ', getKey(stringData, False))
                response = validateAuthenticity(stringData)
                if response == "client.py":
                    print('Authenticated: ', response)
                    print('Server Sending: ssl certificate')
                    conn.send(getKey("I am a cert", True).encode('utf-8'))
                    validated = True
                else:
                    print('Error: Unknown server certificate received!')
                    print('Sending Goodbye and closing connection')
                    conn.send("Goodbye".encode('utf-8'))
            elif keySent == False:
                key = getKey(stringData, False, getPublicKey())
                print('Server Received: Private session key, ', key)
                print('Server Sending: Key acknowledgement')
                conn.sendall(getKey('Server has received session key', True, key).encode('utf-8'))
                keySent = True
            else:
                print('Server Translated: ', getKey(stringData, False, key))
                print("Server Sending: This is some response data")
                conn.sendall(getKey('This is some response data', True).encode('utf-8'))
                keySent = False
                validated = False

s.close()