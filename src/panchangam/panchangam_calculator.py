# Panchangam Calculator
import math
from skyfield.api import load
from skyfield.almanac import moon_phase
import pytz

# Local imports
from src.panchangam.constants import (
    TITHI_NAMES,
    NAK_NAMES,
    YOGA_NAMES,
    KARANA_NAMES,
    VARA_NAMES
)

# Load ephemeris once (efficient)
ts = load.timescale()
eph = load("de440s.bsp") # You can choose a different ephemeris if needed, but DE440s is a good modern choice for accurate planetary positions.
# Define the celestial bodies we need for calculations
SUN = eph["sun"]
MOON = eph["moon"]
EARTH = eph["earth"]

# ------------------------
# Utility functions
# ------------------------

# Normalize angle to [0, 360)
def normalize(angle):
    return angle % 360

# # Ayanamsa is the difference between the tropical and sidereal zodiacs, which is used in Vedic astrology to calculate the positions of celestial bodies in the sidereal zodiac. The value of ayanamsa changes over time due to the precession of the equinoxes, so it should ideally be calculated based on the date. However, for simplicity, we are using a fixed value here. In a real implementation, you would calculate the ayanamsa based on the date, as it changes over time. You can use a library like `pyswisseph` to get accurate ayanamsa values for each date if needed.
# AYANAMSA = 23.15   # approx for 1940 (Lahiri)
# # For a more accurate calculation, you would typically calculate the ayanamsha based on the date, as it changes over time. However, for simplicity, we are using a fixed value here. In a real implementation, you would calculate the ayanamsha based on the date, as it changes over time. You can use a library like `pyswisseph` to get accurate ayanamsha values for each date if needed.
# def sidereal(angle):
#     return (angle - AYANAMSA) % 360

# Get the longitudes of the sun and moon at a given time
def get_longitudes(time):
    geo = EARTH.at(time)
    sun = geo.observe(SUN).apparent()
    moon = geo.observe(MOON).apparent()
    _, sun_lon, _ = sun.ecliptic_latlon()
    _, moon_lon, _ = moon.ecliptic_latlon()
    return normalize(sun_lon.degrees), normalize(moon_lon.degrees)


# -------------------------
# Panchangam calculations
# -------------------------

# The tithi is calculated based on the difference between the moon's longitude and the sun's longitude, divided into 30 equal parts of 12 degrees each.
def calculate_tithi(sun_lon, moon_lon):
    diff = normalize(moon_lon - sun_lon)
    tithi_index = int(diff // 12)
    return tithi_index, TITHI_NAMES[tithi_index]

# The nakshatra is calculated based on the moon's longitude, divided into 27 equal parts of 13.33 degrees each.
def calculate_nakshatra(moon_lon):
    nak_index = int(moon_lon // (360/27))
    return nak_index, NAK_NAMES[nak_index]

# The yoga is calculated based on the sum of the sun and moon longitudes, divided into 27 equal parts.
def calculate_yoga(sun_lon, moon_lon):
    val = normalize(sun_lon + moon_lon)
    yoga_index = int(val // (360/27))
    return yoga_index, YOGA_NAMES[yoga_index]

KARANA_CYCLE = [
"Bava","Balava","Kaulava","Taitila",
"Garija","Vanija","Vishti"
]
# The karana is calculated based on the tithi, with each tithi having two karanas (except for the 30th tithi which has only one). There are 11 unique karanas that repeat in a specific pattern.
def calculate_karana(sun_lon, moon_lon):
    diff = (moon_lon - sun_lon) % 360
    half_tithi = int(diff // 6)
    # repeating karanas
    repeating = [
        "Bava","Balava","Kaulava","Taitila",
        "Garija","Vanija","Vishti"
    ]
    # fixed ending karanas
    fixed = ["Shakuni","Chatushpada","Naga","Kimstughna"]
    if half_tithi >= 56:
        index = 7 + (half_tithi - 56)
        return index, fixed[half_tithi - 56]
    index = half_tithi % 7
    return index, repeating[index]


# The vara (weekday) is calculated based on the day of the week, with Sunday as the first day.
def calculate_vara(time):
    weekday = time.utc_datetime().weekday()
    vara_index = (weekday + 1) % 7
    return vara_index, VARA_NAMES[vara_index]

#-------------------------
# Moon phase calculations
#-------------------------
def calculate_moon_phase(time):
    phase_angle = moon_phase(eph, time).degrees
    if phase_angle < 22.5:
        phase = "New Moon"
    elif phase_angle < 67.5:
        phase = "Waxing Crescent"
    elif phase_angle < 112.5:
        phase = "First Quarter"
    elif phase_angle < 157.5:
        phase = "Waxing Gibbous"
    elif phase_angle < 202.5:
        phase = "Full Moon"
    elif phase_angle < 247.5:
        phase = "Waning Gibbous"
    elif phase_angle < 292.5:
        phase = "Last Quarter"
    else:
        phase = "Waning Crescent"

    return phase_angle, phase

#--------------------------
# Moon distance calculation
#--------------------------
def calculate_moon_distance(time):
    geo = EARTH.at(time)
    moon = geo.observe(MOON).apparent()
    distance_km = moon.distance().km
    return distance_km