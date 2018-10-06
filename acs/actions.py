from abc import ABC, abstractmethod


class Action(ABC):

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_prompt(self):
        pass

    @abstractmethod
    def should_end_round(self):
        return False


class PlayAction(Action):

    def execute(self):
        # Do nothing, as this will advance to harvest.
        pass

    def get_prompt(self):
        return "Advance to harvest time"

    def should_end_round(self):
        return True


class StatusAction(Action):

    def execute(self):
        self.game.report_status()

    def get_prompt(self):
        return "Review farm status"

    def should_end_round(self):
        return False


class ListCropsAction(Action):

    def execute(self):
        self.game.list_crops()

    def get_prompt(self):
        return "See a list of available crops"

    def should_end_round(self):
        return False


class PlantCropsAction(Action):

    def execute(self):
        self.game.plant_crops()

    def get_prompt(self):
        return "Buy and plant crops"

    def should_end_round(self):
        return False


class BuyFieldsAction(Action):

    def execute(self):
        self.game.buy_fields()

    def get_prompt(self):
        return "Buy fields"

    def should_end_round(self):
        return False


class ExitAction(Action):

    def execute(self):
        self.game.exit()

    def get_prompt(self):
        return "Retire from the farming business"

    def should_end_round(self):
        return True
