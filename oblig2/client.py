import socket
from AES import *
from Crypto.PublicKey import RSA

class Client:
    def __init__(self, port):
        self.HOST = "localhost"
        self.PORT = port

    def create(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.socket.connect((self.HOST, self.PORT))
        req = "GET /server_message.txt HTTP/1.1\nHost: "+self.HOST+"\n\n"

        # print(req)
        RSA.generate(1028)

        self.socket.sendall(req.encode())

        recv = self.socket.recv(1024)

        # print(recv.decode())

        key = b"RfUjXn2r5u7x!A%D*G-KaPdSgVkYp3s6"
        self.enc = AES_Encryptor(key)

        recv = self.enc.decrypt(recv, key)
        recv = recv.decode()

        recv = recv.split("\n\n")
        print(recv[1])
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