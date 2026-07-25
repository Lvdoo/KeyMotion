import socket

class UdpComms:
    def __init__(self, ip="127.0.0.1", port=8000):
        """
        Simple UDP sender for KeyMotion (Python → Unity)
        """

        self.ip = ip
        self.port = port

        # socket UDP
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self, message: str):
        """
        Send a simple string message to Unity
        Example: "DO2"
        """

        if not isinstance(message, str):
            message = str(message)

        self.sock.sendto(
            message.encode("utf-8"),
            (self.ip, self.port)
        )

    def close(self):
        """
        Close UDP socket cleanly
        """
        self.sock.close()