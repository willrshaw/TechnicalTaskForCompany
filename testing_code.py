from zynstra_questions import CityWeather, snow_in_any_cities, highest_wind_speed
import unittest

class TestZynstraQuestions(unittest.TestCase):
    
    # first, create some test data to be used in test cases
    test_temp_data = {"friday":[{"humidity":76,"precipitation":6,"pressure":996,"temperature":5,"wind_direction":"E","wind_speed":12},{"humidity":76,"precipitation":6,"pressure":996,"temperature":4,"wind_direction":"E","wind_speed":12}]}
    
    pressure_below_data = {"friday": [{"humidity":85,"precipitation":0,"pressure":992,"temperature":8,"wind_direction":"NE","wind_speed":3},{"humidity":85,"precipitation":0,"pressure":992,"temperature":7,"wind_direction":"NE","wind_speed":3},{"humidity":85,"precipitation":0,"pressure":992,"temperature":7,"wind_direction":"NE","wind_speed":3},{"humidity":85,"precipitation":0,"pressure":992,"temperature":6,"wind_direction":"NE","wind_speed":3},{"humidity":85,"precipitation":0,"pressure":992,"temperature":6,"wind_direction":"NE","wind_speed":4},{"humidity":85,"precipitation":0,"pressure":992,"temperature":5,"wind_direction":"NE","wind_speed":4},{"humidity":85,"precipitation":0,"pressure":992,"temperature":7,"wind_direction":"E","wind_speed":4},{"humidity":85,"precipitation":0,"pressure":992,"temperature":7,"wind_direction":"NE","wind_speed":4},{"humidity":85,"precipitation":1,"pressure":992,"temperature":7,"wind_direction":"N","wind_speed":4},{"humidity":85,"precipitation":0,"pressure":992,"temperature":8,"wind_direction":"N","wind_speed":4},{"humidity":85,"precipitation":0,"pressure":992,"temperature":9,"wind_direction":"N","wind_speed":4},{"humidity":84,"precipitation":0,"pressure":992,"temperature":10,"wind_direction":"NW","wind_speed":3},{"humidity":84,"precipitation":1,"pressure":992,"temperature":10,"wind_direction":"NW","wind_speed":3},{"humidity":85,"precipitation":1,"pressure":992,"temperature":11,"wind_direction":"NW","wind_speed":3},{"humidity":85,"precipitation":2,"pressure":992,"temperature":12,"wind_direction":"N","wind_speed":3},{"humidity":84,"precipitation":2,"pressure":992,"temperature":12,"wind_direction":"NE","wind_speed":3},{"humidity":84,"precipitation":2,"pressure":992,"temperature":12,"wind_direction":"NE","wind_speed":3},{"humidity":83,"precipitation":1,"pressure":992,"temperature":11,"wind_direction":"N","wind_speed":4},{"humidity":83,"precipitation":1,"pressure":992,"temperature":11,"wind_direction":"N","wind_speed":4},{"humidity":83,"precipitation":1,"pressure":992,"temperature":10,"wind_direction":"NW","wind_speed":3},{"humidity":83,"precipitation":1,"pressure":992,"temperature":10,"wind_direction":"NW","wind_speed":3},{"humidity":83,"precipitation":2,"pressure":992,"temperature":10,"wind_direction":"NW","wind_speed":3}]}
                           
    temp_median_data = {'monday' : [{"humidity":85,"precipitation":0,"pressure":992,"temperature":0,"wind_direction":"NE","wind_speed":3}, {"humidity":85,"precipitation":0,"pressure":992,"temperature":1,"wind_direction":"NE","wind_speed":3}, {"humidity":85,"precipitation":0,"pressure":992,"temperature":2,"wind_direction":"NE","wind_speed":3}, {"humidity":85,"precipitation":0,"pressure":992,"temperature":3,"wind_direction":"NE","wind_speed":3}, {"humidity":85,"precipitation":0,"pressure":992,"temperature":4,"wind_direction":"NE","wind_speed":3}]}
    
    def test_get_temp(self):
        fake_city = CityWeather("TemperatureVille", self.test_temp_data)
        self.assertEqual(fake_city.get_temp('friday', 0), 5, "CityWeather.get_temp retrieves wrong temperature")


    def test_pressure_below(self):
        fake_city = CityWeather("Pascalton", self.pressure_below_data)
        self.assertTrue(fake_city.pressure_below_on_day(1000, 'friday'), "CityWeather.pressure_below_on_day failed")

    def test_median_temp(self):
        fake_city = CityWeather("Middlesfjord", self.temp_median_data)
        self.assertEqual(fake_city.get_temp_median(), 2, "CityWeather.get_temp_median failed")
        
    def test_get_higest_windspeed(self):
        fake_city = CityWeather("WindyCity", self.pressure_below_data)
        self.assertEqual(fake_city.get_highest_wind_speed(), 4, "CityWeather.get_highest_wind_speed failed")
if __name__ == "__main__":
    unittest.main()