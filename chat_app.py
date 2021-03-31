import socket
import threading
import sys

class ChatApplication:
    def __init__(self, sys_type, ip=None):
        self.__type__ = sys_type
        self.__ip__ = ip
        self.threads = []
        # Stores the dictionary of devices connected 
        # format - device_ip:device_socket
        self.devices = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if self.__type__ == "server":
            self.socket.bind(('0.0.0.0', 8081))
            print("$ CHAT APPLICATION SERVER $")
            t1 = threading.Thread(target=self.listen_and_accept)
            t1.start()
            self.threads.append(t1)
            self.start_chat_server()
        elif self.__type__ == "client":
            if self.__ip__ != None:
                self.socket.connect((ip, 8081))
                self.start_client()
            else:
                print("[-] Please enter IP address of the server to connect")
        else:
            print(f"[-] Invalid Application type {self.__type__}")

    def listen_and_accept(self):
        """ Listens and accept any new connection.
            Sends the intro to newly joind members. """
        intro = " $ WELCOME TO CHAT APPLICATION $" 
        while True:
            self.socket.listen()
            conn_sock, address = self.socket.accept()
            ip_addr = address[0]
            self.devices[ip_addr] = conn_sock
            print(f"[+] {ip_addr} joined the chat")

            intro_data = intro.encode()
            conn_sock.send(intro_data)

    def start_client(self):
        prompt = ">> "
        while True:
            msg = input(prompt)
            # If line break is not present then append it to msg
            term_pos = msg.find("\n")
            if term_pos < 0:
                msg += "\n"
            data = msg.encode()
            self.socket.send(data)

            if msg == "quit":
                for t in self.threads:
                    t.exit()
                sys.exit()

    def start_chat_server(self):
        while True:
            for address in self.devices:
                sock = self.devices[address]
                for msg in self.get_text(sock):
                    if msg == "quit":
                        print(f"{address} left the chat")
                        del self.devices[address]
                        break
                    elif msg == "sudo close server":
                        sys.exit()
                    else:
                        print(f"{address}: ", msg)

    def send_text_global(self, text):
        for address in self.devices:
            self.devices[address].send(text)

    def send_text(self, sending_socket, text):
        sending_socket.send(text)

    def get_text(self, recv_sock):
        buffer = ""
        is_open = True
        while is_open:
            data = recv_sock.recv(1024)
            if not data:
                is_open = False
            else:
                msg = data.decode()
                buffer += msg
                term_pos = msg.find("\n")
                while term_pos > -1:
                    msg = buffer[:term_pos]
                    yield msg
                    # Remove the msg from buffer
                    buffer = buffer[term_pos+1:]
                    term_pos = msg.find("\n")

if __name__ == "__main__":
    app = None
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            app = ChatApplication(sys.argv[1], sys.argv[2])
        else:
            app = ChatApplication(sys.argv[1])
    else:
        print("[-] Please include all the arguments")
        print("python chat_app server - For creating a server")
        print("python chat_app client {server_ip} - For launching a client instance to connect to a server")

        


