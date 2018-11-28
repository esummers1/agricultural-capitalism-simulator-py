import unittest
import acs.ai as ai
import acs.farm as farm


class TestCropChance(unittest.TestCase):

    def setUp(self):
        self.crop_1 = farm.Crop(1, 'Crop 1', 'Crop 1', 10, 20, 1.1, 0.9, 2, 0.5)
        self.crop_2 = farm.Crop(2, 'Crop 2', 'Crop 2', 5, 15, 1.2, 0.8, 0.5, 2)

        self.crop_chance_1 = ai.CropChance(self.crop_1, 0.4)
        self.crop_chance_2 = ai.CropChance(self.crop_2, 0.6)

    def test_equal_to_are_unequal(self):
        # GIVEN crops with unequal chances of being planted
        # WHEN I check whether their chances are equal
        # THEN I find that they are not
        self.assertFalse(self.crop_chance_1.__eq__(self.crop_chance_2))

    def test_equal_to_are_equal(self):
        # GIVEN crops with equal chances of being planted
        self.crop_chance_1.chance = 0.5
        self.crop_chance_2.chance = 0.5

        # WHEN I check whether their chances are equal
        # THEN I find that they are
        self.assertTrue(self.crop_chance_1.__eq__(self.crop_chance_2))

    def test_less_than_is_less_than(self):
        # GIVEN crops with 40% and 60% chances of being planted
        # WHEN I check whether the first is less likely than the second
        # THEN I find that it is
        self.assertTrue(self.crop_chance_2.__lt__(self.crop_chance_1))

    def test_less_than_is_greater_than(self):
        # GIVEN crops with 40% and 60% chances of being planted
        # WHEN I check whether the second is less likely than the first
        # THEN I find that it is not
        self.assertFalse(self.crop_chance_1.__lt__(self.crop_chance_2))


class TestStrategy(unittest.TestCase):

    def setUp(self):
        self.crop_1 = farm.Crop(1, 'Crop 1', 'Crop 1', 10, 20, 1.1, 0.9, 2, 0.5)
        self.crop_2 = farm.Crop(2, 'Crop 2', 'Crop 2', 5, 15, 1.2, 0.8, 0.5, 2)

        self.strategy_1 = ai.Strategy({self.crop_1: 5, self.crop_2: 20}, 0.9)
        self.strategy_1.fitness = 100

        self.strategy_2 = ai.Strategy({self.crop_1: 20, self.crop_2: 5}, 1.5)
        self.strategy_2.fitness = 200

    def test_calculate_chances_to_plant(self):
        # GIVEN two crops with weightings of 5 and 20
        # WHEN I calculate their chances to plant
        self.strategy_1.calculate_chances_to_plant()

        # THEN the chance of the first crop being planted is 0.2
        self.assertEqual(0.2, self.strategy_1.chances_to_plant[self.crop_1])

    def test_replace_weighting(self):
        # GIVEN my weighting for crop_1 is 5
        # WHEN I try to replace it with 10
        self.strategy_1.replace_weighting(self.crop_1, 10)

        # THEN its weighting is now 10
        self.assertEqual(10, self.strategy_1.crop_weightings[self.crop_1])

    def test_equal_to_are_equal(self):
        # GIVEN strategies with equal fitness
        self.strategy_2.fitness = 100

        # WHEN I determine whether their fitness is equal
        # THEN I find that they are
        self.assertTrue(self.strategy_1.__eq__(self.strategy_2))

    def test_equal_to_are_unequal(self):
        # GIVEN strategies with unequal fitness
        # WHEN I determine whether their fitness is equal
        # THEN I find that they are not
        self.assertFalse(self.strategy_1.__eq__(self.strategy_2))

    def test_less_than_is_less_than(self):
        # GIVEN strategies with fitness scores of 100 and 200
        # WHEN I determine whether the first is less fit than the second
        # THEN I find that it is
        self.assertTrue(self.strategy_2.__lt__(self.strategy_1))

    def test_less_than_is_greater_than(self):
        # GIVEN strategies with fitness scores of 100 and 200
        # WHEN I determine whether the second is less fit than the first
        # THEN I find that it is not
        self.assertFalse(self.strategy_1.__lt__(self.strategy_2))


class TestEvolver(unittest.TestCase):

    def setUp(self):
        self.crops = [
            farm.Crop(1, 'Crop 1', 'Crop 1', 10, 20, 1.1, 0.9, 2, 0.5),
            farm.Crop(2, 'Crop 2', 'Crop 2', 5, 15, 1.2, 0.8, 0.5, 2)
        ]
        self.fields = [farm.Field(1, 'Field 1', '', 100, 1, 1000)]
        self.evolver = ai.Evolver(20, 500, self.crops, self.fields)
        self.crop_weightings = {self.crops[0]: 50, self.crops[1]: 80}
        self.strategy = ai.Strategy(self.crop_weightings, 2)

    def test_generate_random_strategy(self):
        # GIVEN some Evolver
        # WHEN I use it to create a random Strategy
        strategy = self.evolver.generate_random_strategy()

        # THEN this Strategy has a populated dictionary of crop weightings
        self.assertEqual(len(self.crops), len(strategy.crop_weightings))

        # AND a field ratio greater than or equal to 1
        self.assertTrue(strategy.field_ratio >= 1)

    def test_evaluate_strategy(self):
        # GIVEN some Evolver and some Strategy
        # WHEN I evaluate its fitness
        self.evolver.evaluate_strategy(self.strategy)

        # THEN its fitness is greater than zero, as even a lost game will have
        # a positive score
        self.assertTrue(self.strategy.fitness > 0)

    def test_create_child(self):
        # GIVEN father and mother Strategies
        father = ai.Strategy({self.crops[0]: 100, self.crops[1]: 100}, 5)
        mother = ai.Strategy({self.crops[0]: 50, self.crops[1]: 50}, 3)

        # WHEN I combine them to create a child
        child = ai.Evolver.create_child(father, mother)

        # THEN the child has the father's odd-numbered crop weightings
        self.assertEqual(
            father.crop_weightings[self.crops[0]],
            child.crop_weightings[self.crops[0]])

        # AND it has the mother's even-numbered crop weightings
        self.assertEqual(
            mother.crop_weightings[self.crops[1]],
            child.crop_weightings[self.crops[1]])

        # AND its field ratio is the average of both parents'
        self.assertEqual(4, child.field_ratio)

    def test_calculate_common_ratio(self):
        # GIVEN I know the common ratio
        # WHEN I use it to describe a geometric sequence of equal size to the
        # population
        remaining_probability = 1
        current_probability = self.evolver.initial_selection_probability

        for i in range(ai.Evolver.POPULATION_SIZE):
            remaining_probability -= current_probability
            current_probability *= self.evolver.common_ratio

        # THEN the sequence tends to 1
        self.assertTrue(remaining_probability < 0.01)
