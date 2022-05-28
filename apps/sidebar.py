# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Left pannel user input components

import streamlit as st
import datetime
import time
from datetime import date, timedelta
from glov import vars

#!! Add sidebar components


def add():
    inputs = {}
    st.sidebar.title('S+')
    # st.sidebar.header('Quantitative trading')

    #!! START_LEFT_GROUP : Add controls on the left side pannel using st.sidebar

    #!! Input Stock tickers
    ticker_input = vars.ini_Symbol
    tickerSymbol = st.sidebar.text_input(
        "Enter Stock Symbol", ticker_input, 5,)
    tickerSymbol = tickerSymbol.strip()  # remove leading and trailing spaces.
    #!! add running option to list
    inputs[vars.F8] = vars.Run
    if tickerSymbol.isspace() or tickerSymbol == '' or tickerSymbol.isnumeric():
        inputs[vars.F8] = vars.noGO
        st.sidebar.error('Please enter ticker !!!')

    #!! add ticker to the list
    inputs[vars.Symbol] = tickerSymbol

    #!! Select options
    st.sidebar.header('How would you like to gather the data?')
    history_option = st.sidebar.radio(
        "Select the below options:",
        ('Period', 'Date'))

    #!! add time interval
    if history_option == 'Period':
        inputs[vars.xPeriod] = True
        #!! Input the period
        period_option = st.sidebar.selectbox('Data period to download',
                                             ('Weekly', 'Monthly', '3 months', '6 months', '1 year', '2 years', '5 years'), index=0)

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
        inputs[vars.Period] = period
        vars.days = p_days.get(1)
    else:
        inputs[vars.xPeriod] = False
        #!! start and end date
        today = date.today()
        last4day = today - timedelta(5)
        start_date = st.sidebar.date_input("Start Date:", datetime.date(
            last4day.year, last4day.month, last4day.day))
        end_date = st.sidebar.date_input("End Date: ", today)
        inputs[vars.Start] = start_date
        inputs[vars.End] = end_date

        i_days = (end_date-start_date).days
        vars.days = i_days

    #!! Adding global variables
    max1 = vars.days // 5 + 1
    vars.time_window = st.sidebar.slider(
        'Analysis Time-window:', min_value=1, max_value=max1) # help="Calculate rolling and exponential values (day)")
    #!! reuturn input list
    return inputs
