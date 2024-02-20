from modules.models.packet.packet import PacketModel
# from .redis.redis_realtime import RedisRealtime

# from .socketio.socketio_realtime import SoketioRealtime
# from modules.processing.persist.persistence import Persistence
from modules.processing.remote.remote import Remote

from .events.events_processor import EventsProcessor
from .storage.gps_handler import GpsHandler


class Processing:
    _events_processor = EventsProcessor()
    _data: PacketModel

    def __init__(self):
        pass

    def process(self, data: PacketModel):
        self._data = data

        self.storage_data()
        self.events_data()
        self.persist_data()
        # self.realtime_data()
        # self.persist_data()

    def realtime_data(self):
        # RedisRealtime().process(self.data)
        pass

    def storage_data(self):
        GpsHandler().handle(self._data)

    def persist_data(self):
        if self._data.header.protocol_id == "4001" or self._data.header.protocol_id == "4009":
            Remote().construct_from_packet(packet=self._data, event_type=2, event_code=1).send()

    def additional_check(self, data):
        self._data = data

        return self.vin_check()

    def vin_check(self):
        if self._data.header.device_id is None:
            return False

        return True

    def events_data(self):
        self._events_processor.process(self._data)
