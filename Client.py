import socket
import threading

from Server_Client.Config import Config


class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.username = input("Welcome To 'Chat'...\r\n\tEnter your username: ")
        self.run = True
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected()

    def connect(self):
        """
        Binding host to port
        :return: None
        """
        try:
            self.socket.connect((self.host, self.port))
        except Exception as e:
            raise Exception(f"An Error as occured.\r\n\t{e}")

    def connected(self):
        """
        Main connection handler function
        :return: None
        """
        self.connect()

        while self.run:
            thread = threading.Thread(target=self.recv_messages)
            thread.start()
            users_data = input(f"{self.username}: ")
            if users_data == Config.QUIT_MESSAGE:
                print("Logged off...")
                self.socket.close()
                self.run = False
                break
            try:
                sent_message = f'{self.username} {users_data}'
                self.socket.send(sent_message.encode(Config.STRING_FORMAT))
            except ConnectionRefusedError as e:
                raise e

    def recv_messages(self):
        message = self.socket.recv(Config.BUFFER)
        message = message.decode('utf-8')
        print('\r\n' + message)


a = Client(Config.HOST, Config.PORT)
