from abc import ABC, abstractmethod
from acs.data_reader import *
from acs.game import *


class Launcher(ABC):

    MAX_YEARS = 20
    INITIAL_MONEY = 500

    def __init__(self):
        self.data_reader = DataReader()
        self.crops = self.data_reader.import_crops()
        self.fields = self.data_reader.import_fields()

    @staticmethod
    @abstractmethod
    def execute():
        pass


class AILauncher(Launcher):

    def __init__(self):
        pass

    @staticmethod
    def execute():
        # TODO instantiate evolver and run
        pass


class PlayerLauncher(Launcher):

    def __init__(self):
        super().__init__()

    @staticmethod
    def execute():
        input_provider = PlayerInputProvider()
        game = Game(Launcher.MAX_YEARS, Launcher.INITIAL_MONEY, input_provider)
        game.run()
