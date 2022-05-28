#Created by: Long Hoang
#Created on: 2022-05-19
#Description: Stock Insight App
# References:
# 1. https://aroussi.com/post/python-yahoo-finance
# 2. https://docs.streamlit.io/library/api-reference/widgets/st.radio
# 3. https://www.journaldev.com/
# 4. https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.from_dict.html
# 5. https://site.financialmodelingprep.com/developer/docs/company-key-metrics-api

#!! IMPORT LIBRARIES    
import json
import logging
import matplotlib as plt
import numpy as np 
import yfinance as yf
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image
import datetime, time
from datetime import date, timedelta
from util import devf
from apps import sidebar, header
from glov import vars

#!! Load image to the web app
image = Image.open('pannel.jpg')
# st.image(image, use_column_width=True)


#!! MAIN : Main process

#!! Set layout wide
st.set_page_config(page_title="S+", layout="wide")

def main():

    #!! Get user input
    inputs = sidebar.add()
    if inputs[vars.F8] != vars.noGO :
        #!! Get stock infor   
        tickerDf = devf.get_yfdata(inputs)
        if tickerDf.empty :
            st.error('No data found. Please check your ticker and time interval.')
        else:
            header.add(inputs[vars.Symbol])
            st.dataframe(tickerDf)
            devf.quands(tickerDf)

          


#!! run web app         
main()  