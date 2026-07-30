import time
import threading

def show_loading_screen():
    loading_messages = [
        "Calibrating Atmospheric Sensors",
        "Extracting Meteorological Anomalies",
        "Compiling Thermodynamic Parameters",
        "Synchronizing Geospatial Climate Data",
        "Deconstructing Hydrometeorological Patterns"
    ]
    
    for message in loading_messages:
        print(message, end="", flush=True)
        time.sleep(0.5)
        print(".", end="", flush=True)
        time.sleep(0.5)
        print(".", end="", flush=True)
        time.sleep(0.5)
        print(".", end="", flush=True)
        time.sleep(1)
        print()

def weather_app():
    location = input("\nEnter your current location: ").strip()
    if not location:
        print("A location is required.")
        return
    print()

    loading_thread = threading.Thread(target=show_loading_screen)
    loading_thread.start()
    loading_thread.join()

    print(f"\nWeather for {location}: go outside and feel it for yourself.\n")

if __name__ == "__main__":
    weather_app()
