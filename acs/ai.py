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


class Evolver:
    """
    Class representing the evolutionary algorithm for creating, testing and
    breeding Strategies.
    """

    NUM_GAMES = 25
    NUM_GENERATIONS = 1000
    POPULATION_SIZE = 100

    CHANCE_TO_MUTATE_CROP = 0.25
    CHANCE_TO_MUTATE_FIELD = 0.125
    FIELD_MUTATION_SIZE = 0.2

    # Selection pressure weighting, where 1 means fitness is ignored.
    SCORE_BIAS = 1.8

    # Number of generations to compute between console progress reports.
    GENERATIONS_PER_SUMMARY = 10

    def __init__(self, crops, fields):
        self.crops = crops
        self.fields = fields

    def evolve(self):
        """
        Entry point for evolutionary algorithm.
        """

        print('Evolutionary algorithm is online.')

        # Generate initial population of Strategies
        current_generation = self.generate_initial_population()

        for generation in range(Evolver.NUM_GENERATIONS):

            # Compute results of using Strategies in this generation
            self.determine_fitness(current_generation)

            # Rank the Strategies in this generation by fitness
            current_generation.sort()

            # If we are reporting this generation, report
            if generation % Evolver.GENERATIONS_PER_SUMMARY == 0:
                self.report_progress(current_generation)

            # If we are not finished yet, create the next generation
            if generation < Evolver.NUM_GENERATIONS - 1:
                next_generation = self.breed(current_generation)
                self.mutate(next_generation)
                current_generation = next_generation

        current_generation.sort()
        return current_generation

    def generate_initial_population(self):
        """
        Create a random base population of Strategies.
        """

        strategies = []

        for strategy in range(Evolver.POPULATION_SIZE):
            pass

    def determine_fitness(self, current_generation):
        """
        For each Strategy in the current generation, play the game using the
        weightings described in that strategy the given number of times, and
        store the average performance on the Strategy in question.
        """

        pass

    def report_progress(self, current_generation):
        """
        Give a summary of the current fitness of the generation as a whole, and
        list the weightings of the top few performers.
        """

        pass

    def breed(self, current_generation):
        """
        Combine the Strategies in the current generation into a population of
        equal size, preferentially using traits of the highest performers.
        """

        pass

    def mutate(self, current_generation):
        """
        For some of the given Strategies, randomize one of their crop
        weightings. Do the same for field weighting for a different subset.
        """

        pass
