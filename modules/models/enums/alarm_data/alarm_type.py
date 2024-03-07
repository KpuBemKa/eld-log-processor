class AlarmTypeEnum:
    types = {
        0x01: "Speeding",
        0x02: "Low voltage",
        0x03: "High engine coolant Temperature",
        0x04: "Hard acceleration",
        0x05: "Hard deceleration",
        0x06: "Idle engine",
        0x07: "Towing",
        0x08: "High RPM",
        0x09: "Power on",
        0x0A: "Exhaust Emission",
        0x0B: "Quick Lane change",
        0x0C: "Sharp turn",
        0x0D: "Fatigue driving",
        0x0E: "Power off",
        0x0F: "Geo-fence",
        0x10: "Emergency",
        0x11: "Crash",
        0x12: "Tamper",
        0x13: "Illegal enter",
        0x14: "Illegal ignition",
        0x15: "pull out",
        0x16: "Ignition on",
        0x17: "Ignition off",
        0x18: "MIL alarm",
        0x19: "Unlock alarm",
        0x1A: "No card presented",
        0x1B: "Dangerous driving",
        0x1C: "Vibration",
        0x1D: "Door opened",
        0x1E: "Door closed",
        0x20: "1 High temperature alarm",
        0x21: "1 Low temperature alarm",
        0x22: "2 High temperature alarm",
        0x23: "2 Low temperature alarm",
        0x24: "3 High temperature alarm",
        0x25: "3 Low temperature alarm",
        0x26: "1 High temperature alarm",
        0x27: "1 Low temperature alarm",
        0x28: "GPS antenna alarm",
    }

    def get(self, key) -> dict[int, str]:
        value = self.types[key]

        if value is None:
            return {key: "unknown"}

        return {key: value}
