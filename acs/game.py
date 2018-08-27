from acs.farm import *
from acs.actions import *
from acs.data_reader import *


class Game:

    def __init__(self):
        data_reader = DataReader()
        self.available_crops = data_reader.import_crops()
        self.available_fields = data_reader.import_fields()

        first_field = self.available_fields.pop(0)

        self.farm = Farm(first_field)
        self.exiting = False


    def run(self):

        while True:

            action = self.ask_for_input()
            action.execute()

            if self.exiting:
                break

            if action.should_end_round():
                self.run_logic()
                continue

    def ask_for_input(self):

        actions = {
            1: StatusAction(self),
            2: ListCropsAction(self),
            3: PlayAction(self),
            4: ExitAction(self)
        }

        # List available actions
        for key, value in actions.items():
            print(key, ") ", value.get_prompt())

        while True:

            # Ask for choice
            selection = int(input())

            if selection in actions.keys():
                return actions[selection]

    def report_status(self):
        print("Showing status!")

    def list_crops(self):
        print("Listing crops!")

    def run_logic(self):

        """Calculate the outcome of the year's growth, and inform the player.
        TODO: Can split into two functions later"""

        print("Calculating yields!")
        print("Showing results!")

    def exit(self):

        print("Exiting after results!")
        self.exiting = True
