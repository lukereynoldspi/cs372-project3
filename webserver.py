import socket
import sys

# Checks for arguments, uses port 28333 as a default
if len(sys.argv) >= 2:
    port = int(sys.argv[1])
else:
    print("No host or port specified, port 28333")
    port = 28333 # Default port

# Binds socket to port, socket listens
s = socket.socket()
s.bind(('', port))
s.listen()

# Accepts new connections, listens and decodes data
while True:
    new_conn = s.accept()
    new_socket = new_conn[0]  # This is what we'll recv/send on
    while True:
        d = new_socket.recv(4096)
        if "\r\n\r\n" in d.decode("ISO-8859-1"):
            break
    get = ("HTTP/1.1 \r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!")
    new_socket.sendall(get.encode("ISO-8859-1"))
    new_socket.close()
