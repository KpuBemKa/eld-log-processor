from .event_handlers.base_handler import BaseHandler
from .event_handlers.login_handler import LoginHandler
from .event_handlers.logout_handler import LogoutHandler


class EventsProcessor:
    _event_handlers: list[BaseHandler] = []
    # _data = None

    def __init__(self):
        self._event_handlers.extend([LoginHandler(), LogoutHandler()])

    def process(self, data):
        for handler in self._event_handlers:
            handler.handle(data)
