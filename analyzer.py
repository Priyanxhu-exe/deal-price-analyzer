import pandas as pd
import matplotlib.pyplot as plt

file_path = input("Enter the file path: ") or "sample_sellers.xlsx"

try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print("File not found")
    exit()
except Exception as e:
    print(f"Something went wrong: {e}")
    exit()

price_column = input("Enter the column header for price: ") or "Price"
label_column = input("Enter the column header for seller/source name: ") or "Seller"

for col in (price_column, label_column):
    if col not in df.columns:
        print(f"Column '{col}' not found. Available columns: {list(df.columns)}")
        exit()

prices = df[price_column]
labels = df[label_column]

median_price = prices.median()
lowest_price = prices.min()
highest_price = prices.max()

print("Median:", median_price)
print("Lowest:", lowest_price)
print("Highest:", highest_price)

sorted_df = df.sort_values(by=price_column)
sorted_prices = sorted_df[price_column]
sorted_labels = sorted_df[label_column]

base_color = "#4C72B0"
highlight_color = "#DD8452"
colors = [highlight_color if p == lowest_price else base_color for p in sorted_prices]

plt.figure(figsize=(8, 5.5))
plt.bar(sorted_labels, sorted_prices, color=colors)
plt.axhline(median_price, color="gray", linestyle="--", linewidth=1,
            label=f"Median = {median_price:.2f}")

for i, p in enumerate(sorted_prices):
    plt.text(i, p + (highest_price * 0.015), f"{p:.0f}", ha="center", fontsize=9)

plt.title(f"{price_column} Comparison by {label_column}")
plt.xlabel(label_column)
plt.ylabel(price_column)
plt.xticks(rotation=30, ha="right")
plt.legend()

plt.suptitle(
    f"Lowest: {lowest_price:.0f}   |   Median: {median_price:.0f}   |   "
    f"Highest: {highest_price:.0f}",
    y=0.93, fontsize=9, color="dimgray"
)

plt.tight_layout(rect=[0, 0, 1, 0.93])

plt.savefig("seller_comparison.png")
plt.show()