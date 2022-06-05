# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Ticker Trading Data

import streamlit as st
import datetime
import time
import yfinance as yf
import numpy as np
import pandas as pd
from datetime import date, timedelta
from glov import vars
from util import devf
import xlwt

#!!B-----------------------------------------------------------------------------------------------------------------------------------
#!! Header
#!! INPUT:ticker


def add(ticker):
    try:
        #!! Get Stock info
        tickerData = yf.Ticker(ticker)
        #!! Convert ticker data into list and transpose list into data frame
        tickerData_list = list(tickerData.info.items())
        tickerData_df = pd.DataFrame(tickerData_list)
        tickerData_df.replace("", np.nan, inplace=True)
        tickerData_df.dropna(inplace=True)
        tickerData_df.columns = ['label', 'values']
        tickerData_out = tickerData_df
        tickerData_df.set_index('label', inplace=True)

        # tickerData_out["label"] = tickerData_df["label"].capitalize()

        #!! Company name
        longName = tickerData_df.at['longName', 'values']
        st.title(longName)
        hcol1, hcol2, hcol3, hcol4, hcol5 = st.columns(5)
        with hcol1:
            value = tickerData_df.at["volume", "values"]
            delta = tickerData_df.at["averageVolume", "values"]
            st.metric("Trade Volume", value=value,
                      delta=delta)
        with st.expander("Learn more"):
            busiSum = tickerData_df.at['longBusinessSummary', 'values']
            st.write(busiSum)
            csv = tickerData_out.to_csv().encode('utf-8')
            #!! Summary info
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(tickerData.balancesheet)
                # shortRatio = tickerData_df.at["shortRatio", "values"]
                # # st.metric("Short Ratio", value=shortRatio,delta=50, delta_color="inverse")

            st.download_button("Download data to excel", data=csv,
                               file_name=ticker + "_quote_" + str(date.today()) + ".csv")
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E-----------------------------------------------------------------------------------------------------------------------------------
