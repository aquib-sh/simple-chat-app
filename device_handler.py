from errors import DeviceNotFoundError

class DeviceHandler:
    """ 
    DeviceHandler Class
    Handles the devices that are connected to server.
    """

    def __init__(self):
        self.devices = {}

    def add_device(self, IP, socket):
        """ Param: 1> IP: (IP address of the device) type=string
                   2> socket: (connection socket of device to server) type=socket
        """
        self.devices[IP] = socket

    def remove_device(self, IP):
        """ Param: 1> IP: (IP address of the device) type=string. """
        del self.devices[IP]

    def get_device_socket(self, IP):
        """ Param: 1> IP: (IP address of the device) type=string. """
        #print(f"Looking for {IP}")
        if IP in self.devices:
            #print(f"Returning {self.devices[IP]}")
            return self.devices[IP]
        else:
            raise DeviceNotFoundError(IP)
    
    def get_device_IPs(self):
        """ Returns a list of IP Addresses of all the devices connected. """
        ips = self.devices.keys()
        return list(ips)
    