# run py -m pip install -r .\requirements.txt
import alpaca_trade_api as tradeapi
from alpaca_trade_api import StreamConn
import rx
import threading
import time
import datetime
import logging
import argparse
# You must initialize logging, otherwise you'll not see debug output.
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True

# API KEYS
#region
API_KEY = "ALPACA API KEY HERE"
API_SECRET = "ALPACA API SECRET HERE"
APCA_API_BASE_URL = "https://paper-api.alpaca.markets"
#endregion
#Buy a stock when a doji candle forms
class BuyAtDoji:
  def __init__(self):
    self.alpaca = tradeapi.REST(API_KEY, API_SECRET, APCA_API_BASE_URL, api_version='v2')
  def run(self):
        #On Each Minute
        async def on_minute(bar):
            symbol = bar.symbol
            print("Close: ", bar.close)
            print("Open: ", bar.open)
            print("Low: ", bar.low)
            print(symbol)
            #Check for Doji
            if bar.close > bar.open and bar.open - bar.low > 0.1:
              print('Buying on Doji!')
              respSO = []
              self.submitMarketOrder(1, symbol, 'buy', respSO)
            # check position and take profit, 
            # Get the rate at which the market order was filled 
            # place a limit order at 1% higher than market order deal rate
              positions = self.alpaca.list_positions()
              for position in positions:
                if(position.side == 'long'):
                  self.submitLimitOrder(position.qty, symbol, 'sell', position.avg_entry_price + (position.avg_entry_price * 0.1), respSO)
        # Use rx timer to get prices every 5 minutes
        # Subscribe to Microsoft Stock
        rx.timer(5.0).subscribe(lambda t: on_minute(self.alpaca.get_barset('MSFT', 'minute', 1)))

  def submitMarketOrder(self, qty, stock, side, resp):
    if(qty > 0):
      try:
        self.alpaca.submit_order(stock, qty, side, "market", "day")
        print("Market order of | " + str(qty) + " " + stock + " " + side + " | completed.")
        resp.append(True)
      except:
        print("Order of | " + str(qty) + " " + stock + " " + side + " | did not go through.")
        resp.append(False)
    else:
      print("Quantity is 0, order of | " + str(qty) + " " + stock + " " + side + " | not completed.")
      resp.append(True)

  def submitLimitOrder(self, qty, stock, side, price, resp):
    if(qty > 0):
      try:
        self.alpaca.submit_order(stock, qty, side, "limit", "day", price)
        print("Limit order of | " + str(qty) + " " + stock + " " + side + " | completed.")
        resp.append(True)
      except:
        print("Order of | " + str(qty) + " " + stock + " " + side + " | did not go through.")
        resp.append(False)
    else:
      print("Quantity is 0, order of | " + str(qty) + " " + stock + " " + side + " | not completed.")
      resp.append(True)           
# Run the BuyDoji class
ls = BuyAtDoji()
ls.run()