# Deal Price Analyzer

I'm building this to learn pandas, matplotlib, and eventually scikit-learn by working on a project I'd actually use, instead of following disconnected tutorials. It's grown into two things in one script now: comparing prices across sellers for the same item, and tracking how one seller's price moves over time.

## How it works

Run the script. First it asks which mode:

- **1 — Seller comparison.** Compares prices across sellers at one point in time, against a base price you type in.
- **2 — Price trend.** Tracks one seller's price across multiple dates as a line chart.

**Mode 1** asks for the Excel file, a base price to compare against, and the price/seller column names (all have defaults if you just hit enter). It prints median, lowest, highest, then a bar chart sorted cheapest to most expensive, with each bar labeled with its price and how far above or below the base price it is. I went with median over average here — one weirdly high or low price skews an average in a way that's misleading, median holds up better.

**Mode 2** asks for the file and the price/date columns, then plots a line chart over time with the lowest and highest points called out directly on the chart. You can hover over any point to see the exact date and price.

Both modes handle a missing file or a typo'd column name without crashing — they tell you what went wrong and show you what columns actually exist.

### Sample files included

`sample_sellers.xlsx` — Seller / Price, for mode 1
`amazon_price_history.xlsx` — Seller / Date / Price, for mode 2

## Requirements

```
pip install pandas openpyxl matplotlib mplcursors
```

## Usage

```
python analyzer.py
```

## Where this is at

v0.1 was manual terminal input and Python's `statistics` module. v0.2 moved to pandas for Excel input. v0.3 added a matplotlib bar chart. This version split into the two modes, added the base price / margin comparison to mode 1, and added the hover tooltip to mode 2 using mplcursors.

## What's next

Talked to someone in my family who trades commodities professionally, and got a few real ideas out of it — mainly that prices should be benchmarked against something like the LME (London Metal Exchange) reference price instead of just a number I type in myself, and that seller trade history over time matters more than a single day's price. That second one needs `groupby` in pandas, which I haven't properly used yet.

After that: scikit-learn for basic price prediction once there's a real trend to learn from, and probably wrapping this in Streamlit so it's an actual small app instead of a terminal script.

## License

Not decided yet.
