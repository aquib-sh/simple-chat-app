import sys
import threading
import config
from server import ChatServer
from client import ChatClient

if __name__ == "__main__":
    app = None
    if len(sys.argv) > 1:
        if len(sys.argv) == 3:
            app = ChatClient(sys.argv[2], config.default_port)
            app.start_client()
        else:
            app = ChatServer(config.default_ip, config.default_port)
            t1 = threading.Thread(target=app.listen_and_accept)
            t1.start()
            app.display_messages()

    else:
        print("[-] Please include all the arguments")
        print("python chat_app server - For creating a server")
        print("python chat_app client {server_ip} - For launching a client instance to connect to a server")