# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Stock Insight App

import json
import logging
import matplotlib as plt
import numpy as np
import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import datetime
import time
from datetime import date, timedelta
from utils import feeder, logger, ploter
from apps import sidebar, header
from vars import contants, messages as msg
from strategy import indicators


#!! Load image to the web app
# icon = Image.open('icon.jpg')
# st.image(icon, use_column_width=True)


#!! Set layout wide
st.set_page_config(page_title=contants.page_title, layout=contants.page_layout)

#!! Activate Logger
logger = logger.Log.active()

#!!B-----------------------------------------------------------------------------------------------------------------------------------
#!! Application Executor
#!! INPUT: NONE


def main():

    try:
        #!! Get user input
        inputs = sidebar.add()
        if inputs[contants.F8] != contants.noGO:
            #!! Get stock infor
            candle_df, renko_df = feeder.get_yfdata(inputs)
            if candle_df.empty:
                st.error(msg.E001)
            else:
                # header.add(inputs[vars.Symbol])
                # st.write("Historical Data")
                # db.tableau(candle_df, height=650)
                # db.candlestick(candle_df, title=inputs[vars.Symbol])
                # input_renko = inputs
                # input_renko[vars.Interval] = '1h'
                # input_renko[vars.Period] = '1y'
                # input_renko[vars.xPeriod] = True
                # hour_df, raw_df = devf.get_yfdata(input_renko)
                # renko_chart = devf.renko_convertion(renko_df, hour_df)
                # db.renko(renko_chart)
                renko = indicators.renko(renko_df)
                ploter.tableau(renko)
                st.write('Data source: **Yahoo Finance**')
    except Exception as e:
        logger.write(e)
#!!E-----------------------------------------------------------------------------------------------------------------------------------


#!! run web app
if __name__ == '__main__':
    main()

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!!
#!! INPUT:
#!!E------------------------------------------------------------------------------------------------------------------------------------
