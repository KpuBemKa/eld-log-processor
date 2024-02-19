class TlvType:
    types = {
        b"\x10\x01": "Speeding",
        "02": "Low voltage",
        "03": "High engine coolant Temperature",
        "04": "Hard acceleration",
        "05": "Hard deceleration",
        "06": "Idle engine",
        "07": "Towing",
        "08": "High RPM",
        "09": "Power on",
        "0a": "Exhaust Emission",
        "0b": "Quick Lane change",
        "0c": "Sharp turn",
        "0d": "Fatigue driving",
        "0e": "Power off",
        "0f": "Geo-fence",
        "10": "Emergency",
        "11": "Crash",
        "12": "Tamper",
        "13": "Illegal enter",
        "14": "Illegal ignition",
        "15": "pull out",
        "16": "Ignition on",
        "17": "Ignition off",
        "18": "MIL alarm",
        "19": "Unlock alarm",
        "1a": "No card presented",
        "1b": "Dangerous driving",
        "1c": "Vibration",
        "1d": "Door opened",
        "1e": "Door closed",
        "20": "1 High temperature alarm",
        "21": "1 Low temperature alarm",
        "22": "2 High temperature alarm",
        "23": "2 Low temperature alarm",
        "24": "3 High temperature alarm",
        "25": "3 Low temperature alarm",
        "26": "1 High temperature alarm",
        "27": "1 Low temperature alarm",
        "28": "GPS antenna alarm",
    }

    def get(self, key):
        if self.types[key] is None:
            return key

        return {key: self.types[key]}
