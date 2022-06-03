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
from util import devf
from apps import sidebar, header, dashboard as db
from glov import vars, messages as msg
from st_aggrid import AgGrid


#!! Load image to the web app
# icon = Image.open('icon.jpg')
# st.image(icon, use_column_width=True)


#!! Set layout wide
st.set_page_config(page_title=vars.page_title, layout=vars.page_layout)

#!! Activate Logger
devf.active_logger()

#!!B-----------------------------------------------------------------------------------------------------------------------------------
#!! Application Executor
#!! INPUT: NONE


def main():

    try:
        #!! Get user input
        inputs = sidebar.add()
        if inputs[vars.F8] != vars.noGO:
            #!! Get stock infor
            history_df = devf.get_yfdata(inputs)
            if history_df.empty:
                st.error(msg.E001)
            else:
                header.add(inputs[vars.Symbol])
                st.write("Historical Data")
                db.tableau(history_df, height=650)

                # # adding EMA
                # tickerDf[["SEMA", "LEMA", "DSEMA", "DLEMA",
                #           "TSEMA", "TLEMA"]] = devf.EMA(tickerDf)
                # df = pd.DataFrame()
                # df = tickerDf
                # AgGrid(df)
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
#!!E-----------------------------------------------------------------------------------------------------------------------------------


#!! run web app
if __name__ == '__main__':
    main()

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!!
#!! INPUT:
#!!E------------------------------------------------------------------------------------------------------------------------------------
