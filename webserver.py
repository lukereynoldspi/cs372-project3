import socket
import sys
import os

# Map for file extensions, we only need to worry about .txt and .html for this project
file_extensions = {'.txt':'text/plain', '.html':'text/html'}

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

# Parses header of response, returns data when \r\n\r\n is found
def parse_data(data):
    while True:
        d = data.recv(4096)
        decoded_data =""
        decoded_data = decoded_data + d.decode("ISO-8859-1")
        if decoded_data.find("\r\n\r\n"):
            return decoded_data

# Accepts new connections, listens and decodes data
def server_connection():
    while True:
        new_conn = s.accept()
        new_socket = new_conn[0]  # This is what we'll recv/send on
        header_data = parse_data(new_socket) # Calls data parser
        get = header_data.split("\r\n")
        get_parts = get[0].split()

        # Splits data into the method, path, and protocol. We only need the path
        request_method = get_parts[0]
        request_path = get_parts[1]
        request_protocol = get_parts[2]

        # Gets both the file name and extension
        path_file = os.path.split(request_path)[1]
        path_extension = os.path.splitext(path_file)[1]

        print("Your path file is " + path_file)
        
        # Tries to open file path, will return a 404 error if something goes wrong
        try:
            with open(path_file) as fp:
                data = fp.read()   # Read entire file
                data = data.encode("ISO-8859-1")
                bytes = len(data_bytes)

                get = ("HTTP/1.1 200 OK\r\nContent-Type: {}\r\nContent-Length: {}\r\n\r\n{}").format(file_extensions[path_extension], bytes, data)
                new_socket.sendall(get.encode("ISO-8859-1"))
                print("Success! Your file is displayed.")
        except:
            get = ("HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\nConnection: close\r\n\r\n404 not found")
            new_socket.sendall(get.encode("ISO-8859-1"))
            print("Failure, file could not be found.")

        new_socket.close()

if __name__ == '__main__':
    server_connection()