class DTCAttrEnum:

    attrs = {
        0: 'Data Valid But Above Normal Operational Range - Most Severe Level',
        1: 'Data Valid But Below Normal Operational Range - Most Severe Level',
        2: 'Data Erratic, Intermittent Or Incorrect',
        3: 'Voltage Above Normal, Or Shorted To High Source',
        4: 'Voltage Below Normal, Or Shorted To Low Source',
        5: 'Current Below Normal Or Open Circuit',
        6: 'Current Above Normal Or Grounded Circuit',
        7: 'Mechanical System Not Responding Or Out Of Adjustment',
        8: 'Abnormal Frequency Or Pulse Width Or Period',
        9: 'Abnormal Update Rate',
        10: 'Abnormal Rate Of Change',
        11: 'Root Cause Not Known',
        12: 'Bad Intelligent Device Or Component',
        13: 'Out Of Calibration',
        14: 'Special Instructions',
        15: 'Data Valid But Above Normal Operating Range - Least Severe Level',
        16: 'Data Valid But Above Normal Operating Range - Moderately Severe Level',
        17: 'Data Valid But Below Normal Operating Range - Least Severe Level',
        18: 'Data Valid But Below Normal Operating Range - Moderately Severe Level',
        19: 'Received Network Data In Error',
        20: 'Data Drifted High',
        21: 'Data Drifted Low',
        31: 'Condition Exists'
    }

    def get(self, key):
        if self.attrs[key] is None:
            return {key: 'Reserved For SAE Assignment'}

        return {key: self.attrs[key]}