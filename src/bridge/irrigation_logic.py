def irrigation_decision(predictions, soil_moisture=None):
    
    rain_expected = predictions.mean() > 0.5

    if soil_moisture is not None:
        if soil_moisture > 70:
            return "NO - Soil already wet"

    if rain_expected:
        return "NO - Rain expected 🌧️"

    return "YES - Irrigation needed 💧"