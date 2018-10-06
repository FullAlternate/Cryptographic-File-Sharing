import socket
from AES import *
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import ast


class Client:
    def __init__(self, port):
        self.HOST = "localhost"
        self.PORT = port

        # Initializes private and public key
        self.private_key = RSA.generate(1024)
        self.public_key = self.private_key.publickey()

    def handle(self, a_socket):
        """
        Prepares requests for server and handles server responses
        :param a_socket: Socket obj
        """
        # Prompts the user to enter a file name then connects to server
        self.a_file = input("Enter file name: ")
        a_socket.connect((self.HOST, self.PORT))

        key_message = self.post_request(a_socket)

        # Reopens new socket for next request
        a_socket.close()
        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        a_socket.connect((self.HOST, self.PORT))

        # Decrypts encrypted server response using the client private key
        RSA_decryptor = PKCS1_OAEP.new(self.private_key)
        key_message = RSA_decryptor.decrypt(key_message)

        # Extracts symmetric key and initializes AES encryptor with it
        self.sym_key = key_message.decode().split("\n\n")[1]
        self.enc = AES_Encryptor(self.sym_key.encode())

        self.get_request(a_socket)

        a_socket.close()

    def post_request(self, a_socket):
        """
        Generates a post request containing the generated public key. Also receives response decoding it and returning
        it to its original state
        :param a_socket: Socket obj
        :return: Encrypted data(tuple)
        """
        req = "POST /" + self.a_file + " HTTP/1.1\nHost: " + self.HOST + "\n\n"

        req += self.public_key.exportKey().decode()
        a_socket.send(req.encode())

        recv = a_socket.recv(1024)
        check = recv.decode().split("\n")[0]

        # If the response received contains error msg 404, informs the user and terminates client program
        if check == 'HTTP/1.1 404 Not Found':
            print("No file by that name, exiting program")
            a_socket.close()
            exit()

        return ast.literal_eval(recv.decode())

    def get_request(self, a_socket):
        """
        Generates a get request and receives response from server. Using the previously acquired AES key
        the encrypted file information is decrypted and written to a client file
        :param a_socket:
        """
        req = "GET /" + self.a_file + " HTTP/1.1\nHost: " + self.HOST + "\n\n"

        a_socket.send(req.encode())

        recv = a_socket.recv(1024)

        recv = self.enc.decrypt(recv, self.sym_key.encode())
        recv = recv.decode()

        recv = recv.split("\n\n")
        data = recv[1].strip()

        with open("client_message.txt", "w") as f:
            f.write(data)
            f.close()


if __name__ == "__main__":
    theClient = Client(8080)

    the_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    theClient.handle(the_socket)
