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
from vars import contants
import logging
from logging import config
from datetime import date, datetime
from stocktrends import Renko
#!!B-------------------------------------------------------------------------------------------------------------------------------------
#!! Tracker of events that happen when SApp run run_app.
#   Execeptions also will be logged in err_log
#!! INPUT:


def active_logger():

    try:
        config.fileConfig('log.conf')
        # Create logger
        contants.logger = logging.getLogger(contants.the_writer)
        # return vars.logger
    except Exception as e:
        logger = logging.getLogger(contants.the_writer)
        logger.setLevel(logging.DEBUG)
        error_log = logging.FileHandler(contants.error_log)
        error_log.setLevel(logging.ERROR)
        formatter = logging.Formatter(
            contants.logformat, datefmt=contants.datefmt)
        error_log.setFormatter(formatter)
        logger.addHandler(error_log)
        logger.error("Error Type : {}, Error Message : {}".format(
            type(e).__name__, e))
        contants.logger = logger
        # return vars.logger
#!!E-------------------------------------------------------------------------------------------------------------------------------------


# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Fetching data from yahoo finance
#!! INPUT: list of tickers
def get_yfdata(inputs):
    try:
        tickers = inputs[contants.Symbol]

        candle_DF = pd.DataFrame()
        if inputs[contants.xPeriod]:
            period = inputs[contants.Period]
            candle_DF = yf.download(
                tickers, period=period, group_by=tickers, interval=inputs[contants.Interval])
        else:
            start_date = inputs[contants.Start]
            end_date = inputs[contants.End]
            candle_DF = yf.download(
                tickers, start=start_date, end=end_date, group_by=tickers, interval=inputs[contants.Interval])

        candle_DF.dropna(inplace=True)

        # Revert dataframe to get the correct descending sequence
        candle_DF = candle_DF.iloc[::-1]

        renko_DF = candle_DF.copy()

        # Reset index
        candle_DF.reset_index(inplace=True)

        # Rename all columns DataFrame name
        candle_DF.columns = ["Date", "Open", "High",
                             "Low", "Close", "Adj Close", "Volume"]

        if 'Volume' in candle_DF:
            candle_DF["Volume"] = candle_DF["Volume"].map('{:,d}'.format)

        # Round decimal to 2 digits number
        candle_DF = np.round(candle_DF, decimals=2)

        #
        pd.options.display.float_format = '{:, .2f}'.format

        return candle_DF, renko_DF
    except Exception as e:
        contants.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------

# #!!B------------------------------------------------------------------------------------------------------------------------------------
# #!! Average Directional Index (ADX)
# #!! INPUT:
# #!!E------------------------------------------------------------------------------------------------------------------------------------
