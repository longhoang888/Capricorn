# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Utility functions
# References:
# 1. https://aroussi.com/post/python-yahoo-finance
# 2. https://docs.streamlit.io/library/api-reference/widgets/st.radio
# 3. https://www.journaldev.com/
# 4. https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html
# 5. https://site.financialmodelingprep.com/developer/docs/company-key-metrics-api

from time import strftime
import matplotlib as plt
import numpy as np
import yfinance as yf
import streamlit as st
import pandas as pd
from glov import vars



@st.cache(suppress_st_warning=True)

#!! Define custome functions
#!! Get yahoo finance data method
def get_yfdata(inputs):
    tickers = inputs[vars.Symbol]
 
    yfdata_DF = pd.DataFrame()
    if inputs[vars.xPeriod]:
        period = inputs[vars.Period]
        yfdata_DF = yf.download(tickers, period=period, group_by=tickers)
    else:
        start_date = inputs[vars.Start]
        end_date = inputs[vars.End]
        yfdata_DF = yf.download(tickers, start=start_date, end=end_date, group_by=tickers)
    yfdata_DF.fillna(0, inplace=True)
    yfdata_DF.dropna(inplace=True)
    yfdata_DF.reset_index(inplace=True)
    yfdata_DF["Date"] = yfdata_DF["Date"].dt.strftime("%Y-%m-%d")
    yfdata_DF.set_index("Date",inplace=True)
    return yfdata_DF.sort_values('Date', ascending=False)  # return DF without NA


#!!
def quands(rQDF):

    alist = {}
#!! Get different data from given period of time
#!! dataChange = df[n] / df[n-1] - 1) 
#!! dataChange = df / df.shift(1) -1 
    #!! Return data over period
    returns = rQDF.pct_change()
    returns.dropna(inplace=True)
    if not returns.empty :
        alist["return"] = returns
    # st.write ("Return value for entered period")
    # st.write(returns)
    # alist.append(returns)
    # st.area_chart(returns)
    # returns_mean = returns.mean()
    # st.write(returns_mean)
    # returns_std = returns.std() # risk level vs. avarage return

    #!! Calculate simple moving average
    rolling_return = returns.rolling(window=5)
    s_mean = rolling_return.mean()
    s_mean.dropna(inplace=True)
    if not s_mean.empty :
        alist["savg"] = s_mean
        # st.write("Rolling moving average")
        # st.write (s_mean)

    #!! Calculate exponential moving avarage    
    ewm_returns = returns.ewm(com=vars.time_window, min_periods=5)
    e_mean = ewm_returns.mean()
    e_mean.dropna(inplace=True)
    if not e_mean.empty:
        alist["eavg"] = e_mean
        # st.write("Exponential moving average")
        # st.write(e_mean)
    
    return alist
