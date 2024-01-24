class ProtocolA002Model:
    cmd_seq = None
    resp_count = None
    resp_index = None
    fail_count = None
    fail_tag_array = []
    success_count = None
    success_tlv_array = []

    class TLV_Model:
        tag = None
        length = None
        value_array = None

    def set(self, param, value):
        setattr(self, param, value)

    def new_tlv_data(self):
        return self.TLV_Model()

    def add_fail_tlv_data(self, item):
        self.fail_tag_array.append(item)

    def add_success_tlv_data(self, item):
        self.success_tlv_array.append(item)
