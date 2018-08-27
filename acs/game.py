from acs.actions import *
from acs.data_reader import *
from acs.farm import *
from acs.weather import *


class Game:

    wetness_bands = [
        WeatherBand(-3.0, "with an arid climate."),
        WeatherBand(-2.5, "with minimal precipitation."),
        WeatherBand(-2.0, "with scattered drizzle."),
        WeatherBand(-1.5, "with scarce rainfall."),
        WeatherBand(-1.0, "with light showers."),
        WeatherBand(-0.5, "with moderate rainfall."),
        WeatherBand(0.5, "with considerable precipitation."),
        WeatherBand(1.0, "with heavy rainfall."),
        WeatherBand(1.5, "with some squalling."),
        WeatherBand(2.0, "with torrential downpours."),
        WeatherBand(2.5, "with monsoon storms."),
    ]

    heat_bands = [
        WeatherBand(-3.0, "This was a glacial year "),
        WeatherBand(-2.5, "This was a freezing year "),
        WeatherBand(-2.0, "This was a frigid year "),
        WeatherBand(-1.5, "This was a bracing year "),
        WeatherBand(-1.0, "This was a chilly year "),
        WeatherBand(-0.5, "This was a mild year "),
        WeatherBand(0.5, "This was a warm year "),
        WeatherBand(1.0, "This was a hot year "),
        WeatherBand(1.5, "This was a sultry year "),
        WeatherBand(2.0, "This was a sweltering year "),
        WeatherBand(2.5, "This was a scorching year "),
    ]

    def __init__(self, max_years, initial_money):
        data_reader = DataReader()
        self.available_crops = data_reader.import_crops()
        self.available_fields = data_reader.import_fields()

        owned_fields = []
        owned_fields.append(self.available_fields.pop(0))
        self.farm = Farm(owned_fields, initial_money)

        self.max_years = max_years
        self.current_year = 1
        self.score = 0
        self.exiting = False
        self.weather_generator = WeatherGenerator()


    def run(self):
        """Main game loop."""

        self.greet_player()

        while True:

            action = self.ask_for_input()
            action.execute()

            if self.exiting:
                break

            if action.should_end_round():
                self.run_logic()
                continue

    def greet_player(self):
        print("Welcome to Agricultural Capitalism Simulator! \n")
        print("You have", self.max_years, "years to make maximum profit. \n")

    def ask_for_input(self):

        actions = {
            1: StatusAction(self),
            2: ListCropsAction(self),
            3: PlayAction(self),
            4: ExitAction(self)
        }

        # List available actions
        for key, value in actions.items():
            action_choice_text = str(key) + ") " + value.get_prompt()
            print(action_choice_text)

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

        profit_this_year = 0
        weather = self.weather_generator.generate()

        for field in self.farm.owned_fields:
            if not field.is_empty():
                profit_this_year += field.calculate_profit(weather)

        print("Showing results!")

        for field in self.farm.owned_fields:
            field.clear()

    def exit(self):

        print("Exiting after results!")
        self.exiting = True
