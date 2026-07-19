# Deal Price Analyzer

I'm building this to learn pandas, matplotlib, and eventually scikit-learn by working on a project I'd actually use, instead of following disconnected tutorials. The idea is to compare deal prices from multiple sellers for the same item, and see at a glance which one is the best price.

## How it works

Run the script. It asks for three things:

1. The path to your Excel file (e.g. `deals.xlsx`, or a full path if it's elsewhere). Leave it blank and it defaults to `sample_sellers.xlsx`, included in this repo.
2. The column header that holds your prices. Leave it blank and it defaults to `Price`.
3. The column header that holds the seller/source name. Leave it blank and it defaults to `Seller`.

It prints the median, lowest, and highest price, then generates a bar chart comparing every seller, sorted from cheapest to most expensive. The cheapest seller is highlighted, and a dashed line marks the median price so you can see at a glance which sellers are above or below typical price.

I'm using median instead of average as the reference point, since a single unusually high or low price can skew an average in a way that's misleading — median holds up better against that.

If the file doesn't exist or a column name is wrong, it tells you clearly instead of crashing, and shows you the column names it actually found.

### Expected Excel format

| Seller   | Price |
|----------|-------|
| Amazon   | 1200  |
| Flipkart | 1150  |
| Meesho   | 980   |

`sample_sellers.xlsx` in this repo follows this format, so it's a good first thing to run before using your own data.

## Requirements

```
pip install pandas openpyxl matplotlib
```

## Usage

```
analyzer.py
```

## Where this is at

v0.1 was the first working version — manual input through the terminal, stats from Python's `statistics` module. v0.2 moved to pandas, reading prices from an Excel file with the file path and column name entered at runtime, plus basic error handling. v0.3 added a matplotlib bar chart on top of that. This version refines the chart: it compares sellers specifically, sorts by price, highlights the cheapest option, and uses median instead of average as the reference line.

## What's next

A few directions I'm considering:
- Factoring in seller rating alongside price, so the cheapest option isn't always the one recommended if it's from an unreliable seller
- Tracking price over time for the same item, which would need a date column and a line chart instead of a bar chart — a genuinely different use case from comparing sellers at a single point in time
- Eventually pulling in real price data instead of manually entered Excel sheets, and using scikit-learn for basic price prediction once there's a real trend to learn from

## License

Not decided yet.
