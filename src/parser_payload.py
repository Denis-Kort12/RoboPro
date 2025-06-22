import socket
import struct
from dataclasses import dataclass
from typing import List

@dataclass
class Payload:
    timestamp: int
    theta: List[float]


class ParserPaylod:
    def __init__(self, NUM=6):
        self.NUM = NUM
        self.FORMAT = 'Q' + 'd' * NUM
        self.SIZE = struct.calcsize(self.FORMAT)

    def get_payloads(self, server_ip='127.0.0.1', port=8088, count_message=5):
        results = []

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(2.0)
            try:
                sock.sendto(b'get', (server_ip, port))

                for _ in range(count_message):
                    data, _ = sock.recvfrom(self.SIZE)
                    unpacked = struct.unpack(self.FORMAT, data)
                    timestamp = unpacked[0]
                    theta = list(unpacked[1:])
                    results.append(Payload(timestamp, theta))
            except socket.timeout:
                print("Timeout: no response from server")

        return results
