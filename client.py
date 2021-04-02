import sys
import socket
import config

class ChatClient:
    """ 
    ChatClient Class
    Starts the client for chat application.
    """

    def __init__(self, IP, PORT):
        """ Param: 1> IP: (IP address of the machine)
                   2> PORT: (Port to bind the server socket on)
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"[+] Connecting to chat server on {IP} on {PORT}")
        self.socket.connect((IP, PORT))
        print("[+] Connected !")
        data = self.socket.recv(1024)
        intro_msg = data.decode()
        print(intro_msg)

    def start_client(self):
        is_running = True
        while is_running:
            try:
                msg = input(config.client_prompt)
            except ConnectionAbortedError:
                break
            # If line break is not present then append it to msg
            term_pos = msg.find("\n")
            if term_pos < 0:
                msg += "\n"
            data = msg.encode()
            self.socket.send(data)
            if msg == "quit\n" or msg == "sudo server shutdown\n":
                is_running = False
            

                