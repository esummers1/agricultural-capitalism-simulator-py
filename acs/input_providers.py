from abc import ABC, abstractmethod


class InputProvider(ABC):

    def __init__(self, game):
        self.game = game

    @abstractmethod
    def decide_action(self, numbered_actions):
        pass

    @abstractmethod
    def decide_field_to_plant(self, numbered_fields):
        pass

    @abstractmethod
    def decide_crop_to_plant(self, numbered_crops):
        pass

    @abstractmethod
    def decide_crop_quantity(self, maximum):
        pass

    @abstractmethod
    def show_greeting(self):
        pass


class PlayerInputProvider(InputProvider):

    def decide_action(self, numbered_actions):

        # List available actions
        PlayerInputProvider.list_ordered_options(numbered_actions)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_actions)

    def decide_field_to_plant(self, numbered_fields):

        # List available fields
        print("Which field would you like to plant in?\n")
        PlayerInputProvider.list_ordered_options(numbered_fields)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_fields)

    def decide_crop_to_plant(self, numbered_crops):

        # List available crops
        print("Which crop would you like to plant?")
        PlayerInputProvider.list_ordered_options(numbered_crops)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_crops)

    def decide_crop_quantity(self, maximum):

        # Advise of maximum quantity
        print("How many would you like to plant? (1 - ",
              str(maximum),
              ")")

        # Prompt for choice
        return PlayerInputProvider.choose_quantity(maximum)

    def show_greeting(self):
        print("Welcome to Agricultural Capitalism Simulator! \n")
        print("You have", self.game.max_years,
              "years to make maximum profit. \n")

    @staticmethod
    def list_ordered_options(numbered_options):
        for key, value in numbered_options.items():
            print(str(key) + ") " + value.get_prompt())

    @staticmethod
    def choose_from_numbered_list(numbered_list):
        while True:
            selection = int(input())

            if selection in numbered_list.keys():
                return numbered_list[selection]

    @staticmethod
    def choose_quantity(maximum):
        while True:
            selection = int(input())

            if 0 < selection <= maximum:
                return selection
