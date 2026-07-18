import pandas as pd
file_path = input("Enter the file path: ") or "sample_deals.xlsx"
# change this to your file name
try:
    df = pd.read_excel(file_path)
except FileNotFoundError:
    print("File not found")
    exit()
except Exception as e:
    print(f"Something went wrong: {e}")
    exit()
column_name = input("Enter the column header name: ") or "Price"
 
if column_name not in df.columns:
    print(f"Column '{column_name}' not found. Available columns: {list(df.columns)}")
    exit()

prices = df[column_name]

average_price = prices.mean()
median_price = prices.median()
lowest_price = prices.min()
highest_price = prices.max()

print("Average:", average_price)
print("Median:", median_price)
print("Lowest:", lowest_price)
print("Highest:", highest_price)
