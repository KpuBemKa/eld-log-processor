""" Decoder base class """

from abc import ABC, abstractmethod


class Decoder(ABC):
    """Decoder base class"""

    data: bytes
    model = None
    part = None
    position: int = 0

    def move(self, pos):
        self.position += pos
        return self.position

    @abstractmethod
    def decode(self) -> "Decoder":
        pass

    def get_model(self) -> dict:
        return self.model.__dict__

    def set_part(self, part):
        self.part = part
        return self

    def reverse_bytes(self):
        self.part = "".join(reversed([self.part[i : i + 2] for i in range(0, len(self.part), 2)]))
        return self

    def hex_int(self, base=16):
        try:
            self.part = int(self.part, base)
        except (ValueError, TypeError) as ex:
            print("ValueError exception handled: ", ex, ex.args)

        return self

    def to_hex(self):
        self.part = self.part.hex()
        return self

    def get_part(self):
        part = self.part
        self.part = None
        return part

    def to_bin(self, base=8):
        self.part = bin(self.part)[2:].zfill(base)
        return self
