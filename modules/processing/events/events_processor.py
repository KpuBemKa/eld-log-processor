from .event_handlers.base_handler import BaseHandler
from .event_handlers.driver_assignment_handler import DriverAssignmentHandler
from .event_handlers.duty_status_handler import DutyStatusHandler
from .event_handlers.powerup_handler import PowerupHandler

from modules.models.packet.packet import PacketModel
# from ..storage.gps_handler import GpsHandler
# from .event_handlers.driving_handler import DrivingHandler
# from .event_handlers.driver_logout_handler import DriverLogoutHandler


class EventsProcessor:
    _event_handlers: list[BaseHandler] = []
    # _data = None

    def __init__(self):
        self._event_handlers.extend([PowerupHandler(), DriverAssignmentHandler(), DutyStatusHandler()])

    def process(self, data: PacketModel):
        for handler in self._event_handlers:
            handler.handle(data)
