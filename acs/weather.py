import random


class Weather:

    def __init__(self, heat, wetness):
        self.heat = heat
        self.wetness = wetness


class WeatherBand:

    def __init__(self, min_value, message):
        self.min_value = min_value
        self.message = message


class WeatherGenerator:

    wetness_deviation = 0.1
    wetness_min = 1 - 3 * wetness_deviation
    wetness_max = 1 + 3 * wetness_deviation

    heat_deviation = 0.1
    heat_min = 1 - 3 * heat_deviation
    heat_max = 1 + 3 * heat_deviation

    def generate(self):

        wetness = 0
        while (wetness < WeatherGenerator.wetness_min
                or wetness > WeatherGenerator.wetness_max):
            wetness = random.gauss(1, self.wetness_deviation)

        heat = 0
        while (heat < WeatherGenerator.heat_min
                or heat > WeatherGenerator.heat_max):
            heat = random.gauss(1, self.heat_deviation)

        return Weather(heat, wetness)
