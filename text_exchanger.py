class Messenger:
    """
    TextExchanger Class
    Responsible for sending and returning the received text. 
    
    """

    def send_text_global(self, devices, text):
        """ Send text globally to all the devices in dictionary. 
            Param: 1> devices: type=dict format=ip_address:connection_socket
                   2> text: (text to send)
        """
        for address in devices:
            devices[address].send(text)

    def send_text(self, sending_socket, text):
        """ Send a text from sending socket. 
            Param: 1> sending_socket: (socket which will be used to send the text)
                   2> text: (text to send)
        """
        sending_socket.send(text)

    def get_text(self, recv_sock):
        """ Returns the received text from receiving socket. 
            Param: 1> recv_sock: (socket which will be used to receive from)
            Return: text string
        """
        recv_sock.settimeout(0.5)
        buffer = ""
        is_open = True
        while is_open:
            try:
                data = recv_sock.recv(1024)
            except:
                is_open = False
                continue

            if not data or data == b'\n':
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


    def get_text_single(self, recv_sock):
        data = recv_sock.recv(1024)
        msg = data.decode()
        return msg