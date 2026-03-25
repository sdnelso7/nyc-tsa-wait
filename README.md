# nyc-tsa-wait

Live TSA security checkpoint wait times for NYC-area airports — JFK, LGA, and EWR — in your terminal.

## Installation

```bash
pip install -e .
```

## Usage

Show wait times for all three airports:

```bash
tsa-wait
```

Show a specific airport:

```bash
tsa-wait JFK
tsa-wait LGA EWR
```

## Example output

```
JFK — John F. Kennedy International  (updated 08:22 AM)
╭────────────┬──────────┬──────────────╮
│ Terminal   │ Standard │ TSA PreCheck │
├────────────┼──────────┼──────────────┤
│ Terminal 1 │  11 min  │    4 min     │
│ Terminal 4 │  18 min  │    6 min     │
│ Terminal 5 │  Closed  │    Closed    │
│ Terminal 7 │   5 min  │      —       │
│ Terminal 8 │   8 min  │    3 min     │
╰────────────┴──────────┴──────────────╯
```

Wait times are color-coded: green (≤10 min), yellow (≤20 min), red (>20 min).

## Data source

Data comes from the Port Authority of New York & New Jersey's backend, the same source used by [jfkairport.com](https://www.jfkairport.com), [laguardiaairport.com](https://www.laguardiaairport.com), and [newarkairport.com](https://www.newarkairport.com). Updated every few minutes.
