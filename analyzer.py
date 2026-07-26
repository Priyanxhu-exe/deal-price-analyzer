import pandas as pd
import matplotlib.pyplot as plt
import mplcursors

def calculate_statistics(prices):
    median_price = prices.median()
    lowest_price = prices.min()
    highest_price = prices.max()
    return median_price, lowest_price, highest_price

mode=input("Choose the mode you want to work with seller comparison or price trend, type '1' or '2' respectively: ") or "1"
try:
    mode = int(mode)
    if mode not in (1, 2):
        raise ValueError("Invalid mode")
except ValueError:
    print("Invalid input. Please enter '1' for seller comparison or '2' for price trend.")
    exit()
if mode==1:
    file_path = input("Enter the file path: ") or "sample_sellers.xlsx"

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print("File not found")
        exit()
    except Exception as e:
        print(f"Something went wrong: {e}")
        exit()

    base_price = float(input("Enter the base price for comparison: ") or 1050)

    price_column = input("Enter the column header for price: ") or "Price"
    label_column = input("Enter the column header for seller/source name: ") or "Seller"

    for col in (price_column, label_column):
        if col not in df.columns:
            print(f"Column '{col}' not found. Available columns: {list(df.columns)}")
            exit()

    prices = df[price_column]
    labels = df[label_column]

    median_price, lowest_price, highest_price = calculate_statistics(prices)
    print("Median:", median_price)
    print("Lowest:", lowest_price)
    print("Highest:", highest_price)

    df["Margin %"] = ((df[price_column] - base_price) / base_price) * 100

    sorted_df = df.sort_values(by=price_column)
    sorted_prices = sorted_df[price_column]
    sorted_labels = sorted_df[label_column]
    sorted_margins = sorted_df["Margin %"]

    base_color = "#4C72B0"

    plt.figure(figsize=(8, 5.5))
    plt.bar(sorted_labels, sorted_prices, color=base_color)
    plt.axhline(base_price, color="green", linestyle="-", linewidth=1, label=f"Base Price = {base_price:.2f}")
    plt.axhline(median_price, color="gray", linestyle="--", linewidth=1,
                label=f"Median = {median_price:.2f}")

    for i, p in enumerate(sorted_prices):
        margin = sorted_margins.iloc[i]
        direction = "above" if margin > 0 else "below"
        plt.text(i, p + (highest_price * 0.015), f"{p:.0f}", ha="center", fontsize=9)
        plt.text(i, p + (highest_price * 0.060), f"({abs(margin):.1f}% {direction} base)",
                          ha="center", fontsize=7, color="dimgray")

    plt.ylim(0, highest_price * 1.15)   
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
else:
    file_path = input("Enter the file path: ") or "amazon_price_history.xlsx"

    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print("File not found")
        exit()
    except Exception as e:
        print(f"Something went wrong: {e}")
        exit()

    price_column = input("Enter the column header for price: ") or "Price"
    date_column = input("Enter the column header for date: ") or "Date"

    for col in (price_column, date_column):
        if col not in df.columns:
            print(f"Column '{col}' not found. Available columns: {list(df.columns)}")
            exit()

    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(by=date_column)

    prices = df[price_column]
    dates = df[date_column]

    median_price, lowest_price, highest_price = calculate_statistics(prices)

    print("Median:", median_price)
    print("Lowest:", lowest_price)
    print("Highest:", highest_price)

    base_color = "#4C72B0"

    fig, ax = plt.subplots(figsize=(9, 5.5))
    line, = ax.plot(dates, prices, color=base_color, marker="o", markersize=3)
    ax.axhline(median_price, color="gray", linestyle="--", linewidth=1,
               label=f"Median = {median_price:.2f}")

    min_idx = prices.idxmin()
    max_idx = prices.idxmax()
    ax.annotate(f"Lowest: {lowest_price:.0f}", xy=(dates[min_idx], prices[min_idx]),
                xytext=(0, -15), textcoords="offset points", ha="center", fontsize=8, color="dimgray")
    ax.annotate(f"Highest: {highest_price:.0f}", xy=(dates[max_idx], prices[max_idx]),
                xytext=(0, 8), textcoords="offset points", ha="center", fontsize=8, color="dimgray")

    ax.set_title(f"{price_column} Trend Over Time")
    ax.set_xlabel(date_column)
    ax.set_ylabel(price_column)

    step = max(1, len(dates) // 8)
    ax.set_xticks(dates[::step])
    ax.set_xticklabels(dates[::step].dt.strftime("%b %d"), rotation=30, ha="right")

    ax.legend()

    fig.suptitle(
        f"Lowest: {lowest_price:.0f}   |   Median: {median_price:.0f}   |   "
        f"Highest: {highest_price:.0f}",
        y=0.97, fontsize=9, color="dimgray"
    )

    fig.tight_layout(rect=[0, 0, 1, 0.94])

    cursor = mplcursors.cursor(line, hover=True)

    @cursor.connect("add")
    def on_hover(sel):
        x_val, y_val = sel.target
        hovered_date = pd.to_datetime(x_val, unit="D", origin="1970-01-01")
        sel.annotation.set_text(f"{hovered_date.strftime('%b %d, %Y')}\nPrice: {y_val:.0f}")

    plt.savefig("price_trend.png")
    plt.show()