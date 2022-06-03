# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Utility functions

from asyncio import exceptions
from time import strftime
import matplotlib as plt
from matplotlib.pyplot import subplot
import numpy as np
import yfinance as yf
import streamlit as st
import pandas as pd
from glov import vars
import logging
from logging import config
from datetime import date, datetime
#!!B-------------------------------------------------------------------------------------------------------------------------------------
#!! Tracker of events that happen when SApp run run_app.
#   Execeptions also will be logged in err_log
#!! INPUT:


def active_logger():

    try:
        config.fileConfig('log.conf')
        # Create logger
        vars.logger = logging.getLogger(vars.the_writer)
        # return vars.logger
    except Exception as e:
        logger = logging.getLogger(vars.the_writer)
        logger.setLevel(logging.DEBUG)
        error_log = logging.FileHandler(vars.error_log)
        error_log.setLevel(logging.ERROR)
        formatter = logging.Formatter(vars.logformat, datefmt=vars.datefmt)
        error_log.setFormatter(formatter)
        logger.addHandler(error_log)
        logger.error("Error Type : {}, Error Message : {}".format(
            type(e).__name__, e))
        vars.logger = logger
        # return vars.logger
#!!E-------------------------------------------------------------------------------------------------------------------------------------


@st.cache(suppress_st_warning=True, allow_output_mutation=True)

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Fetching data from yahoo finance
#!! INPUT: list of tickers
def get_yfdata(inputs):
    try:
        tickers = inputs[vars.Symbol]

        yfdata_DF = pd.DataFrame()
        if inputs[vars.xPeriod]:
            period = inputs[vars.Period]
            yfdata_DF = yf.download(
                tickers, period=period, group_by=tickers, interval=vars.interval)
        else:
            start_date = inputs[vars.Start]
            end_date = inputs[vars.End]
            yfdata_DF = yf.download(
                tickers, start=start_date, end=end_date, group_by=tickers, interval=vars.interval)
        yfdata_DF.fillna(0, inplace=True)
        yfdata_DF.dropna(inplace=True)
        yfdata_DF.reset_index(inplace=True)
        yfdata_DF = np.round(yfdata_DF, decimals=2)
        yfdata_DF["Volume"] = yfdata_DF["Volume"].map('{:,d}'.format)
        pd.options.display.float_format = '{:, .2f}'.format
        yfdata_DF.sort_values("Datetime", ascending=False)
        return yfdata_DF
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Calculate Technical Indicator MACD https://www.tradingview.com/scripts/
    #   MACD Line: (12-day EMA - 26-day EMA)
    #   Signal Line: 9-day EMA of MACD Line
    #   MACD Histogram: MACD Line - Signal Line
#!! INPUT: ticker data includes Adj Close


def MACD(data, column=vars.AdjClose, fast=12, slow=26, smooth=9):
    try:
        result = data.copy()  # make a copy of input data
        result["FMA"] = result[column].ewm(span=fast, min_periods=fast).mean()
        result["SMA"] = result[column].ewm(span=slow, min_periods=slow).mean()
        result["MACD"] = result["FMA"] - result["SMA"]
        result["SIGNAL"] = result["MACD"].ewm(
            span=smooth, min_periods=smooth).mean()
        # return result.loc[:,["FMA","SMA","MACD", "SIGNAL"]]
        return result["FMA", "SMA", "MACD", "SIGNAL"]
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------


#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Calculate Exponential Moving Average https://www.tradingview.com/scripts/
    # Calculation EMA, Double EMA, Triple EMA
    # There are three steps to calculate the EMA. Here is the formula for a 5 Period EMA

    # 1. Calculate the SMA

    # (Period Values / Number of Periods)
    # 2. Calculate the Multiplier

    # (2 / (Number of Periods + 1) therefore (2 / (5+1) = 33.333%
    # 3. Calculate the EMA
    # For the first EMA, we use the SMA(previous day) instead of EMA(previous day).

    # EMA = {Close - EMA(previous day)} x multiplier + EMA(previous day)
#!! INPUT: ticker data includes Adj Close
def EMA(data, column=vars.AdjClose, short=50, long=200):
    try:
        result = data.copy()
        # EMA
        sema = result[column].ewm(span=short, min_periods=short).mean()
        lema = result[column].ewm(span=long, min_periods=long).mean()
        result["SEMA"] = sema
        result["LEMA"] = lema

        # Double EMA
        sema2 = sema.ewm(span=short, min_periods=short).mean()
        lema2 = lema.ewm(span=long, min_periods=long).mean()
        result["DSEMA"] = 2*sema - sema2
        result["DLEMA"] = 2*lema - lema2

        # Triple EMA
        result["TSEMA"] = (3*sema - 3*sema2) + \
            sema2.ewm(span=short, min_periods=short).mean()
        result["TLEMA"] = (3*sema - 3*sema2) + \
            sema2.ewm(span=long, min_periods=long).mean()

        return result[["SEMA", "LEMA", "DSEMA", "DLEMA", "TSEMA", "TLEMA"]]
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!!
    # Calculation Bollinger Bands
    # https://www.tradingview.com/scripts/bollingerbands/
    # Essentially Bollinger Bands are a way to measure and visualize volatility.
    # As volatility increases, the wider the bands become.
    # Likewise, as volatility decreases, the gap between bands narrows.
    # The higher the volatility, the riskier the securit
    # There are three bands when using Bollinger Bands
    # SMA - Typically set to a 20 day period
    # Upper band - 2 Standard deviations aways from the SMA
    # Lower band - 2 standard devisations aways from the SMA
    # Calculate:
    # Middle Band – 20 Day Simple Moving Average
    # Upper Band – 20 Day Simple Moving Average + (Standard Deviation x 2)
    # Lower Band – 20 Day Simple Moving Average - (Standard Deviation x 2)
#!! INPUT:
    # Ticker data includes Adjust Close Price
    # Time period: time period to be used in calculating the SMA, Upper and Lower Bands.
    # Standard Deviation: number of Std Dev away from the SMA that the Upper and Lower Bands


def BB(data, column=vars.AdjClose, period=20, stdDev=2):
    try:
        result = data.copy()
        result["MidBand"] = result[column].rolling(
            period).mean()  # Simple Moving Average Price
        result["UpBand"] = result["MidBand"] + stdDev * \
            result[column].rolling(period).std(ddof=0)
        result["LowBand"] = result["MidBand"] - stdDev * \
            result[column].rolling(period).std(ddof=0)
        result["BBWidth"] = result["UpBand"] - result["LowBand"]
        return result["MidBand", "UpBand", "LowBand", "BBWidth"]
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None

#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Calculate Average True Range ATR to measure volatility,
#   especially volatility caused by price gaps or limit moves and should not used to
#   indicate the direction of price (because ATR uses absolute price).
#   The higher the ATR value, then the higher the level of volatility.
#   Take the most current period high/low range as well as the previous period close
#   then compared against each others.
#   The Current Period High minus (-) Current Period Low
#   The Absolute Value (abs) of the Current Period High minus (-) The Previous Period Close
#   The Absolute Value (abs) of the Current Period Low minus (-) The Previous Period Close
#   true range = max[(high - low), abs(high - previous close), abs (low - previous close)]
#!! INPUT:
#   Ticker data includes High, Low, Close, Adjust Close
#   Time period to calculate Average True Range (14 days is set by default)


def ATR(data, period=14):
    try:
        result = data.copy()
        result["HTL"] = result[vars.High] - result[vars.Low]
        result["HTPC"] = result[vars.High] - result[vars.AdjClose].shift(1)
        result["LTPC"] = result[vars.High] - result[vars.AdjClose].shift(1)
        result["TR"] = result[["HTL", "HTPC", "LTPC"]].abs().max(axis=1,
                                                                 skipna=False)
        result["ATR"] = result["TR"].ewm(
            span=period, min_periods=period).mean()
        return result["ATR"]
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------



#!!B------------------------------------------------------------------------------------------------------------------------------------
#!!
#!! INPUT:
#!!E------------------------------------------------------------------------------------------------------------------------------------
