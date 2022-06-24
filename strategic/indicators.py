# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Utility functions

from asyncio import exceptions
from time import strftime
import matplotlib as plt
from matplotlib.pyplot import axes, subplot
import numpy as np
import yfinance as yf
import streamlit as st
import pandas as pd
from glov import contants
import logging
from logging import config
from datetime import date, datetime
from stocktrends import Renko
#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Calculate Technical Indicator MACD https://www.tradingview.com/scripts/
    #   MACD Line: (12-day EMA - 26-day EMA)
    #   Signal Line: 9-day EMA of MACD Line
    #   MACD Histogram: MACD Line - Signal Line
#!! INPUT: ticker data includes Adj Close


def MACD(data, column=contants.AdjClose, fast=12, slow=26, smooth=9):
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
        contants.logger.error(
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
def EMA(data, column=contants.AdjClose, short=20, long=60):
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

        result = np.round(result, decimals=2)

        # return result[["SEMA", "LEMA", "DSEMA", "DLEMA", "TSEMA", "TLEMA"]]
        return result
    except Exception as e:
        contants.logger.error(
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


def BB(data, column=contants.AdjClose, period=20, stdDev=2):
    try:
        result = data.copy()
        result["MidBand"] = result[column].rolling(
            period).mean()  # Simple Moving Average Price
        result["UpBand"] = result["MidBand"] + stdDev * \
            result[column].rolling(period).std(
                ddof=0)  # calculate StdDev of population (ddof = 0)
        result["LowBand"] = result["MidBand"] - stdDev * \
            result[column].rolling(period).std(ddof=0)
        result["BBWidth"] = result["UpBand"] - result["LowBand"]
        return result["MidBand", "UpBand", "LowBand", "BBWidth"]
    except Exception as e:
        contants.logger.error(
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
        result["HTL"] = result[contants.High] - result[contants.Low]
        result["HTPC"] = result[contants.High] - result[contants.AdjClose].shift(1)
        result["LTPC"] = result[contants.High] - result[contants.AdjClose].shift(1)
        result["TR"] = result[["HTL", "HTPC", "LTPC"]].abs().max(axis=1,
                                                                 skipna=False)
        result["ATR"] = result["TR"].ewm(
            span=period, min_periods=period).mean()
        result.dropna(inplace=True)
        return result[["Date","ATR"]]
    except Exception as e:
        contants.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
# Relative Strength Index - RSI measures the velocity (speed) and magnitude of directional price movements
# Using the closing price over specified trading period
# RSI = 100 - 100 / (1+RS)
# RS = Average Gain of n days UP / Average Loss of n days DOWN
# change = change(close)
# gain = change >= 0 ? change : 0.0
# loss = change < 0 ? (-1) * change : 0.0
# avgGain = rma(gain, 14)
# avgLoss = rma(loss, 14)
# rs = avgGain / avgLoss
# rsi = 100 - (100 / (1 + rs))
# "rsi", above, is exactly equal to rsi(close, 14).
# RSI above 70 - overbought and RSI <30 oversold.
# 30 < RSI < 70  Neutral
# Bullish RSI Divergence – When price makes a new low but RSI makes a higher low.
# Bearish RSI Divergence – When price makes a new high but RSI makes a lower high.
# Wilder believed that Bearish Divergence creates a selling opportunity while Bullish Divergence creates a buying opportunity.
# #!! INPUT:
# # RSI Length  = 14
# # MA Type = SEMA
# # MA Length =  14
# # BB StdDev = 2


def RSI(data, length=14):
    try:
        result = data.copy()
        result["Change"] = result["Adj Close"] - result["Adj Close"].shift(-1)
        result["Gain"] = np.where(result["Change"] > 0, result["Change"], 0)
        result["Loss"] = np.where(result["Change"] < 0, -1*result["Change"], 0)
        result["avgGain"] = result["Gain"].ewm(
            alpha=1/length, min_periods=length).mean()
        result["avgLoss"] = result["Loss"].ewm(
            alpha=1/length, min_periods=length).mean()
        result["rs"] = result["avgGain"] - result["avgLoss"]
        result["RSI"] = 100 - (100 / (1 + result["rs"]))
        return result[["Date", "RSI"]]
    except Exception as e:
        contants.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
# #!!E------------------------------------------------------------------------------------------------------------------------------------

# #!!B------------------------------------------------------------------------------------------------------------------------------------
# #!! Average Directional Index (ADX)
# # Determine the strength of trend
# +DI - Positive Directional Indicator
# -DI Negative Directional Indicator
# Start off by calculating the +DM, -DM, and True Range (TR) for each period you are analyzing. Note:
# +DM = Current High - Previous High
# -DM = Previous Low - Current Low
# Use +DM when +DM > -DM; Use -DM when -DM > +DM
# TR is the greater of the Current High - Current Low, the Current High - Previous Close, or the Current Low - Previous Close
# Smooth your period averages of +DM, -DM, and TR. Then, insert the -DM and +DM values to calculate the smoothed averages of those.
# First xTR = Sum of first x TR readings (x = number of…)
# Next xTR value = First xTR - (Prior xTR/14) + Current TR
# Then divide the smoothed +DM value by the smoothed TR value to get your +DI value. Multiply this value by 100.
# Divide the smoothed -DM value by the smoothed TR value to get your -DI value. Multiply this value by 100.
# Directional Movement Index (DX) is +DI minus -DI, then divided by the sum of +DI and -DI (all of these are absolute values). Multiply by 100.
# To get the ADX, calculating the DX values for x periods. Smooth the results of the periods in order to get your ADX value.
# First ADX = the sum of x periods of DX / x
# Finally, ADX = ((Prior ADX * 13) + Current DX) / x
# prices move up (when +DI is above -DI), and when the prices move down (when -DI is above +DI)
# Crosses between both +DI and -DI lines, it can signify potential trading signals, as a bearish or bullish market emerges.
# Trend < 20 : should not enter the market
# Trend < 25 :confusing - potential for money loss high
# 25< Trend < 75: strong
# Trend > 75: extremely strong
# https://www.tradingview.com/scripts/directionalmovement/?solution=43000502250
# #!! INPUT:


def ADX(data, period=14):
    try:
        result = data.copy()
        result["ATR"] = ATR(data, period=period)
        result["Up"] = result["High"] - result["High"].shift(-1)
        result["Down"] = result["Close"].shift(-1) - result["Close"]
        result["+DM"] = np.where(((result["Up"] < result["Down"])
                                  & result["Up"] > 0), result["Up"], 0)
        result["-DM"] = np.where(((result["Down"] < result["Up"])
                                  & result["Down"] > 0), result["Down"], 0)
        result["+DI"] = 100 * (result["+DM"] / result["ATR"]
                               ).ewm(com=period, min_period=period).mean()
        result["-DI"] = 100 * (result["-DM"] / result["ATR"]
                               ).ewm(com=period, min_period=period).mean()
        result["ADX"] = 100 * abs((result["+DI"] - result["-DI"]) / (
            result["+DI"] + result["-DI"])).ewm(com=period, min_period=period).mean()
        return result[["Date", "ADX"]]
    except Exception as e:
        contants.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
# #!!E------------------------------------------------------------------------------------------------------------------------------------

# #!!B------------------------------------------------------------------------------------------------------------------------------------
# #!! RENKO: idicate trend with by building a serie of brick (45 degree). The time axis is not fixed in Renko chart.
# A box size (brick size) typically 3$, 5$ filter out the noise  (all the moements that are smaller than the box size are filtered out)
# Renko chart uses on the closing prices.
# Renko chart on draws upside box when the price reachs to box size and downside box when the price down 2x box size.
# #!! INPUT:


def renko_convertion(data, hourly_data, period=120, atr_length=3):
    try:

        #Calculate ATR
        atr_df = ATR(hourly_data, period)
        atr_df = round(atr_df, 0)
        atr_df.reset_index(inplace=True)
        value = atr_df.iloc[0:1]["ATR"]

        candle_df = data.copy()
        candle_df.drop('Close', axis=1, inplace=True)
        candle_df.reset_index(inplace=True)
        candle_df.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        renko = Renko(candle_df)
        
        # renko.brick_size = atr_length * round(ATR(hourly_data, period).iloc(-1),0)
        renko.brick_size = atr_length * value
        renko_data = renko.get_ohlc_data()
        return renko_data, renko.brick_size
    except Exception as e:
        contants.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None

# #!!E------------------------------------------------------------------------------------------------------------------------------------


# #!!B------------------------------------------------------------------------------------------------------------------------------------
# #!! Average Directional Index (ADX)
# #!! INPUT:
# #!!E------------------------------------------------------------------------------------------------------------------------------------
