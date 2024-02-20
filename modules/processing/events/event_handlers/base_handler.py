# from __future__ import annotations
from abc import ABC, abstractmethod

from modules.models.packet.packet import PacketModel


class BaseHandler(ABC):
    @abstractmethod
    def handle(self, data: PacketModel) -> None:
        pass
