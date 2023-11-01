from datetime import datetime
import MetaTrader5 as mt5
import pandas as pd
import pytz

class MarketPriceData:
    def __init__(self, login, server, password):
        self.login = login
        self.server = server
        self.password = password
        self.initialize_mt5()
    
    def initialize_mt5(self):
        if not mt5.initialize(login=self.login, server=self.server, password=self.password):
            print(f"initialize() failed, error code = {mt5.last_error()}")
            self.initialized = False
        else:
            self.initialized = True

    def fetch_data(self, asset, timeframe=mt5.TIMEFRAME_M1, date_from=None, bars=100):
        if not self.initialized:
            return None

        timezone = pytz.timezone("Etc/UTC") # Ensure that the time-zone is consistent in UTC
        date_from = date_from if date_from else datetime.now().astimezone(timezone) # Latest time-stamp of fetched data
        rates = mt5.copy_rates_from(asset, timeframe, date_from, bars)
        
        if rates is None:
            return None

        rates_frame = pd.DataFrame(rates)
        rates_frame['time'] = pd.to_datetime(rates_frame['time'], unit='s')
        return rates_frame

    def shutdown(self):
        mt5.shutdown()


if __name__ == "__main__":
    fetcher = MarketPriceData(login=51439076, server="ICMarketsSC-Demo", password="vwYYuaZt")
    
    assets = ["EURUSD", "USDJPY"]  # Add more assets as needed
    timeframe = mt5.TIMEFRAME_M1
    date_from = None
    bars = 1
    
    for asset in assets:
        data = fetcher.fetch_data(asset, timeframe, date_from, bars)
        if data is not None:
            print(f"Displaying data for {asset}")
            print(data)
        else:
            print(f"Failed to fetch data for {asset}")

    fetcher.shutdown()

