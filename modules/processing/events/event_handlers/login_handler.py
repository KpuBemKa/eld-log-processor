from .base_handler import BaseHandler


class LoginHandler(BaseHandler):
    def handle(self, data) -> None:
        self._data = data

        if not self.__is_login_packet():
            return

        print(
            "Device '",
            self._data["payload"]["device_id"],
            "' has logged in",
        )

    def __is_login_packet(self) -> bool:
        return self._data["header"]["protocol_id"] == "1001"
