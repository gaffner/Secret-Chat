from abc import ABC, abstractmethod


class Interactor(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def start_interaction(self):
        pass
