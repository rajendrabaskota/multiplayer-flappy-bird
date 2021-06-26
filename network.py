import socket
import pickle


class Network:
    def __init__(self):
        self.server = socket.gethostbyname(socket.gethostname())
        self.port = 5555
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, bird_width, pipe_width, pipe_height):
        self.client.connect((self.server, self.port))
        send_data = str(bird_width) + ' ' + str(pipe_width) + ' ' + str(pipe_height)
        self.client.send(str.encode(send_data))
        val = self.client.recv(8)
        return int(val.decode())

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048 * 100)
            reply = pickle.loads(reply)
            print(reply)
            return reply
        except socket.error as e:
            print(e)
