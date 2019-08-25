from alpha_vantage.timeseries import TimeSeries
import csv
import time


my_key = ""  # alphavantage key
portfolio = "portfolio.csv"


def summary():
    """
    Generates a summary of my portfolio
    :return: null
    """
    my_summary = {}  # map of symbol to total value
    ts = TimeSeries(key=my_key, output_format='pandas')
    with open(portfolio, newline='') as csvfile:
        rows = list(csv.DictReader(csvfile))
        i = 0
        print("Symbol\tShares\tPrice-per-share\tTotal value")  # table header
        for row in enumerate(rows):
            csv_row = row[1]
            symbol = csv_row['symbol']
            num_shares = int(csv_row['shares'])
            data, meta_data = ts.get_intraday(symbol=symbol, interval='1min', outputsize='compact')
            latest_price = data['4. close'].iloc[0]
            value = latest_price * num_shares
            my_summary[symbol] = value
            if len(symbol) < 4:
                # For formatting purpose
                symbol = f"{symbol:<4}"
            print(f"{symbol}\t{num_shares}\t\t{latest_price:.2f}\t\t\t{value:.2f}")
            i += 1
            if i % 5 == 0 and i < len(rows):
                # To keep in line with the 5 calls/min rule
                time.sleep(299)
    print(f"Done fetching data for {i} symbols")


def main():
    summary()


if __name__ == "__main__":
    # get my key
    with open('alphavantage.key') as k:
        my_key = k.read().strip()

    # run main
    main()
