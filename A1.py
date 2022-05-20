#Created by: Long Hoang
#Created on: 2022-05-19
#Description: Test Web App built on Streamlit lib
# References:
# 1. https://aroussi.com/post/python-yahoo-finance
# 2. https://docs.streamlit.io/library/api-reference/widgets/st.radio
# 3. https://www.journaldev.com/

#!! IMPORT LIBRARIES    
import numpy as np 
import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import datetime, time
from datetime import date, timedelta

#!! Load image to the web app
image = Image.open('pannel.jpg')

#!! Header
# st.image(image, use_column_width=True)
st.sidebar.write(""" 
# Stock Insight
""")

#!! START_LEFT_GROUP : Add controls on the left side pannel using st.sidebar

#!! Input Stock tickers
ticker_input = "GOOGL"
tickerSymbol = st.sidebar.text_input("Enter Stock Symbol", ticker_input, 5,)
tickerSymbol = tickerSymbol.strip() #remove leading and trailing spaces.
exe = 'xGox'
if tickerSymbol.isspace() or tickerSymbol == '' or tickerSymbol.isnumeric():
    exe = 'noGo'
    st.sidebar.error('Please enter ticker !!!')

#!! Select options
st.sidebar.header('How would you like to gather the data?')
history_option = st.sidebar.radio(
     "Select the below options:",
     ('Period', 'Time Interval'))
#!! Input the period
period_option = st.sidebar.selectbox( 'Data period to download', 
                            ('Weekly', 'Monthly', '3 months', '6 months' ,'1 year', '2 years', '5 years'), index=0)

period = {
    period_option == 'Weekly'    : '5d',
    period_option == 'Monthly'   : '1mo',
    period_option == '3 months'  : '3mo',
    period_option == '6 months'  : '6mo',
    period_option == '1 year'    : '1y',
    period_option == '2 years'   : '2y',
    period_option == '5 years'   : '5y',
}

period_v = period.get(1)

st.sidebar.write('You selected:', period_option)

#!! Input start and end date
today = date.today()
last4day =  today - timedelta(5)
#yesterday = today- timedelta(1)
start_date = st.sidebar.date_input("Start Date:", datetime.date(last4day.year, last4day.month, last4day.day))
end_date = st.sidebar.date_input("End Date: ", today)

#!! END_LEFT_GROUP

#!! MAIN : Main process
if exe != 'noGo' :

    #!! Get Stock info   
    tickerData = yf.Ticker(tickerSymbol)
    #st.write(tickerData.info)
    if history_option == 'Period':
        tickerDf = tickerData.history(period=period_v)
    else:
        period_v = ''
        tickerDf = pd.DataFrame(tickerData.history(period=period_v, start=start_date, end=end_date))

    #!! Inform user if no data found
    if tickerDf.empty :
        st.error('No data found. Please check your ticker and time interval.')
    else:
        # with st.spinner('Wait for it...'):
        #     time.sleep(5)
        # st.success('Done!')
        #st.markdown("<h1 style='text-align: left; color: red;'>Some title</h1>", unsafe_allow_html=True)
        # with st.empty():
        #     st.table(tickerData.info)
        st.dataframe(tickerDf, width=1000)
        st.write("""  **Close Price**""")
        st.line_chart(tickerDf.Close)
        st.write(""" **Volume** """)
        st.line_chart(tickerDf.Volume)
        