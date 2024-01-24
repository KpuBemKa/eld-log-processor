import random


class Request2002:
    response = {}

    def make(self):
        self.response['cmd_seq'] = random.randint(0, 65535).to_bytes(4, 'little')
        self.response['query_count'] = int(1).to_bytes(2, 'little')
        self.response['tag_array'] = hex(0x2001)

        return self.response
