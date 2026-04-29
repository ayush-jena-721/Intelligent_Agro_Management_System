# ------------------------
# Panchangam name lists
# ------------------------

# The tithi is calculated based on the difference between the moon's longitude and the sun's longitude, divided into 30 equal parts of 12 degrees each.
TITHI_NAMES = [
"Pratipada","Dvitiya","Tritiya","Chaturthi","Panchami","Shashti",
"Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
"Trayodashi","Chaturdashi","Purnima",
"Krishna Pratipada","Krishna Dvitiya","Krishna Tritiya","Krishna Chaturthi",
"Krishna Panchami","Krishna Shashti","Krishna Saptami","Krishna Ashtami",
"Krishna Navami","Krishna Dashami","Krishna Ekadashi","Krishna Dwadashi",
"Krishna Trayodashi","Krishna Chaturdashi","Amavasya"
]

# The nakshatra is calculated based on the moon's longitude, divided into 27 equal parts of 13.33 degrees each.
NAK_NAMES = [
"Ashwini","Bharani","Krittika","Rohini","Mrigashirsha","Ardra","Punarvasu","Pushya","Ashlesha",
"Magha","Purva Phalguni","Uttara Phalguni","Hasta","Chitra","Swati","Vishakha","Anuradha",
"Jyeshtha","Mula","Purva Ashadha","Uttara Ashadha","Shravana","Dhanishta","Shatabhisha",
"Purva Bhadrapada","Uttara Bhadrapada","Revati"
]

# The yoga is calculated based on the sum of the sun and moon longitudes, divided into 27 equal parts.
YOGA_NAMES = [
"Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda","Sukarma","Dhriti","Shoola",
"Ganda","Vriddhi","Dhruva","Vyaghata","Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha",
"Shiva","Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"
]

# The karana is calculated based on the tithi, with each tithi having two karanas (except for the 30th tithi which has only one). There are 11 unique karanas that repeat in a specific pattern.
KARANA_NAMES = [
"Bava","Balava","Kaulava","Taitila","Garija","Vanija","Vishti",
"Shakuni","Chatushpada","Naga","Kimstughna"
]

# The vara (weekday) is calculated based on the day of the week, with Sunday as the first day.
VARA_NAMES = [
"Ravivara","Somavara","Mangalavara","Budhavara","Guruvara","Shukravara","Shanivara"
]