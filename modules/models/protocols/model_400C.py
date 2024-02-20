class Protocol400CModel:
    stat_data = None
    card_id = None

    def set(self, param, value):
        setattr(self, param, value)
