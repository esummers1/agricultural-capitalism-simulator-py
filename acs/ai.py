from functools import total_ordering


@total_ordering
class CropChance:
    """
    Class representing a single pairing of a Crop to a probability of planting
    this Crop.
    """

    def __init__(self, crop, chance):
        self.crop = crop
        self.chance = chance

    def describe(self):
        """
        Return the name of the Crop and the chance, expressed as a percentage.
        """

        return str(self.crop.name) + ": " + str(self.chance * 100) + "%"

    def __eq__(self, other):
        return self.chance == other.chance

    def __lt__(self, other):
        return self.chance < other.chance


@total_ordering
class Strategy:
    """
    Class representing a single set of decision rules for the AI to play the
    game with. Includes a map of decision weights for choosing crops for
    planting, and an idea of what multiple of a field's cost the AI should have
    saved up before being able to buy it.
    """

    def __init__(self, crop_weightings, field_ratio):
        self.crop_weightings = crop_weightings
        self.field_ratio = field_ratio
        self.fitness = 0
        self.chances_to_plant = {}
        self.calculate_chances_to_plant()

    def calculate_chances_to_plant(self):
        """
        Populate this strategy's set of probabilities for planting each crop in
        the game using the stored weightings.
        """

        total_weight = sum(self.crop_weightings.keys())

        for crop, weighting in self.crop_weightings.items():
            chance = (weighting / total_weight)
            self.chances_to_plant[crop] = chance

    def describe(self):
        """
        Return a summary of this strategy's performance, and the planting
        probabilities used to achieve it.
        """

        report = ("SCORE: " + str(self.fitness) + ". Field ratio: " +
                  str(self.field_ratio) + ".")

        # Construct ordered list of crop chances
        crop_chances = []
        for crop, chance in self.chances_to_plant:
            crop_chances.append(CropChance(crop, chance))
        crop_chances.sort()

        for crop_chance in crop_chances:
            report += (crop_chance + ", ")

        return report

    def __eq__(self, other):
        return self.fitness == other.fitness

    def __lt__(self, other):
        return self.fitness < other.fitness

