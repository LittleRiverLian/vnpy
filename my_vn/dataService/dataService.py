# encoding: UTF-8

from __future__ import print_function
import json
from datetime import datetime
from time import time

from vnpy.trader.constant import Interval, Exchange
from vnpy.trader.object import BarData, TickData
from vnpy.trader.database import database_manager

import rqdatac as rq

# 加载配置
config = open('config.json')
setting = json.load(config)

USERNAME = setting['rqUsername']
PASSWORD = setting['rqPassword']
rq.init(USERNAME, PASSWORD)

FIELDS = ['open', 'high', 'low', 'close', 'volume']


# ----------------------------------------------------------------------
def generateVtBar(row, symbol, interval):
    """生成K线"""
    bar = BarData(
        symbol=symbol,
        datetime=row.name,
        open_price=row['open'],
        high_price=row['high'],
        low_price=row['low'],
        close_price=row['close'],
        volume=row['volume'],
        exchange=Exchange.SHFE,
        interval=interval,
        gateway_name='DB',
    )
    return bar


# ----------------------------------------------------------------------
def generateVtTick(row, symbol):
    """生成K线"""
    tick = TickData(
        symbol=symbol,
        last_price=row['last'],
        volume=row['volume'],
        open_interest=row['open_interest'],
        datetime=row.name,
        open_price=row['open'],
        high_price=row['high'],
        low_price=row['low'],
        pre_close=row['prev_close'],
        limit_up=row['limit_up'],
        limit_down=row['limit_down'],
        bid_price_1=row['b1'],
        bid_price_2=row['b2'],
        bid_price_3=row['b3'],
        bid_price_4=row['b4'],
        bid_price_5=row['b5'],
        bid_volume_1=row['b1_v'],
        bid_volume_2=row['b2_v'],
        bid_volume_3=row['b3_v'],
        bid_volume_4=row['b4_v'],
        bid_volume_5=row['b5_v'],
        ask_price_1=row['a1'],
        ask_price_2=row['a2'],
        ask_price_3=row['a3'],
        ask_price_4=row['a4'],
        ask_price_5=row['a5'],
        ask_volume_1=row['a1_v'],
        ask_volume_2=row['a2_v'],
        ask_volume_3=row['a3_v'],
        ask_volume_4=row['a4_v'],
        ask_volume_5=row['a5_v']
    )

    return tick


# ----------------------------------------------------------------------
def downloadMinuteBarBySymbol(symbol):
    """下载某一合约的分钟线数据"""
    start = time()
    df = rq.get_price(symbol, frequency='1m', fields=FIELDS)
    bars = []
    for ix, row in df.iterrows():
        bar = generateVtBar(row, symbol, Interval.MINUTE)
        bars.append(bar)
    database_manager.save_bar_data(bars)

    end = time()
    cost = (end - start) * 1000

    print(u'合约%s的分钟K线数据下载完成%s - %s，耗时%s毫秒' % (symbol, df.index[0], df.index[-1], cost))


# ----------------------------------------------------------------------
def downloadDailyBarBySymbol(symbol):
    """下载某一合约日线数据"""
    start = time()

    df = rq.get_price(symbol, frequency='1d', fields=FIELDS,start_date="2013-01-04", end_date=datetime.now().strftime('%Y%m%d'))
    bars = []
    for ix, row in df.iterrows():
        bar = generateVtBar(row, symbol, Interval.DAILY)
        bars.append(bar)
    database_manager.save_bar_data(bars)

    end = time()
    cost = (end - start) * 1000

    print(u'合约%s的日K线数据下载完成%s - %s，耗时%s毫秒' % (symbol, df.index[0], df.index[-1], cost))


# ----------------------------------------------------------------------
def downloadTickBySymbol(symbol, date):
    """下载某一合约日线数据"""
    start = time()

    df = rq.get_price(symbol, frequency='tick', start_date=date, end_date=date)
    ticks = []
    for ix, row in df.iterrows():
        tick = generateVtTick(row, symbol)
        ticks.append(tick)
    database_manager.save_bar_data(ticks)

    end = time()
    cost = (end - start) * 1000

    print(u'合约%sTick数据下载完成%s - %s，耗时%s毫秒' % (symbol, df.index[0], df.index[-1], cost))
