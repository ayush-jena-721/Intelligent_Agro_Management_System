import pandas as pd
import matplotlib.pyplot as plt

# Load the cleaned dataset
df = pd.read_csv("data/processed/clean_dataset.csv")

# remove date column
df_numeric = df.drop(columns=["date"])

# compute correlation
corr = df_numeric.corr()

# print rainfall correlation
print("\nCorrelation with Rainfall:\n")
print(corr["rainfall"].sort_values(ascending=False))

# plot heatmap
plt.figure(figsize=(12,8))
plt.imshow(corr)
plt.colorbar()
# Set the ticks and labels
plt.xticks(range(len(corr.columns)), corr.columns, rotation=90)
plt.yticks(range(len(corr.columns)), corr.columns)

plt.title("Climate Feature Correlation Matrix")

plt.tight_layout()
plt.show()