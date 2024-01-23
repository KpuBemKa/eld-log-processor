class StatDataReservedEnum:

    engine_diagnose_protocol = {
        '01': 'VPW (passage car)',
        '02': 'PWM (passage car)',
        '03': 'CAN11 (passage car)',
        '04': 'CAN29 (passage car)',
        '05': 'KWP2000 (passage car)',
        '06': 'KWP2000M (passage car)',
        '07': 'ISO9141 (passage car)',
        '0a': 'J939(commercial vehicle)',
        '0b': 'J1708(commercial vehicle)',
        'a0': 'SINOTRUK CAN29 (heavy duty)',
        'a1': 'volvoCAN29 (commercial vehicle)',
        '00': 'unknown or tracker mode the values should be cleared on system reset'
    }

    network_frequency = {
        '00': 'No Service',
        '01': 'CDMA BC0',
        '02': 'CDMA BC1',
        '03': 'CDMA BC2',
        '04': 'CDMA BC3',
        '05': 'CDMA BC4',
        '06': 'CDMA BC5',
        '07': 'CDMA BC6',
        '08': 'CDMA BC7',
        '09': 'CDMA BC8',
        '10': 'CDMA BC9',
        '11': 'CDMA BC10',
        '12': 'CDMA BC11',
        '13': 'CDMA BC12',
        '14': 'CDMA BC13',
        '15': 'CDMA BC14',
        '16': 'CDMA BC15',
        '17': 'CDMA BC16',
        '18': 'CDMA BC17',
        '19': 'CDMA BC18',
        '20': 'CDMA BC19',
        '21': 'GSM 450',
        '22': 'GSM 480',
        '23': 'GSM 480',
        '24': 'GSM 850',
        '25': 'GSM 900',
        '26': 'GSM 1800',
        '27': 'GSM 1900',
        '28': 'WCDMA 2100',
        '29': 'WCDMA 1900',
        '30': 'WCDMA 1800',
        '31': 'WCDMA 1700 US',
        '32': 'WCDMA 850',
    }

    def make_response(self, item, key):
        if item.get(key):
            return item[key]
        return key

    def get_engine_diagnose_protocol(self, data):
        return self.make_response(self.engine_diagnose_protocol, data)

    def get_network_frequency(self, data):
        return self.make_response(self.network_frequency, data)