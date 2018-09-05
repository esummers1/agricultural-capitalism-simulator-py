class Farm:

    def __init__(self, owned_fields, initial_money):
        self.owned_fields = owned_fields
        self.money = initial_money
        self.current_year_expenditure = 0


class Field:

    def __init__(self,
                 id,
                 name,
                 description,
                 crop,
                 crop_quantity,
                 max_crop_quantity,
                 soil_quality,
                 price):

        self.id = id
        self.name = name
        self.description = description
        self.crop = crop
        self.crop_quantity = crop_quantity
        self.max_crop_quantity = max_crop_quantity
        self.soil_quality = soil_quality
        self.price = price

    def clear(self):
        self.crop = None
        self.crop_quantity = None

    def plant(self, crop, quantity):
        self.crop = crop
        self.crop_quantity = quantity

    def is_empty(self):
        return self.crop is None

    def report_status(self):

        """
        Print a summary of this field's properties and contents.
        """

        if self.crop is None:
            print(self.name, "-", self.description)
            print("Value:", self.price, " Size:", self.max_crop_quantity)
            print("Contents: None\n")
        else:
            print(self.name, "-", self.description)
            print("Value:", self.price, " Size:", self.max_crop_quantity)
            print("Contents:", self.crop.name, "(", self.crop_quantity, ")\n")

    def calculate_profit(self, weather):

        """
        Evaluate the distance between the crop's ideal weather and the
        actual weather, scale this depending on the crop's sensitivity
        to that weather, and calculate yield as a perfect score of 1
        minus deductions according to weather differences.
        """

        heat_delta = abs(weather.heat - self.crop.ideal_heat)
        wetness_delta = abs(weather.wetness - self.crop.ideal_wetness)

        heat_score = heat_delta * self.crop.heat_sensitivity
        wetness_score = wetness_delta * self.crop.wetness_sensitivity

        crop_yield = 1 - heat_score - wetness_score

        return int(
            crop_yield
            * self.crop_quantity
            * self.crop.sale_price
            * self.soil_quality)


class Crop:

    def __init__(self,
                 id,
                 name,
                 description,
                 cost,
                 sale_price,
                 ideal_heat,
                 ideal_wetness,
                 heat_sensitivity,
                 wetness_sensitivity):

        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.sale_price = sale_price
        self.ideal_heat = ideal_heat
        self.ideal_wetness = ideal_wetness
        self.heat_sensitivity = heat_sensitivity
        self.wetness_sensitivity = wetness_sensitivity

    def describe(self):
        print(self.name, "-", self.description)
        print("Cost:", self.cost, "  Sale price:", self.sale_price, "\n")
