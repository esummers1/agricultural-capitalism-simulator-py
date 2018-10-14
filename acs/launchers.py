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

    @abstractmethod
    def execute(self):
        pass


class AILauncher(Launcher):

    def __init__(self):
        pass

    def execute(self):
        # TODO instantiate evolver and run
        pass


class PlayerLauncher(Launcher):

    def __init__(self):
        super().__init__()

    def execute(self):
        input_provider = PlayerInputProvider()
        game = Game(
            Launcher.MAX_YEARS,
            Launcher.INITIAL_MONEY,
            input_provider,
            self.crops,
            self.fields)
        game.run()
