import unittest
import acs.ai as ai
import acs.farm as farm


class TestStrategy(unittest.TestCase):

    def setUp(self):
        self.crop_1 = farm.Crop(1, 'Crop 1', 'Crop 1', 10, 20, 1.1, 0.9, 2, 0.5)
        self.crop_2 = farm.Crop(2, 'Crop 2', 'Crop 2', 5, 15, 1.2, 0.8, 0.5, 2)

        crop_weightings = {self.crop_1: 5, self.crop_2: 20}
        field_ratio = 0.9
        self.strategy = ai.Strategy(crop_weightings, field_ratio)

    def test_calculate_chances_to_plant(self):
        # GIVEN two crops with weightings of 5 and 20
        # WHEN I calculate their chances to plant
        self.strategy.calculate_chances_to_plant()

        # THEN the chance of the first crop being planted is 0.2
        self.assertEqual(0.2, self.strategy.chances_to_plant[self.crop_1])

    def test_replace_weighting(self):
        # GIVEN my weighting for crop_1 is 5
        # WHEN I try to replace it with 10
        self.strategy.replace_weighting(self.crop_1, 10)

        # THEN its weighting is now 10
        self.assertEqual(10, self.strategy.crop_weightings[self.crop_1])
