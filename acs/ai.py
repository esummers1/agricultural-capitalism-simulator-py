from functools import total_ordering
import random

import acs.input_providers
from acs.game import *


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
        return other.chance == self.chance

    def __lt__(self, other):
        return other.chance < self.chance


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

        total_weight = sum(self.crop_weightings.values())

        for crop, weighting in self.crop_weightings.items():
            chance = (weighting / total_weight)
            self.chances_to_plant[crop] = chance

    def describe(self):
        """
        Return a summary of this strategy's performance, and the planting
        probabilities used to achieve it.
        """

        report = ("SCORE: " + str(round(self.fitness)) + "  Field ratio: " +
                  "{:.3f}".format(round(self.field_ratio, 3)) + " || ")

        # Construct ordered list of crop chances
        crop_chances = []
        for crop, chance in self.chances_to_plant.items():
            crop_chances.append(CropChance(crop, chance))
        crop_chances.sort()

        for crop_chance in crop_chances:
            report += (crop_chance.crop.name + ": " +
                       str(int(round(crop_chance.chance * 100))) + "%  ")

        print(report)

    def replace_weighting(self, crop_to_replace, new_weighting):
        """
        Update an existing Crop => Weighting pair with a given new weighting.
        """

        for crop, weighting in self.crop_weightings.items():
            if crop == crop_to_replace:
                self.crop_weightings[crop] = new_weighting
        self.calculate_chances_to_plant()

    def __eq__(self, other):
        return other.fitness == self.fitness

    def __lt__(self, other):
        return other.fitness < self.fitness


class Evolver:
    """
    Class representing the evolutionary algorithm for creating, testing and
    breeding Strategies.
    """

    NUM_GAMES = 20
    NUM_GENERATIONS = 1000
    POPULATION_SIZE = 100

    CHANCE_TO_MUTATE_CROP = 0.25
    CHANCE_TO_MUTATE_FIELD = 0.2
    FIELD_MUTATION_SIZE = 0.7

    # Number of generations to compute between console progress reports.
    GENERATIONS_PER_SUMMARY = 1

    # Number of Strategies included in progress reports.
    TOP_STRATEGIES_TO_REPORT = 5

    def __init__(self, max_years, initial_money, crops, fields):
        self.max_years = max_years
        self.initial_money = initial_money
        self.crops = crops
        self.fields = fields

        # Probability of selecting the first available parent (start of
        # geometric sequence)
        self.initial_selection_probability = 2 / Evolver.POPULATION_SIZE

        # Common ratio for geometric selection sequence
        self.common_ratio = Evolver.calculate_common_ratio(self)

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
                average_fitness = \
                    self.sum_fitness_of_strategies(current_generation) \
                    / Evolver.POPULATION_SIZE

                self.report_progress(
                    current_generation, generation, average_fitness)

            # If we are not finished yet, create the next generation
            if generation < Evolver.NUM_GENERATIONS - 1:
                next_generation = self.breed_generation(current_generation)
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
            strategies.append(self.generate_random_strategy())

        return strategies

    def generate_random_strategy(self):
        """
        Create a random Strategy.
        """

        crop_weightings = {}

        for crop in self.crops:
            weighting = random.randint(1, 1000)
            crop_weightings[crop] = weighting

        field_ratio = random.random() * 2 + 1

        return Strategy(crop_weightings, field_ratio)

    def determine_fitness(self, current_generation):
        """
        For each Strategy in the supplied generation, determine its fitness at
        playing the game.
        """

        for strategy in current_generation:
            self.evaluate_strategy(strategy)

    def evaluate_strategy(self, strategy):
        """
        Exercise a single Strategy for the requisite number of games and store
        its fitness.
        """

        input_provider = acs.input_providers.AIInputProvider(strategy)
        scores = []

        # Run Strategy through games
        for i in range(Evolver.NUM_GAMES):
            game = Game(
                self.max_years,
                self.initial_money,
                input_provider,
                self.crops,
                self.fields)
            score = game.run()
            scores.append(score)

        # Calculate overall fitness
        strategy.fitness = sum(scores) / len(scores)

    @staticmethod
    def sum_fitness_of_strategies(strategies):
        """
        For a list of Strategies whose fitness has been computed, return the
        sum of their fitnesses (i.e. average scores across all games).
        """

        total_fitness = 0

        for strategy in strategies:
            total_fitness += strategy.fitness

        return total_fitness

    @staticmethod
    def report_progress(current_generation, generation_number, average_fitness):
        """
        Give a summary of the current fitness of the generation as a whole, and
        list the weightings of the top few performers.
        """

        print("\n***** Generation " + str(generation_number + 1)
              + " - Average Score: " + str(round(average_fitness)))
        Evolver.print_top_strategies(
            current_generation, Evolver.TOP_STRATEGIES_TO_REPORT)

    @staticmethod
    def print_top_strategies(strategies, number_to_list):
        """
        Given a list of Strategies sorted by fitness and a number N, list the
        weightings of the top N Strategies.
        """

        maximum = min(number_to_list, len(strategies))

        for i in range(maximum):
            strategies[i].describe()

    def breed_generation(self, current_generation):
        """
        Combine the Strategies in the current generation into a population of
        equal size, preferentially using traits of the highest performers.
        """

        next_generation = []

        for i in range(Evolver.POPULATION_SIZE):

            # Select parent Strategies
            father = self.choose_parent(current_generation)
            mother = self.choose_parent(current_generation)

            # Create child
            next_generation.append(Evolver.create_child(father, mother))

        return next_generation

    @staticmethod
    def create_child(father, mother):
        """
        Given 'father' and 'mother' Strategies, combine their traits into a
        single child Strategy.
        """

        child_crop_weightings = {}

        # Use odd-number ID crop weightings from father Strategy
        for crop, weighting in father.crop_weightings.items():
            if crop.id % 2 != 0:
                child_crop_weightings[crop] = weighting

        # Use even-number ID crop weightings from mother Strategy
        for crop, weighting in mother.crop_weightings.items():
            if crop.id % 2 == 0:
                child_crop_weightings[crop] = weighting

        # Take average of field weightings from both Strategies
        child_field_ratio = 0.5 * (father.field_ratio + mother.field_ratio)

        return Strategy(child_crop_weightings, child_field_ratio)

    def calculate_common_ratio(self):
        """
        Use an iterative technique to calculate the common ratio for the
        geometric sequence used to select parent strategies.
        """

        this_r = self.initial_selection_probability
        size = Evolver.POPULATION_SIZE

        while True:
            next_r = ((size - 2) + 2 * (this_r ** size)) / size

            if abs(next_r - this_r) < 0.000001:
                return this_r
            else:
                this_r = next_r

    def choose_parent(self, generation):
        """
        Return a parent Strategy from the given list at random, with earlier
        (i.e. fitter) Strategies being advantaged.
        """

        r = random.random()
        initial_probability = self.initial_selection_probability
        cumulative_probability = initial_probability

        for counter, strategy in enumerate(generation, start=1):

            if r < cumulative_probability:
                return strategy

            # Use the common ratio and our position in the list to calculate the
            # additive probability of the current element, given that each
            # element has the probability of the previous * the common ratio.
            cumulative_probability += \
                (self.initial_selection_probability
                 * self.common_ratio ** (counter - 1))

        return generation[len(generation) - 1]

    def mutate(self, current_generation):
        """
        For some of the given Strategies, randomize one of their crop
        weightings. Do the same for field weighting for a different subset.
        """

        for strategy in current_generation:
            r = random.random()

            if r < Evolver.CHANCE_TO_MUTATE_CROP:
                self.mutate_crop_weighting(strategy)

            # If mutating field ratio, add or subtract up to the size constant
            if r < Evolver.CHANCE_TO_MUTATE_FIELD:
                Evolver.mutate_field_ratio(strategy)

    def mutate_crop_weighting(self, strategy):
        """
        Randomly mutate a random crop weighting of the supplied Strategy.
        """

        # Determine which crop's weighting to change
        weighting_to_change = \
            int(round(random.random() * (len(self.crops) - 1)))

        # Generate new weighting
        new_weighting = int(round(random.random() * 100))

        # Replace weighting in Strategy
        strategy.replace_weighting(
            self.crops[weighting_to_change], new_weighting)

    @staticmethod
    def mutate_field_ratio(strategy):
        """
        Mutate the given Strategy's field ratio by up to the known maximum
        mutation size.
        """

        # Generate field ratio delta
        delta = (random.random() * 2 - 1) * Evolver.FIELD_MUTATION_SIZE

        # Modify field ratio in Strategy
        strategy.field_ratio += delta
