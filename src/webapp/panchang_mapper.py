import pandas as pd

# ------------------------
# IMPORT CONSTANTS
# ------------------------
from panchangam.constants import (
    TITHI_NAMES,
    NAK_NAMES,
    YOGA_NAMES,
    KARANA_NAMES,
    VARA_NAMES
)

# ------------------------
# SAFE INDEX MAPPER
# ------------------------
def safe_index_map(series, names_list):
    """
    Maps numeric values safely to list names.
    Handles:
    - NaN
    - strings
    - 0-based or 1-based indexing
    """

    def map_value(x):
        try:
            if pd.isna(x):
                return x

            x = int(float(x))  # handles "5", 5.0, etc.

            # ✅ Auto-detect 1-based indexing
            if x >= 1 and x <= len(names_list):
                return names_list[x - 1]

            # ✅ Handle 0-based indexing
            elif x >= 0 and x < len(names_list):
                return names_list[x]

            else:
                return x

        except:
            return x

    return series.apply(map_value)


# ------------------------
# MAIN MAPPING FUNCTION
# ------------------------
def map_panchang_names(df):
    df = df.copy()

    # Ensure no duplicate columns (important fix)
    df = df.loc[:, ~df.columns.duplicated()]

    # ---------------- TITHI ----------------
    if "tithi" in df.columns:
        df["tithi"] = safe_index_map(df["tithi"], TITHI_NAMES)

    # ---------------- NAKSHATRA ----------------
    if "nakshatra" in df.columns:
        df["nakshatra"] = safe_index_map(df["nakshatra"], NAK_NAMES)

    # ---------------- VARA ----------------
    if "vara" in df.columns:
        df["vara"] = safe_index_map(df["vara"], VARA_NAMES)

    # ---------------- OPTIONAL ----------------
    if "yoga" in df.columns:
        df["yoga"] = safe_index_map(df["yoga"], YOGA_NAMES)

    if "karana" in df.columns:
        df["karana"] = safe_index_map(df["karana"], KARANA_NAMES)

    return df