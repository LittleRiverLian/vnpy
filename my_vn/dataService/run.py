#!/usr/bin/env python
# coding: utf-8

from datetime import datetime

from dataService import downloadDailyBarBySymbol
from turtleEngine import BacktestingEngine


def runBacktesting(filename):
    engine = BacktestingEngine()
    engine.setPeriod(datetime(2014, 1, 1), datetime(2019, 6, 30))
    engine.initPortfolio(filename, 10000000)

    engine.loadData()
    engine.runBacktesting()
    engine.showResult()


runBacktesting("setting_portfolio.csv")

# 下载数据
# downloadDailyBarBySymbol("IF99")
# downloadDailyBarBySymbol("I99")
# downloadDailyBarBySymbol("CU99")
# downloadDailyBarBySymbol("TA99")
# downloadDailyBarBySymbol("AL99")
# downloadDailyBarBySymbol("RB99")
# downloadDailyBarBySymbol("ZN99")
# downloadDailyBarBySymbol("M99")
# downloadDailyBarBySymbol("J99")
# downloadDailyBarBySymbol("JM99")
