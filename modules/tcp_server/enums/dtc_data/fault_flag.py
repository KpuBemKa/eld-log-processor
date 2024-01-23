class DTCFaultFlagEnum:

    def get(self, fault):
        match fault:
            case 0:
                return {0: 'Stored'}
            case 1:
                return {1: 'Pending'}