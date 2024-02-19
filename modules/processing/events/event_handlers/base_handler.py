# from __future__ import annotations
from abc import ABC, abstractmethod


class BaseHandler(ABC):
    @abstractmethod
    def handle(self, data: dict) -> None:
        pass
