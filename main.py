from alpha_vantage.timeseries import TimeSeries
import matplotlib.pyplot as plt
import csv
import time


my_key = ""  # alphavantage key
PORTFOLIO = "portfolio.csv"
POSITIONS = "positions.csv"


def to_csv():
    """
    Fetches the latest market data using the Alphavantage API.
    For each position in POSITIONS, it fetches the market data, and writes the
    following to PORTFOLIO: Symbol, Shares, Price-per-share, Total value, Timestamp,
    where Price-per-share is the price at the time represented in Timestamp.
    It also prints these information to STDIO
    TODO: Sort the entries based on percentage value
    :return: null
    """
    with open(PORTFOLIO, "w") as portfolio_file:
        # First write the heading into PORTFOLIO
        portfolio_file.write(f"{','.join(['Symbol', 'Shares', 'Price-per-share', 'Total value', 'Timestamp'])}\n")
    ts = TimeSeries(key=my_key, output_format='pandas')
    with open(POSITIONS, newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))
        i = 0
        print(f"Fetching data for {len(rows)} positions.")
        print("\tSymbol\tShares\tPrice-per-share\tTotal value\tTimestamp")
        for row in enumerate(rows):
            # For each row in POSITIONS
            csv_row = row[1]
            symbol = csv_row['Symbol']
            num_shares = int(csv_row['Shares'])
            # Fetch from Alphavantage
            data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='compact')
            latest_price = data['4. close'].iloc[0]
            timestamp = data.index.values[0]
            value = latest_price * num_shares
            with open(PORTFOLIO, "a") as portfolio_file:
                # Write to PORTFOLIO
                portfolio_file.write(f"{symbol},{num_shares},{latest_price:.2f},{value:.2f},{timestamp}\n")
            if len(symbol) < 4:
                # For formatting purpose
                symbol = f"{symbol:<4}"
            print(f"{i}.\t{symbol}\t{num_shares}\t\t{latest_price:.2f}\t\t\t{value:.2f}\t\t{timestamp}")
            i += 1
            if i % 5 == 0 and i < len(rows):
                # To keep in line with the 5 calls/min rule from Alphavantage
                time.sleep(299)
    print(f"Done fetching data for {i} symbols")


def gen_graphics():
    """
    Generates graphics for PORTFOLIO
    :return: null
    """
    # Fetch data from PORTFOLIO
    symbols, shares, pps, values = [], [], [], []
    with open(PORTFOLIO, "r") as portfolio_file:
        reader = csv.DictReader(portfolio_file)
        for cvs_row in reader:
            symbols.append(cvs_row['Symbol'])
            shares.append(cvs_row['Shares'])
            pps.append(cvs_row['Price-per-share'])
            values.append(cvs_row['Total value'])

    # Draw pie chart
    fig1, ax1 = plt.subplots()
    ax1.pie(values, labels=symbols, autopct='%1.1f%%')
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.show()


def main():
    # to_csv()
    gen_graphics()


if __name__ == "__main__":
    # get my key
    with open('alphavantage.key') as k:
        my_key = k.read().strip()

    # run main
    main()
