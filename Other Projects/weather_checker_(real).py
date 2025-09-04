'''import python_weather
import asyncio
import os

async def get_weather(location: str) -> None:
    # declare the client with the unit system (Imperial for Fahrenheit, mph, etc.)
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        try:
            # fetch the weather forecast for the given location
            weather = await client.get(location)
            
            # display the current temperature
            print(f"\nThe current temperature in {location} is {weather.temperature}°F.")
            print(f"with a high of {daily.weather.highest_temperature}°F and a low of {daily.weather.lowest_temperature}°F.")
        except Exception as e:
            print(f"Error: Unable to retrieve detailed weather information for '{location}'. Please ensure the location is valid and try again.")

if __name__ == '__main__':
    if os.name == 'nt':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    location = input("Enter a location to get the weather: ")
    asyncio.run(get_weather(location))
'''

import python_weather

import asyncio
import os

async def getweather() -> None:
  # declare the client. the measuring unit used defaults to the metric system (celcius, km/h, etc.)
  async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
    # fetch a weather forecast from a city
    weather = await client.get('San Francisco')

    # returns the current day's forecast temperature (int)
    print(forecast.chances_of_high_temperature)

    # get the weather forecast for a few days
    for daily in weather:
      print(daily)

      # hourly forecasts
      for hourly in daily:
        print(f' --> {hourly!r}')

if __name__ == '__main__':
  # see https://stackoverflow.com/questions/45600579/asyncio-event-loop-is-closed-when-getting-loop
  # for more details
  if os.name == 'nt':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

  asyncio.run(getweather())
