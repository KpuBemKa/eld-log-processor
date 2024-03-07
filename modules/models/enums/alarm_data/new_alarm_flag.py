class AlarmNewFlagEnum:
    def get(self, alarm: int) -> dict[int, str]:
        match alarm:
            case 0:
                return {0: "ending alert"}
            case 1:
                return {1: "new alert"}

        return {-1: "unknown"}
