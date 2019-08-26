from alpha_vantage.timeseries import TimeSeries
import csv
import time


my_key = ""  # alphavantage key
portfolio = "portfolio.csv"
positions = "positions.csv"


def to_csv():
    with open(portfolio, "w") as portfolio_file:
        portfolio_file.write(f"{','.join(['Symbol', 'Shares', 'Price-per-share', 'Total value', 'Timestamp'])}\n")
    ts = TimeSeries(key=my_key, output_format='pandas')
    with open(positions, newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))
        i = 0
        print(f"Fetching data for {len(rows)} positions.")  # table header
        print("\tSymbol\tShares\tPrice-per-share\tTotal value\tTimestamp")  # table header
        for row in enumerate(rows):
            csv_row = row[1]
            symbol = csv_row['Symbol']
            num_shares = int(csv_row['Shares'])
            data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='compact')
            latest_price = data['4. close'].iloc[0]
            timestamp = data.index.values[0]
            value = latest_price * num_shares
            with open(portfolio, "a") as portfolio_file:
                portfolio_file.write(f"{symbol},{num_shares},{latest_price:.2f},{value:.2f},{timestamp}\n")
            if len(symbol) < 4:
                # For formatting purpose
                symbol = f"{symbol:<4}"
            print(f"{i}.\t{symbol}\t{num_shares}\t\t{latest_price:.2f}\t\t\t{value:.2f}\t\t{timestamp}")
            i += 1
            if i % 5 == 0 and i < len(rows):
                # To keep in line with the 5 calls/min rule
                time.sleep(299)
    print(f"Done fetching data for {i} symbols")


def main():
    to_csv()


if __name__ == "__main__":
    # get my key
    with open('alphavantage.key') as k:
        my_key = k.read().strip()

    # run main
    main()
