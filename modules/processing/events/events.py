from .event_handlers.base_handler import BaseHandler
from .event_handlers.driver_handler import DriverAssignmentHandler
from .event_handlers.driving_handler import DrivingHandler
# from .event_handlers.driver_logout_handler import DriverLogoutHandler


class EventsProcessor:
    _event_handlers: list[BaseHandler] = []
    # _data = None

    def __init__(self):
        self._event_handlers.extend([DriverAssignmentHandler(), DrivingHandler()])

    def process(self, data):
        for handler in self._event_handlers:
            handler.handle(data)
