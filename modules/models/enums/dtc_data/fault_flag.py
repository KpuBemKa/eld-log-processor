class DTCFaultFlagEnum:
    def get(self, fault) -> dict[int, str]:
        match fault:
            case 0:
                return {0: "Stored"}

            case 1:
                return {1: "Pending"}

            case _:
                return {1: "Pending"}
