class DeviceNotFoundError(Exception):
    """ If device with the IP address is not found in DeviceHandler. """
    def __init(self, IP):
        self.ip = IP
    def __str__(self):
        return f"No Such Device Found: {self.ip}"