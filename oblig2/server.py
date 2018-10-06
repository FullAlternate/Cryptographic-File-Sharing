import socketserver
from AES import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


class TCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """
        Handles the client requests
        """

        # Receives full request from client
        self.rData = self.request.recv(1024).decode("utf-8")
        print("Connected to {}".format(self.client_address))

        # Initializes symmetric key and AES encryptor for later use
        self.key = b"RfUjXn2r5u7x!A%D*G-KaPdSgVkYp3s6"
        self.enc = AES_Encryptor(self.key)

        # Extracts method and endpoint requested from client
        string_list = self.rData.split(" ")
        method = string_list[0]
        ep = string_list[1]

        # Reads end point and adds file signature if missing
        self.the_ep = ep.split("%")[0]
        self.the_ep = self.the_ep.lstrip("/")
        if self.the_ep.endswith(".txt") is False:
            self.the_ep += ".txt"

        # Handles methods
        if method == "POST":
            self.handle_post()

        if method == "GET":
            self.handle_get()

    def create_header(self):
        """
        Creates http header for the server response
        :return: Header(str)
        """
        try:
            if self.the_ep == "server_message.txt":
                file = open(self.the_ep, "r")
                self.data = file.read()
                file.close()

            header = 'HTTP/1.1 200 OK\n'

            header += "Content-Length: " + str(len(self.data)) + "\n\n"

        except Exception as FileNotFoundError:
            header = 'HTTP/1.1 404 Not Found\n'
            self.sData = '<html><body><center><h1>Error 404: File not found</h1></center></body></html>'

            header += "Content-Type: text/html\n"
            header += "Content-Length: " + str(len(self.sData)) + "\n\n"

        return header

    def handle_post(self):
        """
        Handles a post request from the client by storing their public key, then using this key the symmetric key is
        encrypted and sent as a response
        """
        body = self.rData.split("\n\n")[1]

        print("RECEIVED PUBLIC KEY:\n", body)
        pubKey = RSA.importKey(body.encode())

        response = self.create_header()
        check = response.split("\n")[0]

        # Creates a 404 file missing response and sends it to client if the file requested does not exists
        if check == "HTTP/1.1 404 Not Found":
            response += self.sData

            self.request.send(response.encode())
            print("\n\n404 - DONE\n\n")
            return

        key_response = response + self.key.decode()
        print("\n1ST MESSAGE:\n", key_response)

        RSA_encryptor = PKCS1_OAEP.new(pubKey)

        print("\n\nENCRYPTING...")
        key_response = RSA_encryptor.encrypt(key_response.encode())
        print("\nENCRYPTED RESULT:\n", key_response)

        self.request.send(str(key_response).encode())

    def handle_get(self):
        """
        Handles a get request by encrypting the requested file data using AES and sending it as a response to client
        """
        response = self.create_header()
        msg_response = response + self.data
        print("2ND MESSAGE:\n", msg_response)

        print("\n\nENCRYPTING...")
        msg_response = self.enc.encrypt(msg_response.encode(), self.key)
        print("\nENCRYPTED RESULT:\n", msg_response)

        self.request.send(msg_response)
        print("\n\nDONE\n\n")


if __name__ == "__main__":

    HOST = "localhost"
    PORT = 8080

    server = socketserver.TCPServer((HOST, PORT), TCPHandler)

    server.serve_forever()
    server.allow_reuse_address(True)

    server.shutdown()
    server.server_close()
