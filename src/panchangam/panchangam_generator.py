import json
from datetime import datetime, timedelta
import pytz
from astral import LocationInfo
from astral.sun import sunrise
from skyfield.api import load

# Local imports
from src.panchangam.constants import (
    TITHI_NAMES,
    NAK_NAMES,
    YOGA_NAMES,
    KARANA_NAMES,
    VARA_NAMES
)
from src.panchangam.panchangam_calculator import (
    get_longitudes,
    calculate_tithi,
    calculate_nakshatra,
    calculate_yoga,
    calculate_karana,
    calculate_vara,
    calculate_moon_phase,
    calculate_moon_distance
)

OUTPUT = "data/raw/panchangam_dataset.jsonl"

# Define the location for which we want to calculate the Panchangam. You can change this to any location you want by providing the appropriate latitude and longitude.
city = LocationInfo(
    "Villupuram",
    "India",
    "Asia/Kolkata",
    11.94,
    79.49
)

TZ = pytz.timezone("Asia/Kolkata")
ts = load.timescale()

# Lahiri ayanamsa approximation
AYANAMSA = 23.15
# For a more accurate calculation, you would typically calculate the ayanamsha based on the date, as it changes over time. However, for simplicity, we are using a fixed value here. In a real implementation, you would calculate the ayanamsha based on the date, as it changes over time. You can use a library like `pyswisseph` to get accurate ayanamsha values for each date if needed.
def sidereal(angle):
    return (angle - AYANAMSA) % 360

# This module generates a Panchangam dataset for each day from 1940 to 2050 by calculating the tithi, nakshatra, yoga, karana, and vara based on the positions of the sun and moon at sunrise time. The dataset is saved in a JSONL format for easy analysis and merging with weather data later.
def generate_dataset(start="1940-01-01", end="2050-12-31"):

    start_dt = datetime.fromisoformat(start)
    end_dt = datetime.fromisoformat(end)
    current = start_dt    
    with open(OUTPUT, "w") as f:
        # Loop through each day in the specified date range
        while current <= end_dt:

            # Calculate sunrise time for the current date and location
            try:
                sunrise_time = sunrise(
                    city.observer,
                    date=current.date(),
                    tzinfo=TZ
                )
            except Exception:
                # fallback if Astral fails
                print(f"Sunrise fallback used for {current}")   
                sunrise_time = TZ.localize(
                    datetime(current.year, current.month, current.day, 6, 0)
                )  
                       


            # For accurate sunrise times, you would typically use an astronomical library or API to get the actual sunrise time for the location and date. Here, we are using a fixed time of 6:00 AM IST for simplicity, but this can be improved by integrating with a library like `astral` or using the `skyfield` library to calculate the sunrise time based on the observer's location.
            t = ts.from_datetime(sunrise_time.astimezone(pytz.utc))

            # Calculate the longitudes of the sun and moon at sunrise time
            sun_lon, moon_lon = get_longitudes(t)

            # Convert to sidereal longitudes by applying the ayanamsa correction
            sun_lon = sidereal(sun_lon)
            moon_lon = sidereal(moon_lon)

            # Calculate the Panchangam elements based on the longitudes
            tithi_i, tithi = calculate_tithi(sun_lon, moon_lon)
            nak_i, nak = calculate_nakshatra(moon_lon)
            yoga_i, yoga = calculate_yoga(sun_lon, moon_lon)
            kar_i, kar = calculate_karana(sun_lon, moon_lon)
            vara_i, vara = calculate_vara(t)
            phase_angle, moon_phase_name = calculate_moon_phase(t)
            moon_distance_km = calculate_moon_distance(t)
            # Create a dictionary for the current date's Panchangam data
            row = {

                "date": current.strftime("%Y-%m-%d"),
            # Include the index and name for each Panchangam element for easier analysis later

                "tithi_index": tithi_i,
                "tithi": tithi,

                "nakshatra_index": nak_i,
                "nakshatra": nak,

                "yoga_index": yoga_i,
                "yoga": yoga,

                "karana_index": kar_i,
                "karana": kar,

                "vara_index": vara_i,
                "vara": vara,

                "moon_phase_angle": phase_angle,
                "moon_phase": moon_phase_name,

                "moon_distance_km": moon_distance_km,

                "sun_lon": sun_lon,
                "moon_lon": moon_lon
            }
            f.write(json.dumps(row) + "\n")
            current += timedelta(days=1)

    print("Panchangam dataset generated")

# Example usage:
if __name__ == "__main__":
    generate_dataset()  
