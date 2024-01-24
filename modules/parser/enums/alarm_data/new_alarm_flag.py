class AlarmNewFlagEnum:

    def get(self, alarm):
        match alarm:
            case 0:
                return {0: 'ending alert'}
            case 1:
                return {1: 'new alert'}