class Farm:

    def __init__(self, owned_fields):
        self.owned_fields = owned_fields
        self.funds = 0


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

    def print(self):
        print(self.name, ": ", self.description)
        print("Cost: ", self.cost, ". Sale price: ", self.sale_price)