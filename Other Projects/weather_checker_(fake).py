import time
import threading
import random

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
    user_input = input(f"\nEnter your current location: ")
    print()

    loading_thread = threading.Thread(target=show_loading_screen)
    loading_thread.start()
    loading_thread.join()

    print(f"\nIdk. Go outside for once and feel it for yourself.\n")

if __name__ == "__main__":
    weather_app()
