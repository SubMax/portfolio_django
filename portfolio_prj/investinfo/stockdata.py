import pandas
import sqlite3
import os

from yfinance import Ticker, download, shared

from .stockdataexception import StockDataIntervalValueError, StockDataValueError
import time

'''
Модуль для работы с yfinance, для получения
информации об инвестиционных инструментах

'''


def get_info_data(tickername):
    """
    :param tickername: краткое название биржевого инструмента
    :return: возвращает список из [тикера, название компании,
     описание компании, ссылка на лого]
    """

    info = {}
    try:
        info = Ticker(tickername).info
    except (IndexError, ):
        info = None
    return info


def fetchdata(**kwargs):
    """
    Получение основной информации об инструменте
    :param tickername:
    :param start:  гггг-мм-дд
    :param end: формат гггг-мм-дд
    :param period: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
    :param interval: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
    """
    tickername = kwargs.get('tickername')
    start = kwargs.get('start')
    end = kwargs.get('end')
    period = kwargs.get('period')
    interval = kwargs.get('interval')
    _shared = shared
    download_errors = _shared._ERRORS

    if not interval:
        interval = '1m'

    if period:
        start, end = None, None

    if not period and not start and not end:
        period, interval = '1d', '1m'

    try:
        dataframe = download(tickers=tickername,
                             start=start,
                             end=end,
                             period=period,
                             interval=interval)
        download_errors = _shared._ERRORS
        if download_errors:
            raise StockDataIntervalValueError(tickername, download_errors.get(tickername))
    except StockDataIntervalValueError:
        dataframe = download(tickers=tickername,
                             start=start,
                             end=end,
                             period=period,
                             interval='60m')
        if download_errors:
            raise StockDataIntervalValueError(tickername, download_errors.get(tickername))

    dataframe.dropna(inplace=True)
    dataframe.columns = dataframe.columns.str.replace(' ', '')
    # удаление пробелов в названиях столбцов
    dataframe.insert(loc=len(dataframe.columns),
                     column='ticker_id',
                     value=tickername)
    # вставка столбца с названием тикера
    for axe in dataframe.axes:
        if axe.name:
            axe.name = "Datetime"

    path = os.getcwd()
    path = path + "/db.sqlite3"

    connect = sqlite3.connect(path)
    name = "investinfo_data"
    pandas.DataFrame.to_sql(dataframe, name, connect, if_exists='append')


if __name__ == "__main__":
    # print(get_info_data('msft'))
    # print(fetchdata(tickerName='MSFT',
    #                 start='2020-09-19',
    #                 end='2020-09-22',
    #                 interval='15m'))
    fetchdata(tickername='A', period='max', interval='1wk')
