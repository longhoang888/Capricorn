# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Left pannel user input components

import streamlit as st
import datetime
import time
from datetime import date, timedelta
from vars import contants, messages as msg

#!!B-----------------------------------------------------------------------------------------------------------------------------------
#!! Add sidebar components
#!! INPUT:


def add():
    try:
        inputs = {}
        st.sidebar.title('S+')
        # st.sidebar.header('Quantitative trading')

        #!! START_LEFT_GROUP : Add controls on the left side pannel using st.sidebar

        #!! Input Stock tickers
        ticker_input = contants.ini_Symbol
        tickerSymbol = st.sidebar.text_input(
            "Enter Stock Symbol", ticker_input, 5,)
        # remove leading and trailing spaces.
        tickerSymbol = tickerSymbol.strip()
        #!! add running option to list
        inputs[contants.F8] = contants.Run
        if tickerSymbol.isspace() or tickerSymbol == '' or tickerSymbol.isnumeric():
            inputs[contants.F8] = contants.noGO
            st.sidebar.error(msg.E002)

        #!! add ticker to the list
        inputs[contants.Symbol] = tickerSymbol

        #!! Select options
        st.sidebar.header('How would you like to gather the data?')
        history_option = st.sidebar.radio(
            "Select the below options:",
            ('Period', 'Date'))

        #!! add time interval
        if history_option == 'Period':
            inputs[contants.xPeriod] = True
            #!! Input the period
            period_option = st.sidebar.selectbox('Data period to download',
                                                 ('Weekly', 'Monthly', '3 months',
                                                  '6 months', '1 year', '2 years', '5 years'),
                                                 index=0)

            period_t = {
                period_option == 'Weekly': '5d',
                period_option == 'Monthly': '1mo',
                period_option == '3 months': '3mo',
                period_option == '6 months': '6mo',
                period_option == '1 year': '1y',
                period_option == '2 years': '2y',
                period_option == '5 years': '5y',
            }
            period = period_t.get(1)

            p_days = {
                period == '5d': 5,
                period == '1mo': 22,
                period == '3mo': 66,
                period == '6mo': 132,
                period == '1y': 264,
                period == '2y': 528,
                period == '5y': 1320

            }
            st.sidebar.write('You selected:', period_option)

            #!! add period into list
            inputs[contants.Period] = period
            contants.days = p_days.get(1)
        else:
            inputs[contants.xPeriod] = False
            #!! start and end date
            today = date.today()
            last4day = today - timedelta(5)
            start_date = st.sidebar.date_input("Start Date:", last4day,
                                               max_value=today)  # - timedelta(1))
            end_date = st.sidebar.date_input(
                "End Date: ", today, min_value=start_date, max_value=today)
            inputs[contants.Start] = start_date
            inputs[contants.End] = end_date

        #!! Adding global variables
        st.sidebar.write("""
            ## Time interval
            """)
        inter_ops = st.sidebar.selectbox('', ('15 minutes', 'Hour', 'Day',
                                              'Week', 'Month'),
                                         index=0)
        inputs[contants.Interval] = {inter_ops == '15 minutes': '15m',
                                     inter_ops == 'Hour': '1h',
                                     inter_ops == 'Day': '1d',
                                     inter_ops == 'Week': '1wk',
                                     inter_ops == 'Month': '1mo'
                                     }.get(1)
        #!! reuturn input list
        return inputs
    except Exception as e:
        contants.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None

#!!E-----------------------------------------------------------------------------------------------------------------------------------
