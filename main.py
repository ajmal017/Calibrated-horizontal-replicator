from QuantConnect import *
from QuantConnect.Data import *
from QuantConnect.Algorithm import *
from QuantConnect.Indicators import *
#########################################
from datetime import timedelta

# Kommentar zu Testzwecken!

# ein weiterer Kommentar nachem ich *.qcproject zu .gitignore hinzugefügt habe. :-)

class MACD_Extension_Example(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 7, 1)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        tickers = ["SPY", "WMT", "PG", "JPM", "JNJ"]
        self.symbols = [self.AddEquity(ticker, Resolution.Daily).Symbol for ticker in tickers]
        self.macd = { symbol: self.MACD(symbol, 12, 26, 9, MovingAverageType.Exponential, Resolution.Daily) for symbol in self.symbols}
        self.std = {symbol: self.STD(symbol, 9, Resolution.Daily) for symbol in self.symbols}
        self.macd_std = {symbol: IndicatorExtensions.Of(self.macd[symbol], self.std[symbol]) for symbol in self.symbols}
        self.SetWarmUp(timedelta(days=26))


    def OnData(self, data):
        
        
        for symbol in self.symbols:
            if data.Bars.ContainsKey(symbol):
                self.macd[symbol].Update(data[symbol].EndTime, data[symbol].Close)
                self.std[symbol].Update(data[symbol].EndTime, data[symbol].Close)
                if self.macd[symbol].IsReady and self.std[symbol].IsReady:
                    self.macd_std[symbol].Update(data[symbol].EndTime, data[symbol].Close)
                
                if self.macd_std[symbol].IsReady:
                    macd = self.macd[symbol].Current.Value
                    macd_std = self.macd_std[symbol].Current.Value
                    self.Debug("{0} | MACD Value of {1} : {2}".format(self.Time, symbol, macd))
                    self.Debug("{0} | MACD_STD Value of {1} : {2}".format(self.Time, symbol, macd_std))