import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

DATA_PATH = "data/processed/merged_imd-weather_dataset.csv"

# Load the dataset
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")
    return df

# Detect cycles in rainfall data using Fourier Transform
def detect_cycles(df):
    # rainfall = df["rainfall"].values
    rainfall = df["rainfall"].rolling(7).mean().fillna(0).values  # Smooth the data with a 7-day rolling average to reduce noise
    # Number of samples
    N = len(rainfall)
    T = 1  # 1 day interval
    # Perform Fourier Transform
    yf = fft(rainfall)
    xf = fftfreq(N, T)[:N//2]
    # Calculate the power of the frequencies
    power = 2.0/N * np.abs(yf[0:N//2])
    return xf, power

# Plot the frequency spectrum to visualize the detected cycles
def plot_cycles(xf, power):
    plt.figure(figsize=(10,5))
    plt.plot(xf, power)
    plt.title("Rainfall Frequency Spectrum")
    plt.xlabel("Frequency (1/day)")
    plt.ylabel("Power")
    plt.show()

# Main function to run the analysis
def run():
    df = load_data()
    xf, power = detect_cycles(df)
    plot_cycles(xf, power)

# Entry point
if __name__ == "__main__":
    run()