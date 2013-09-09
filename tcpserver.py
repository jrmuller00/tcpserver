import socket
import threading
import socketserver

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        if data == "zimbra":
            serverResponse = 'You are asking about zimbra'
            response = bytes("{}: {}".format(cur_thread.name, serverResponse), 'ascii')
        elif data == "openvpn":
            serverResponse = 'You are asking about openvpn'
            response = bytes("{}: {}".format(cur_thread.name, serverResponse), 'ascii')
        else:
            serverResponse = 'I do not know what you are asking about'
            response = bytes("{}: {}".format(cur_thread.name, serverResponse), 'ascii')
        #response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
    finally:
        sock.close()

if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    server_thread.daemon = True
    server_thread.start()
    print("Server loop running in thread:", server_thread.name)

    client(ip, port, "zimbra")
    client(ip, port, "openvpn")
    client(ip, port, "maccor")

    server.shutdown()