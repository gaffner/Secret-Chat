from abc import ABC, abstractmethod
from Chat.Chat import Chat


class Interactor(ABC):
    def __init__(self, chat: Chat):
        self._chat: Chat = chat

    @abstractmethod
    def send_message(self, text: str):
        pass

    @abstractmethod
    def receive_message(self) -> str:
        pass

    @abstractmethod
    def interaction_loop(self):
        pass
