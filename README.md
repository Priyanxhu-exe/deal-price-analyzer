Deal Price Analyzer

I'm building this to learn pandas, matplotlib, and eventually scikit-learn by working on a project I'd actually use, instead of following disconnected tutorials. The idea is simple: compare a set of deal prices and get the average, median, lowest, and highest — but do it properly, from an Excel sheet, instead of typing prices in one by one.

How it works

Run the script. It asks for two things:


The path to your Excel file (e.g. deals.xlsx, or a full path if it's elsewhere). Leave it blank and it defaults to sample_deals.xlsx, included in this repo.
The column header that holds your prices. Leave it blank and it defaults to Price.


It then prints the average, median, lowest, and highest price from that column.

If the file doesn't exist or the column name is wrong, it tells you clearly instead of crashing — and if the column name is wrong, it also shows you the column names it actually found.

Expected Excel format

| Deal   | Price |
|--------|-------|
| Deal A | 1200  |
| Deal B | 1350  |
| Deal C | 980   |

sample_deals.xlsx in this repo follows this format, so it's a good first thing to run before using your own data.

Requirements

pip install pandas openpyxl

Usage

analyzer.py

Where this is at

v0.1 was the first working version — manual input through the terminal, stats from Python's statistics module. v0.2 is the current version: it reads from Excel using pandas, and the file path and column name are entered at runtime instead of hardcoded, with basic error handling around both.

Next, I'm adding graphs with matplotlib, then looking at basic price prediction with scikit-learn once that's solid.

License

Not decided yet.
