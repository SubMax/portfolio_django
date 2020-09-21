from yfinance import Ticker

'''
Модуль для работы с yfinance, для получения информации об инвестиционных инструментах

'''


def getStockData(tickerName):
    """
    :param tickerName: краткое название биржевого инструмента
    :return: возвращает список из [тикера, название компании, описание компании, ссылка на лого]
    """

    info = []
    ticker = Ticker(tickerName).info
    info.append(ticker.get('symbol'))
    info.append(ticker.get('longName'))
    info.append(ticker.get('longBusinessSummary'))
    info.append(ticker.get('logo_url'))
    return info


def fetchData(tickerName, start, stop, interval):
    pass


if __name__ == "__main__":
    print(getStockData('msft'))
