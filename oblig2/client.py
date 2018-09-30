import socket
from AES import *
from Crypto.PublicKey import RSA
import ast

class Client:
    def __init__(self, port):
        self.HOST = "localhost"
        self.PORT = port

    def create(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.HOST, self.PORT))
        req = "POST /server_message.txt HTTP/1.1\nHost: "+self.HOST+"\n\n"

        # print(req)
        private_key = RSA.generate(1024)
        public_key = private_key.publickey()

        #print(public_key.exportKey())

        req += public_key.exportKey().decode()



        self.socket.send(req.encode())

        #self.socket.sendall(req.encode())

        recv = self.socket.recv(1024)
        print(recv)

        key_message = ast.literal_eval(recv.decode())
        key_message = private_key.decrypt(key_message)

        #print(key_message)

        sym_key = key_message.decode().split("\n\n")[1]
        # print(recv.decode())
        print(sym_key.encode())
        # key = b"RfUjXn2r5u7x!A%D*G-KaPdSgVkYp3s6"
        self.enc = AES_Encryptor(sym_key.encode())

        req = "GET /server_message.txt HTTP/1.1\nHost: "+self.HOST+"\n\n"

        self.socket.send(req.encode())

        recv = self.socket.recv(1024)

        recv = self.enc.decrypt(recv, sym_key)
        recv = recv.decode()

        recv = recv.split("\n\n")
        #print(recv[1])
        data = recv[1].strip()




        with open("client_message.txt", "w") as f:
            f.write(data)
            f.close()

        #self.enc.decrypt_file("client_message.txt")
        self.socket.close()



if __name__ == "__main__":
    theClient = Client(8080)
    theClient.create()
    theClient.connect()