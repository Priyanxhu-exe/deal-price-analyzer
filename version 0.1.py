n=int(input("How many deals do you want to compare? "))
prices=[]
for i in range (n):
    price = float(input(f"Enter price {i+1}: "))
    prices.append(price)
import statistics

print("Average: ", statistics.mean(prices))
print("Median: ", statistics.median(prices))
print("Lowest: ", min(prices))
print("Highest:", max(prices))