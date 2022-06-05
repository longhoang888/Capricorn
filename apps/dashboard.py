# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Dashboard

import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from glov import vars
from util import devf
import logging
from logging import config
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objs as go
import plotly.subplots as ms
#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Display Tabular DataFrame on pretty table
#!! INPUT:


def tableau(data, checkbox=False, theme='material', height=250, pivot=True):
    try:
        gb = GridOptionsBuilder.from_dataframe(data)
        # Pagination setting
        gb.configure_pagination(paginationAutoPageSize=True)
        # Columns setting
        gb.configure_default_column(sorteable=False,
                                    groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)

        gb.configure_column("Date", type=[
            "dateColumnFilter", "customDateTimeFormat"], custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)

        # gb.configure_column("Open", type=["numericColumn","numberColumnFilter", "currencyFormatter"
        #      "customDateTimeFormat"], custom_format_string="{:, .2f}", precision=2)

        # gb.configure_columns(columns_name=["Open", "High", "Close", "Adj Close"], type=[
        #                      "numericColumn", "numberColumnFilter", "customNumericFormat"], custom_format_string="{:, .2f}", precision=2)

        gb.configure_grid_options(domLayout='normal')

        gb.configure_side_bar()
        if checkbox:
            gb.configure_selection("multiple", use_checkbox=checkbox)

        gOps = gb.build()

        gResponse = AgGrid(data, gridOptions=gOps, theme=theme, data_return_mode=DataReturnMode.FILTERED,
                           update_mode=GridUpdateMode.SELECTION_CHANGED, fit_columns_on_grid_load=False,
                           enable_enterprise_modules=pivot, height=height, reload_data=True)
        return gResponse
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Plotting DataFrame with candlestick chart
#!! INPUT:


def candlestick(data, EMA=True, title='', yaxis='Price'):
    try:
        # Candlestick Trace
        candlestick = go.Candlestick(x=data['Date'], open=data['Open'],
                                     high=data['High'], low=data['Low'], close=data['Close'], showlegend=False)

        # Bar Volume Trace
        bar = go.Bar(x=data["Date"], y=data["Volume"],
                     name="Volume", showlegend=False)

        # Create Subplots and plot grid
        fig = ms.make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=True, row_heights=[
                               1, 0.15], vertical_spacing=0)

        # fig = go.Figure(data=[candlestick]

        # Add traces to figure
        fig.add_trace(candlestick, row=1, col=1)
        fig.add_trace(bar, row=2, col=1)
        
        # Update layout
        fig.update_layout(title=title, yaxis_title=yaxis,
                          xaxis_rangeslider_visible=False, height=1150)

        #Update Plot theme
        fig.update_layout(template="ggplot2")

        # Update hovermode and spike line
        fig.update_layout(hovermode="x", hoverdistance=100, spikedistance=1000)

        # Set the background color to white
        fig.update_layout(plot_bgcolor="#FFF", paper_bgcolor="#FFF")

        fig.update_yaxes(type="log")

        # Smooth Candlestick (esclude empty column data in the chart)
        fig.update_xaxes(type="category", categoryorder="category ascending")

        # Delete grid line in sub plots
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        # Set the x axis of the first chart invisible, and colored the x axis of second chart
        fig.update_layout(xaxis=dict(visible=False), xaxis2=dict(linecolor='#BCCCDC'))
        fig.update_layout(yaxis=dict(linecolor='#BCCCDC'), yaxis2=dict(linecolor='#BCCCDC'))

        st.plotly_chart(fig, use_container_width=True)
        return fig
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Plotting DataFrame with various style
#
#!! INPUT:


def splot(data, style=vars.LINE):
    try:
        data.plot()
    except Exception as e:
        vars.logger.error(
            "Error Type : {}, Error Message : {}".format(type(e).__name__, e))
        return None
#!!E------------------------------------------------------------------------------------------------------------------------------------
