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
        pass

    def test_generate_initial_population(self):
        pass

    def test_generate_random_strategy(self):
        pass
