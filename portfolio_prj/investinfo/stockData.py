from yfinance import Ticker, download
from pandas import DataFrame
import sqlite3, pandas

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


def fetchData(tickerName, start, end, period=None, interval='1h'):
    """
    Получение основной информации об инструменте
    :param tickerName:
    :param start:  гггг-мм-дд
    :param end: формат гггг-мм-дд
    :param period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    :param interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    dataFrame = download(tickers=tickerName, start=start, end=end, period=period, interval=interval)
    dataFrame.columns = dataFrame.columns.str.replace(' ', '')  # удаление пробелов в названиях столбцов
    dataFrame.insert(loc=len(dataFrame.columns), column='ticker_id', value=tickerName)  # вставка столбца с названием тикера

    connect = sqlite3.connect(r'C:\Users\subm\PycharmProjects\portfolio2\portfolio_prj\db.sqlite3')
    name = "investinfo_data"
    pandas.DataFrame.to_sql(dataFrame, name, connect, if_exists='append')


if __name__ == "__main__":
    # print(getStockData('msft'))
    print(fetchData('MSFT', start='2020-09-19', end='2020-09-22', interval='15m'))


