import socketserver
from AES import *
from Crypto.PublicKey import RSA


class TCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.rData = self.rfile.readline().strip().decode("utf-8")
        print("Connected to {}".format(self.client_address))

        key = b"RfUjXn2r5u7x!A%D*G-KaPdSgVkYp3s6"
        self.enc = AES_Encryptor(key)

        self.string_list = self.rData.split(" ")
        self.method = self.string_list[0]
        self.ep = self.string_list[1]

        print(self.rData)

        #print(self.method)

        self.the_ep = self.ep.split("%")[0]
        self.the_ep = self.the_ep.lstrip("/")

        response = self.create_header()

        response += str(self.data)

        #print(response)

        response = self.enc.encrypt(response.encode(), key)

        self.request.send(response)

    def create_header(self):
        """
        Creates http header for the server response
        :return: Header(str)
        """
        try:
            if self.the_ep == "server_message.txt":
                self.file = open(self.the_ep, "r")
                self.data = self.file.read()
                self.file.close()

            header = 'HTTP/1.1 200 OK\n'

           # header += "Content-Disposistion: attachment; filename=" + self.the_ep + "\n"
            header += "Content-Length: " + str(len(self.data)) + "\n\n"

        except Exception as FileNotFoundError:
            header = 'HTTP/1.1 404 Not Found\n'
            self.sData = '<html><body><center><h1>Error 404: File not found</h1></center></body></html>'.encode(
                'utf-8')

            header += "Content-Type: text/html\n"
            header += "Content-Length: " + str(len(self.sData)) + "\n\n"

        return header
class Server:
    def __init__(self, port):
        self.HOST = "localhost"
        self.PORT = port
        self.server = None

    def create(self):
        """
        Initializes server
        """
        self.server = socketserver.TCPServer((self.HOST, self.PORT), TCPHandler)

    def start(self):
        """
        Continually listens for requests
        """
        self.server.serve_forever()

    def stop(self):
        """
        Stops listening for requests and closes server
        """
        self.server.shutdown()
        self.server.server_close()


if __name__ == "__main__":

    theServer = Server(8080)
    theServer.create()

    theServer.start()
    theServer.server.allow_reuse_address(True)
    theServer.stop()
