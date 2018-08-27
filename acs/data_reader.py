from farm import Crop, Field
import json


class DataReader:

    crops_file_name = "../crops.dat"
    fields_file_name = "../fields.dat"


    def import_crops(self):

        imported_crops = []

        try:
            raw_crops = self.read_data(DataReader.crops_file_name)

            for crop in raw_crops["crops"]:

                imported_crop = Crop(
                    crop["id"],
                    crop["name"],
                    crop["description"],
                    crop["cost"],
                    crop["sale_price"],
                    crop["ideal_heat"],
                    crop["ideal_wetness"],
                    crop["heat_sensitivity"],
                    crop["wetness_sensitivity"]
                )
                imported_crops.append(imported_crop)

        except (ValueError, KeyError, TypeError):
            print("JSON Format Error")

        return imported_crops


    def import_fields(self):

        imported_fields = []

        try:
            raw_fields = self.read_data(DataReader.fields_file_name)

            for field in raw_fields["fields"]:

                imported_field = Field(
                    field["id"],
                    field["name"],
                    field["description"],
                    None,
                    None,
                    field["max_crop_quantity"],
                    field["soil_quality"],
                    field["price"]
                )
                imported_fields.append(imported_field)

        except (ValueError, KeyError, TypeError):
            print("JSON Format Error")

        return imported_fields


    def read_data(self, file_name):

        with open(file_name, encoding="utf-8") as data_file:
            data = json.load(data_file)

        return data
