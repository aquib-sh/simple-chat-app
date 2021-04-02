import socket
import config
from device_handler import DeviceHandler
from text_exchanger import Messenger

class ChatServer:
    """ 
    ChatServer Class
    Starts the server for chat application.
    """

    def __init__(self, IP, PORT):
        """ Param: 1> IP: (IP address of the machine)
                   2> PORT: (Port to bind the server socket on)
        """
        print(config.server_intro)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((IP, PORT))
        self.devices = DeviceHandler()
        self.exchanger = Messenger()
        self.accepting_new_connections = True

    def listen_and_accept(self):
        """ Listens and accept any new connection.
            Sends the intro to newly joind members. """
        while self.accepting_new_connections:
            self.socket.listen()
            try:
                conn_sock, address = self.socket.accept()
            except OSError:
                break
            ip_addr = address[0]
            self.devices.add_device(ip_addr, conn_sock)
            print(f"\n[+] {ip_addr} joined the chat\n")
            intro_data = config.client_intro.encode()
            conn_sock.send(intro_data)

    def display_messages(self):
        """ Constantly checks if new messages have arrived.
            if arrived then display them on screen.
        """
        server_running = True
        while server_running:
            devices = self.devices.get_device_IPs()
            for address in devices:
                devices = self.devices.get_device_IPs()
                sock = self.devices.get_device_socket(address)
                for msg in self.exchanger.get_text(sock):
                    if msg == "quit":
                        print(f"\n{address} left the chat\n")
                        self.devices.remove_device(address)
                        break
                    elif msg == "sudo server shutdown":
                        print("** Performing Server Shutdown **")
                        server_running = False
                        self.accepting_new_connections = False
                        self.socket.close()
                        return
                    else:
                        print(f"{address}: ", msg)
