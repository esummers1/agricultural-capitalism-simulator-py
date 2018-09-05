from acs.actions import *
from acs.data_reader import *
from acs.farm import *
from acs.input_providers import *
from acs.weather import *
import math


class Game:

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

    def __init__(self, max_years, initial_money):
        data_reader = DataReader()
        self.available_crops = data_reader.import_crops()
        self.available_fields = data_reader.import_fields()

        owned_fields = []
        owned_fields.append(self.available_fields.pop(0))
        self.farm = Farm(owned_fields, initial_money)

        self.max_years = max_years
        self.current_year = 1
        self.exiting = False
        self.weather_generator = WeatherGenerator()
        self.lowest_crop_cost = self.get_lowest_crop_cost()
        self.input_provider = PlayerInputProvider(self)

    def get_lowest_crop_cost(self):

        lowest_cost = 10000

        for crop in self.available_crops:
            if crop.cost < lowest_cost:
                lowest_cost = crop.cost

        return lowest_cost

    def run(self):

        """
        Main game loop.
        """

        self.input_provider.show_greeting()

        while True:

            action = self.decide_action()
            action.execute()

            if self.exiting:
                break

            if action.should_end_round():
                self.advance_year()

            if self.current_year == self.max_years:
                break

        score = self.calculate_final_score()
        self.input_provider.show_final_score(score)

        return score

    def decide_action(self):
        actions = self.build_actions()
        return self.input_provider.decide_action(actions)

    def build_actions(self):

        """
        Create a numbered dictionary of Actions based on the current situation.
        """

        actions = [
            StatusAction(self),
            ListCropsAction(self)
        ]

        if self.is_empty_field_available() and not self.is_player_bankrupt():
            actions.append(PlantCropsAction(self))

        actions.append(PlayAction(self))
        actions.append(ExitAction(self))

        return self.make_numbered_dictionary(actions)

    def is_empty_field_available(self):

        for field in self.farm.owned_fields:
            if field.is_empty():
                return True

        return False

    def report_status(self):
        self.input_provider.report_status(self)

    def list_crops(self):
        self.input_provider.list_available_crops_with_details()

    def plant_crops(self):

        """
        Prompt player to select an empty field, a crop, and a quantity to plant.
        Store these crops in the appropriate field and register the transaction.
        """

        # Decide field for planting
        empty_fields = [field for field in self.farm.owned_fields
                        if field.is_empty()]
        numbered_empty_fields = Game.make_numbered_dictionary(empty_fields)

        selected_field = self.input_provider.decide_field_to_plant(
            numbered_empty_fields)

        # Decide crop for planting
        affordable_crops = [crop for crop in self.available_crops
                            if crop.cost < self.farm.money]
        numbered_crops = Game.make_numbered_dictionary(affordable_crops)
        selected_crop = self.input_provider.decide_crop_to_plant(numbered_crops)

        # Calculate maximum that can be planted here
        affordable_quantity = math.floor(self.farm.money / selected_crop.cost)
        maximum_crop_quantity = min(affordable_quantity,
                                    selected_field.max_crop_quantity)

        # Decide quantity to plant
        quantity_to_plant = self.input_provider.decide_crop_quantity(
            maximum_crop_quantity)

        # Plant this field
        selected_field.crop = selected_crop
        selected_field.crop_quantity = quantity_to_plant

        # Record transaction
        total_crop_cost = selected_crop.cost * quantity_to_plant
        self.farm.money -= total_crop_cost
        self.farm.current_year_expenditure += total_crop_cost

    @staticmethod
    def make_numbered_dictionary(ordered_list):

        new_dict = {}

        for counter, value in enumerate(ordered_list, 1):
            new_dict[counter] = value

        return new_dict

    def advance_year(self):

        # Compute results
        weather = self.weather_generator.generate()
        income = self.calculate_income(weather)
        profit = income - self.farm.current_year_expenditure

        # Report to player
        self.input_provider.show_year_results_header()
        self.input_provider.report_weather(weather)
        self.input_provider.report_profit(profit)

        # Register results in game state
        self.current_year += 1
        self.farm.money += income

        # Clear fields
        for field in self.farm.owned_fields:
            field.clear()

        # TODO check for bankruptcy - do this in main game loop?
        if self.is_player_bankrupt():
            self.input_provider.show_loss_message()

    def calculate_income(self, weather):
        profit_this_year = 0
        for field in self.farm.owned_fields:
            if not field.is_empty():
                profit_this_year += field.calculate_profit(weather)
        return profit_this_year

    def calculate_assets(self):
        assets = 0
        for field in self.farm.owned_fields:
            assets += field.price
        return assets

    def is_player_bankrupt(self):
        return self.farm.money < self.lowest_crop_cost

    def calculate_final_score(self):
        return self.farm.money + self.calculate_assets()

    def exit(self):
        self.exiting = True
