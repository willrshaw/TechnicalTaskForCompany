import sys
import json
import requests
from tqdm import tqdm # for progress monitoring
from typing import List, Dict


class CityWeather():
    def __init__(self, name, weather):
        self.name = name
        self.weather = weather # store all weather in this variable to reduce requests
        
        
    def __str__(self): # ToString method for printing
        return self.name
    
   
    def get_temp(self, day : str, hour : int) -> int: # used for Q1, Q3, Q5
        """get_temp Get temperature in a current city at a certain time and  day.

        Parameters
        ----------
        day : str
            Day in string format
        hour : str
            Time in 24 hour clock format

        Returns
        -------
        int
            Temperature in degrees C, int.
        """
        temp = self.weather[day][hour]["temperature"]
        return temp
    
    def pressure_below_on_day(self, limit : int, day : str) -> bool: # used in Q2
        """pressure_below_on_day Returns true if the pressure falls below limit at any time on day supplied

        Parameters
        ----------
        limit : int
            Limit in millibars, int
        day : str
            Day to test, string

        Returns
        -------
        bool
            True if pressure falls below limit on day, False if not.
        """
        for data_point in self.weather[day]:
            if data_point['pressure'] < limit:
                return True
        return False # if loop does not trigger the return, return False as pressure never fell below limit
        
        
    def get_temp_median(self) -> int: # pass no params as we look over every data point on every day
        """get_temp_median Calculate the median temperature over entire week's datapoints.

        Returns
        -------
        _type_
            Median tempature in degrees C, int.
        """
        temp_list = []
        # O(N^2), but max run time of 24 * 7 so not bad. 
        for day in self.weather:
            for hour in self.weather[day]:
                temp_list.append(hour['temperature'])
                
        # definition of median is
        # case 1: odd length list => central value of sorted list
        # case 2: even length list=> (list[n // 2] + list[n // 2 + 1]) / 2
        # note that: 24 * 7 is always even, so I will put even case first
        # but, I will include odd case just incase data is imcomplete
        
        temp_list.sort() # list has to be sorted, inbuilt function is better than what I can make
        if (len(temp_list) % 2 == 0):
            left = temp_list[len(temp_list) // 2]
            right = temp_list[len(temp_list) // 2 + 1]
            return int((left + right) / 2)
        
        else:
            return int(temp_list[len(temp_list) // 2])
    
    def get_highest_wind_speed(self) -> int: # used for Q4
        """get_highest_wind_speed Returns the highest wind speed over an entire week

        Returns
        -------
        int
            Wind speed in knots(?), int
        """
        speed = 0 # base case, will iter over all wind speed values and then compare to this
        for day in self.weather:
            for hour in self.weather[day]:
                speed = max(speed, hour['wind_speed']) # keep highest
                
        return speed
    
    def temp_below_all_week(self, limit : int) -> bool: # Used for Q5
        """temp_below_all_week Return True or False if the temperture falls below limit during a week

        Parameters
        ----------
        limit : int
            Limit for the temperature to fall below in degrees C, int.

        Returns
        -------
        bool
            True if temperature falls below limit, False if not.
        """
        for day in self.weather:
            for hour in self.weather[day]:
                if hour["temperature"] < limit: # return True first time temp falls below limit
                    return True                 # this saves wasting iterations on comparisons
                
        return False
        


def highest_wind_speed(cities : Dict[str, CityWeather]) -> str: # Used for Q4
    """highest_wind_speed Returns name of city which 

    Parameters
    ----------
    cities : dict
        Dict of City names : CityWeather object pairs
    Returns
    -------
    str
        Name of city with highest windspeed
    """
    city_highest = ""
    speed = 0
    for city in cities:
        current_speed = cities[city].get_highest_wind_speed()
        if current_speed > speed: 
            city_highest = city
            speed = current_speed
        elif current_speed == speed and city < city_highest: # could combine these if statements with an OR, but this is more readable
            city_highest = city
            speed = current_speed            
    return city_highest

def snow_in_any_cities(cities : Dict[str, CityWeather], temp_limit : int = 2) -> bool: #used for Q5
    for city in cities:
        if cities[city].temp_below_all_week(temp_limit):
            return True
    return False
def main():
    
    # accouting for tests where a different candidate number is used
    if len(sys.argv) > 1:
        cn = sys.argv[1]
    else:
        # no sys args, use candidate number provided by email
        cn = 75
    
    # for JSON get requests, everything will be wrapped in try-catch blocks
    
    try: # get all cities, these will be iter'd over to generate data for all cities
        api_response = requests.get("http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/cities/")

        all_cities = api_response.json()["cities"] # extract city names
    except:
        print("JSON GET request failed, is the link correct and your network connected?")
        raise
    
    
    # generate all cities, use hashmap approach which in pyhon is a dict of
    # {city name : city weather objects}
    
    cities = dict()
    tqdm_city_loop = tqdm(all_cities)
    print('Generating all City Weather objects')
    for city_name in tqdm_city_loop:
        tqdm_city_loop.set_description(f"Processing {city_name}")
        try:
            api_response = requests.get(f"http://weather-api.eba-jgjmjs6p.eu-west-2.elasticbeanstalk.com/api/weather/{cn}/{city_name}/")
            
            if api_response.ok:
                new_city = CityWeather(city_name, api_response.json()) # new cityWeather object populated with weather data
                cities.update({city_name : new_city})
                
        except:
            print("Error creating city object, does the city exist?")
            raise
    
    
    # Questions:
    q_dict = {1 : "What will the temperature be in Bath at 10am on Wednesday morning? int",
              2 : "Does the pressure fall below 1000 millibars in Edinburgh at any time on Friday? boolean",
              3 : "What is the median temperature during the week for Cardiff? int",
              4 : "In which city is the highest wind speed recorded this week? If there is more than one city shares the maximum speed, choose the one which is first alphabetically. string",
              5 : " It is likely to snow if there is precipitation when the temperature is below 2 degrees. Will it snow in any of the cities this week? Boolean"}
   
    print(f"Question 1: {q_dict[1]} => {cities['bath'].get_temp('wednesday', 10)}")
    print(f"Question 2: {q_dict[2]} => {cities['edinburgh'].pressure_below_on_day(1000, 'friday')}")
    print(f"Question 3: {q_dict[3]} => {cities['cardiff'].get_temp_median()}")
    print(f"Question 4: {q_dict[4]} => {highest_wind_speed(cities)}")
    print(f"Question 5: {q_dict[5]} => {snow_in_any_cities(cities, 2)}")
    
if __name__ == "__main__":
    main()