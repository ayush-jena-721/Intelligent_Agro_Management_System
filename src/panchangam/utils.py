from panchangam.constants import (
    TITHI_NAMES,
    NAK_NAMES,
    YOGA_NAMES,
    KARANA_NAMES,
    VARA_NAMES
)

def decode_panchang(row):

    tithi = TITHI_NAMES[int(row["tithi_index"])]
    nak = NAK_NAMES[int(row["nakshatra_index"])]
    yoga = YOGA_NAMES[int(row["yoga_index"])]
    karana = KARANA_NAMES[int(row["karana_index"])]
    vara = VARA_NAMES[int(row["vara_index"])]

    return {
        "tithi": tithi,
        "nakshatra": nak,
        "yoga": yoga,
        "karana": karana,
        "vara": vara
    }