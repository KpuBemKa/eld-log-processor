class StatDataReservedEnum:
    engine_diagnose_protocol = {
        1: "VPW (passage car)",
        2: "PWM (passage car)",
        3: "CAN11 (passage car)",
        4: "CAN29 (passage car)",
        5: "KWP2000 (passage car)",
        6: "KWP2000M (passage car)",
        7: "ISO9141 (passage car)",
        11: "J939(commercial vehicle)",  # 0A
        12: "J1708(commercial vehicle)",  # 0B
        160: "SINOTRUK CAN29 (heavy duty)",  # A0
        161: "volvoCAN29 (commercial vehicle)",  # A1
        0: "unknown or tracker mode the values should be cleared on system reset",
    }

    network_frequency = {
        0: "No Service",
        1: "CDMA BC0",
        2: "CDMA BC1",
        3: "CDMA BC2",
        4: "CDMA BC3",
        5: "CDMA BC4",
        6: "CDMA BC5",
        7: "CDMA BC6",
        8: "CDMA BC7",
        9: "CDMA BC8",
        10: "CDMA BC9",
        11: "CDMA BC10",
        12: "CDMA BC11",
        13: "CDMA BC12",
        14: "CDMA BC13",
        15: "CDMA BC14",
        16: "CDMA BC15",
        17: "CDMA BC16",
        18: "CDMA BC17",
        19: "CDMA BC18",
        20: "CDMA BC19",
        21: "GSM 450",
        22: "GSM 480",
        23: "GSM 480",
        24: "GSM 850",
        25: "GSM 900",
        26: "GSM 1800",
        27: "GSM 1900",
        28: "WCDMA 2100",
        29: "WCDMA 1900",
        30: "WCDMA 1800",
        31: "WCDMA 1700 US",
        32: "WCDMA 850",
    }

    def make_response(self, item: dict[int, str], key: int) -> str:
        if item.get(key):
            return item[key]
        return str(key)

    def get_engine_diagnose_protocol(self, index: int) -> str:
        return self.make_response(self.engine_diagnose_protocol, index)

    def get_network_frequency(self, index: int) -> str:
        return self.make_response(self.network_frequency, index)
