# encoding: UTF-8

"""
导入CSV历史数据到MongoDB中
"""

from datetime import datetime
import csv
from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import BarData
from vnpy.trader.database import database_manager

# ----------------------------------------------------------------------
def loadCsv(filename, symbol):

    """"""
    # 读取数据和插入到数据库
    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        bars = []
        for d in reader:
            date = d['date']
            tm = d['time']
            dt = datetime.strptime(date + ' ' + tm, '%Y%m%d %H:%M:%S')

            bar = BarData(
                symbol=symbol,
                datetime=dt,
                open_price=float(d['open']),
                high_price=float(d['high']),
                low_price=float(d['low']),
                close_price=float(d['close']),
                volume=d['volume'],
                exchange=Exchange.SHFE,
                interval=Interval.DAILY,
                gateway_name='DB',
            )
            bars.append(bar)

        database_manager.save_bar_data(bars)


if __name__ == '__main__':
    loadCsv('IF99.csv', 'IF99')
    loadCsv('RB99.csv', 'RB99')
    loadCsv('TA99.csv', 'TA99')
    loadCsv('I99.csv', 'I99')
