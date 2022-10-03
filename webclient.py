import socket
import sys

# Checks for arguments, uses example.com as a default
if len(sys.argv) >= 2:
    host = str(sys.argv[1])
    if len(sys.argv) >= 3:
        port = int(sys.argv[2])
    else:
        port = 80
else:
    print("No host or port specified, using default values")
    host = "example.com"
    port = 80

# Connects socket
s = socket.socket()
s.connect((host, port))

# Sends request, encodes it
get = ("GET / HTTP/1.1\r\nHost: {}\r\nConnection: close\r\n\r\n").format(host)
s.sendall(get.encode("ISO-8859-1"))
d = s.recv(4096)
while d:
    print(d.decode("ISO-8859-1"))
    d = s.recv(4096)
if len(d) == 0:
    s.close()
