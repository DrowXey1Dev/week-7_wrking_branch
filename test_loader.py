#-----IMPORTS-----#
import unittest
import pandas as pd
import math
from loader import *


#test known valid locations return the correct latitude and logitude and that the type is valid
class TestLoader(unittest.TestCase):
    def test_valid_locations(self):
        #create instance from the module under test
        geolocator = get_geolocator()

        #predetermined valid test location
        valid_locations = {
            "Museum of Modern Art": {"latitude": 40.7618552, "longitude": -73.9782438, "type": "museum"},
            "USS Alabama Battleship Memorial Park": {"latitude": 30.684373, "longitude": -88.015316, "type": "park"}
        }
        #parse list, and find the location data per each item
        for x, expected in valid_locations.items():
            #call the function to queiry the geolocator for the target name
            result = fetch_location_data(geolocator, x)
            #class self reference
            #ensure that each assertion is approximately equal to what is expected of the result
            self.assertIsNotNone(result, "Result should not be None for valid locations")
            self.assertAlmostEqual(result["latitude"], expected["latitude"], delta=0.01)
            self.assertAlmostEqual(result["longitude"], expected["longitude"], delta=0.01)
            #ensure that type is not a NaN string
            self.assertFalse(pd.isna(result["type"]), "Type should not be NaN for valid locations")


    def test_invalid_location(self):
        #instantiate again
        geolocator = get_geolocator()
        #queiry an random invalid location string that shouldnt exist
        result = fetch_location_data(geolocator, "asdfqwer1234")

        #ensure that NaN values are returned for each invalid return
        self.assertTrue(math.isnan(result["latitude"]), "Latitude should return NaN for invalid location")
        self.assertTrue(math.isnan(result["longitude"]), "Longitude should return NaN for invalid location")
        self.assertTrue(pd.isna(result["type"]), "Type should return NaN for invalid location")


#-----TEMP MAIN-----#
#debug code. remove.
if __name__ == "__main__":
    unittest.main()




