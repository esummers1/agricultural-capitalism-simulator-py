from abc import ABC, abstractmethod
from game import Game
from weather import WeatherGenerator


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

    @abstractmethod
    def list_available_crops_with_details(self):
        pass

    @abstractmethod
    def report_status(self):
        pass

    @abstractmethod
    def report_field_performance(self):
        pass

    @staticmethod
    @abstractmethod
    def show_year_results_header():
        pass

    @staticmethod
    @abstractmethod
    def report_weather(weather):
        pass

    @staticmethod
    @abstractmethod
    def report_financials(income, expenditure, new_assets):
        pass

    @staticmethod
    @abstractmethod
    def show_loss_message():
        pass

    @staticmethod
    @abstractmethod
    def show_final_score(score):
        pass


class PlayerInputProvider(InputProvider):

    def decide_action(self, numbered_actions):

        # List available actions
        PlayerInputProvider.list_action_options(numbered_actions)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_actions)

    def decide_field_to_plant(self, numbered_fields):

        # List available fields
        print("\nWhich field would you like to plant in?")
        PlayerInputProvider.list_numbered_items(numbered_fields)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_fields)

    def decide_crop_to_plant(self, numbered_crops):

        # List available crops
        print("\nWhich crop would you like to plant?")
        PlayerInputProvider.list_numbered_items(numbered_crops)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_crops)

    def decide_crop_quantity(self, maximum):

        # Advise of maximum quantity
        print("How many would you like to plant? ( 1 - ", maximum, ")")

        # Prompt for choice
        return PlayerInputProvider.choose_quantity(maximum)

    def show_greeting(self):
        print("Welcome to Agricultural Capitalism Simulator! \n")
        print("You have", self.game.max_years, "years to make maximum profit.")

    def list_available_crops_with_details(self):
        print("\nAvailable crops for planting:\n")
        for crop in self.game.available_crops:
            crop.describe()

    def report_status(self, game):
        print("\nYear:", game.current_year)
        print("Balance:", game.farm.money)
        print("Asset Value:", game.calculate_assets())
        print("\nFields:\n")

        for field in game.farm.owned_fields:
            field.report_status()

    def report_field_performance(self):
        print()
        for field in self.game.farm.owned_fields:
            field.report_performance()

    @staticmethod
    def show_year_results_header():
        print("\n====== RESULTS ======")

    @staticmethod
    def report_weather(weather):

        heat_message = PlayerInputProvider.find_weather_band(
            weather.heat,
            Game.heat_bands,
            WeatherGenerator.heat_deviation
        )
        wetness_message = PlayerInputProvider.find_weather_band(
            weather.wetness,
            Game.wetness_bands,
            WeatherGenerator.wetness_deviation
        )
        print(heat_message, wetness_message, "\n")

    @staticmethod
    def report_financials(income, expenditure, new_assets):
        print("Asset acquisitions:", new_assets)
        print("Revenue:", income)
        print("Expenses:", expenditure)

        profit = income + new_assets - expenditure

        if profit < 0:
            print("Commiserations... you made a loss of", profit)
        else:
            print("Congratulations! You made a profit of", profit)

    @staticmethod
    def show_loss_message():
        print("\nYou are bankrupt. You will have to find a job.")

    @staticmethod
    def show_final_score(score):
        print("\nWell played, capitalist - the rich get richer.")
        print("Final total assets:", score)

    @staticmethod
    def find_weather_band(weather_component, weather_bands, deviation):

        """
        Given a component of some Weather and the deviation factor used when
        calculating said Weather component's value in this game, find the
        correct band in a given list of WeatherBands to describe this result.
        """

        number_of_sd_from_mean = (weather_component - 1) / deviation

        for band in reversed(weather_bands):
            if number_of_sd_from_mean >= (band.min_value):
                return band.message

    @staticmethod
    def list_action_options(action_options):
        print()
        for key, value in action_options.items():
            string_to_print = (str(key) + ") " + value.get_prompt())
            print(string_to_print)

    @staticmethod
    def list_numbered_items(numbered_items):
        for key, value in numbered_items.items():
            string_to_print = (str(key) + ") " + value.name)
            print(string_to_print)

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
