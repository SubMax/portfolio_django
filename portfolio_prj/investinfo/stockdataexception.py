import re
import time


class StockDataValueError(ValueError):
    pass


class StockDataIntervalValueError(StockDataValueError):
    def __init__(self, ticker, message):
        self.ticker = ticker
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        self.date_pattern = r'\d{10}'
        self.result = re.findall(self.date_pattern, self.message)
        for d in self.result:
            self.message = re.sub(self.date_pattern,
                                  time.strftime('%Y-%m-%d %X', time.localtime(int(d))),
                                  self.message,
                                  count=1)
        return self.message
