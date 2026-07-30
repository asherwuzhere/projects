import asyncio
import os

import python_weather


async def get_weather(location: str) -> None:
    async with python_weather.Client(unit=python_weather.IMPERIAL) as client:
        try:
            weather = await client.get(location)
        except Exception as exc:
            print(f"Unable to retrieve weather for {location}: {exc}")
            return

        print(f"\nCurrent temperature in {location}: {weather.temperature}°F")
        forecasts = list(weather)
        if forecasts:
            today = forecasts[0]
            print(
                f"Today's high: {today.highest_temperature}°F; "
                f"low: {today.lowest_temperature}°F"
            )


def main() -> None:
    if os.name == "nt":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    location = input("Enter a location to get the weather: ").strip()
    if not location:
        raise SystemExit("A location is required.")
    asyncio.run(get_weather(location))


if __name__ == "__main__":
    main()
