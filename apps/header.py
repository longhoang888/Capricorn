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

def add(ticker):
    st.write('Data source: **Yahoo Finance**')
    #!! Get Stock info
    tickerData = yf.Ticker(ticker)

    #!! Convert ticker data into list and transpose list into data frame
    tickerData_list = list(tickerData.info.items())
    tickerData_df = pd.DataFrame(tickerData_list)
    tickerData_df.replace("", np.nan, inplace=True)
    tickerData_df.dropna(inplace=True)
    tickerData_df.columns = ['label', 'values']
    tickerData_df.set_index('label', inplace=True)
    # np_array = np.array(tickerData_list)
    # tickerData_trans_list = np_array.T.tolist()
    # tickerData_df = pd.DataFrame( tickerData_trans_list, columns=tickerData_trans_list[0])
    # tickerData_df = tickerData_df[1:]
    # tickerData_df.dropna(axis=1, inplace=True)
    
    #!! Company name
    longName = tickerData_df.at['longName', 'values']
    st.title(longName)
    with st.expander("Learn more"):
        busiSum = tickerData_df.at['longBusinessSummary', 'values']
        st.write(busiSum)

    # st.write(tickerData_df)

    # st.markdown(f"Company name: {cname}")
    # with st.container():
    # st.write(tickerData_df[["longName"]])
    # st.dataframe(tickerData_df)
