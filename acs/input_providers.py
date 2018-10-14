from acs.weather import WeatherGenerator
from acs.actions import *


class InputProvider(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def decide_action(self, game, numbered_actions):
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
    def decide_field_to_buy(self, numbered_fields):
        pass

    @abstractmethod
    def show_greeting(self, max_years):
        pass

    @abstractmethod
    def list_available_crops_with_details(self, available_crops):
        pass

    @abstractmethod
    def report_status(self):
        pass

    @abstractmethod
    def report_field_performance(self, owned_fields):
        pass

    @staticmethod
    @abstractmethod
    def show_year_results_header():
        pass

    @staticmethod
    @abstractmethod
    def report_weather(weather, heat_bands, wetness_bands):
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


class AIInputProvider(InputProvider):
    """
    Class representing the decision engine for a specific strategy instance of
    the AI.
    """

    def __init__(self, strategy):
        super().__init__()
        self.strategy = strategy

    def decide_action(self, game, numbered_actions):
        """
        Decide what to do, in this order:
         - Buy field, if strategy says sufficient funds are available
         - Plant crops, if there are available fields and funds
         - Advance to harvest, if there is nothing else to do
        """

        # Buy fields
        for action in numbered_actions:
            if type(action) == BuyFieldsAction:
                for field in game.available_fields:
                    if field.price < (game.farm.money
                                      / self.strategy.field_ratio):
                        return action

        # Plant crops
        for action in numbered_actions:
            if type(action) == PlantCropsAction:
                return action

        # Advance to harvest
        for action in numbered_actions:
            if type(action) == PlayAction:
                return action

    def decide_field_to_plant(self, numbered_fields):
        """
        Choose the first available field for planting.
        """

        return numbered_fields[0]

    def decide_crop_to_plant(self, numbered_crops):
        pass

    def decide_crop_quantity(self, maximum):
        """
        Decide to plant the maximum possible number of crops.
        """

        return maximum

    def decide_field_to_buy(self, numbered_fields):
        """
        Choose the first available field for purchase.
        """

        return numbered_fields[0]

    def show_greeting(self, max_years):
        pass

    def list_available_crops_with_details(self, available_crops):
        pass

    def report_status(self):
        pass

    def report_field_performance(self, owned_fields):
        pass

    @staticmethod
    def show_year_results_header():
        pass

    @staticmethod
    def report_weather(weather, heat_bands, wetness_bands):
        pass

    @staticmethod
    def report_financials(income, expenditure, new_assets):
        pass

    @staticmethod
    def show_loss_message():
        pass

    @staticmethod
    def show_final_score(score):
        pass


class PlayerInputProvider(InputProvider):

    def decide_action(self, game, numbered_actions):

        # List available actions
        PlayerInputProvider.list_action_options(numbered_actions)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_actions)

    def decide_field_to_plant(self, numbered_fields):

        # List available fields
        print("\nWhich field would you like to plant in? Enter 0 to cancel.")
        PlayerInputProvider.list_numbered_items(numbered_fields)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_fields)

    def decide_crop_to_plant(self, numbered_crops):

        # List available crops
        print("\nWhich crop would you like to plant? Enter 0 to cancel.")
        PlayerInputProvider.list_numbered_items(numbered_crops)

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_crops)

    def decide_crop_quantity(self, maximum):

        # Advise of available range
        print("How many would you like to plant? "
              "( 1 - ", maximum, "| to cancel.)")

        # Prompt for choice
        return PlayerInputProvider.choose_quantity(maximum)

    def decide_field_to_buy(self, numbered_fields):

        # List available fields
        print("\nWhich field would you like to purchase? Enter 0 to cancel.")
        for key, field in numbered_fields.items():
            first_line = (str(key) + ") " + field.name + " - " +
                               field.description)
            print()
            print(first_line)
            print("Price:", field.price)

        print()

        # Prompt for choice
        return PlayerInputProvider.choose_from_numbered_list(numbered_fields)

    def show_greeting(self, max_years):
        print("\n\nWelcome to Agricultural Capitalism Simulator! \n")
        print("You have", max_years, "years to make maximum profit.")

    def list_available_crops_with_details(self, available_crops):
        print("\nAvailable crops for planting:\n")
        for crop in available_crops:
            crop.describe()

    def report_status(self, game):
        print("\nYear:", game.current_year)
        print("Balance:", game.farm.money)
        print("Asset Value:", game.calculate_assets())
        print("\nFields:\n")

        for field in game.farm.owned_fields:
            field.report_status()

    def report_field_performance(self, owned_fields):
        print()
        for field in owned_fields:
            field.report_performance()

    @staticmethod
    def show_year_results_header():
        print("\n====== RESULTS ======")

    @staticmethod
    def report_weather(weather, heat_bands, wetness_bands):

        heat_message = PlayerInputProvider.find_weather_band(
            weather.heat,
            heat_bands,
            WeatherGenerator.heat_deviation
        )
        wetness_message = PlayerInputProvider.find_weather_band(
            weather.wetness,
            wetness_bands,
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
        correct band in a given list of WeatherBands to describe this result,
        and return its message field.
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
        """
        Prompt player to enter a number between 0 and the length of the supplied
        dictionary, and continue prompting until such an input is given. Return
        the number selected, or None if the selection is 0.
        """

        while True:
            selection = int(input())

            if selection in numbered_list.keys():
                return numbered_list[selection]
            if selection == 0:
                return None

    @staticmethod

    def choose_quantity(maximum):
        """
        Prompt player to enter a number between 0 and the maximum, and continue
        prompting until such an input is given. Return the number selected, or
        None if the selection is 0.
        """

        while True:
            selection = int(input())

            if 0 < selection <= maximum:
                return selection
            if selection == 0:
                return None
