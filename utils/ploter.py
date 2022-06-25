# Created by: Long Hoang
# Created on: 2022-05-19
# Description: painter

from turtle import color
import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode
from vars import contants
from strategy import indicators
import logging
from logging import config
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.subplots as ms
import plotly.tools as tls
import plotly.express as px
from datetime import datetime
import mplfinance as mpl
#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Display Tabular DataFrame on pretty table
#!! INPUT:


def tableau(data, checkbox=False, theme='material', height=250, pivot=False):
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
        raise e
#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Plotting DataFrame with candlestick chart
#!! INPUT:


def plot_candlestick(data, EMA=True, title='', yaxis='Price'):
    try:
        # Candlestick Trace
        candlestick = go.Candlestick(x=data['Date'], open=data['Open'],  # name="Trading Price",
                                     high=data['High'], low=data['Low'], close=data['Close'], showlegend=False)

        #  Add EMA line chart to candlestick
        if EMA:
            ema_data = indicators.EMA(data, short=50, long=100)[
                ["Date", "TSEMA", "TLEMA"]].dropna()
            # ema_data_60 = devf.EMA(data, short=60)[["Date", "DSEMA"]].dropna()
            # st.write(ema)
            ema_line_20 = go.Scatter(
                x=ema_data['Date'], y=ema_data['TSEMA'], showlegend=False)
            ema_line_60 = go.Scatter(
                x=ema_data['Date'], y=ema_data['TLEMA'], showlegend=False)

        # Bar Volume Trace
        # Add color code for volume chart
        # Closing price of the current bar is higher than that of the previous bar
        # The volume bar will be green in colour. Else it will be red
        data["PreClose"] = data["Adj Close"].shift(-1)
        data.fillna(method='ffill', inplace=True)

        data["Color"] = ""
        data["Color"] = ['#9fccb8' if (x >= y) else t for x, y, t in zip(
            data["Close"], data["PreClose"], data["Color"])]
        # data["Line"] = ['#479c79' if (x >= y) else t for x, y, t in zip(
        #     data["Close"], data["PreClose"], data["Line"])]
        data["Color"] = ['#ffa09a' if (x < y) else t for x, y, t in zip(
            data["Close"], data["PreClose"], data["Color"])]
        # data["Line"] = ['#fd6c63' if (x < y) else t for x, y, t in zip(
        #     data["Close"], data["PreClose"], data["Line"])]
        bar = go.Bar(x=data["Date"], y=data["Volume"],
                     name="Volume", showlegend=False, marker={'color': data['Color']})
        #  marker_line=dict(width=2, color=data["Line"]))

        # Create Subplots and plot grid
        fig = ms.make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=True, row_heights=[
                               0.5, 0.05], vertical_spacing=0)

        # fig = go.Figure(data=[candlestick])

        # Add traces to figure
        fig.add_trace(candlestick, row=1, col=1)
        fig.add_trace(ema_line_20, row=1, col=1)
        fig.add_trace(ema_line_60, row=1, col=1)
        fig.add_trace(bar, row=2, col=1)

        # Update layout
        fig.update_layout(title=title, yaxis_title=yaxis,
                          xaxis_rangeslider_visible=False, height=1000)

        # Update Plot theme
        fig.update_layout(template="ggplot2")

        # Update hovermode and spike line
        # , hoverdistance=1000, spikedistance=1000)
        fig.update_layout(hovermode="x")

        # Set the background color to white
        fig.update_layout(plot_bgcolor="#FFF", paper_bgcolor="#FFF")

        fig.update_yaxes(type="log")

        # Smooth Candlestick (esclude empty column data in the chart)
        fig.update_xaxes(type="category", categoryorder="category ascending")

        # Delete grid line in sub plots
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)

        # Set the x axis of the first chart invisible, and colored the x axis of second chart
        fig.update_layout(xaxis=dict(visible=False),
                          xaxis2=dict(linecolor='#BCCCDC'))
        fig.update_layout(yaxis=dict(linecolor='#BCCCDC'),
                          yaxis2=dict(linecolor='#BCCCDC'))

        # Hide ticklabel and tick on second plot
        fig.update_layout(yaxis2=dict(showticklabels=False, ticks=""))

        # Active spikeline
        fig.update_traces(xaxis="x1")  # make the spike line acrros both charts

        fig.update_xaxes(showspikes=True, spikethickness=2,
                         spikedash="dot",
                         spikecolor="#999999",
                         spikemode="across")
        fig.update_yaxes(showspikes=True, spikethickness=2,
                         spikedash="dot",
                         spikecolor="#999999",
                         spikemode="across")

        # # Remove floating menu and unnecesary dialog box
        # fig = fig.show(config={"displayModeBar": False, "showTips": False})

        st.plotly_chart(fig, use_container_width=True)
        return fig
    except Exception as e:
        raise e
#!!E------------------------------------------------------------------------------------------------------------------------------------

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!! Plotting DataFrame with various style
#
#!! INPUT:


def plot_renko(data, **kwargs):
    try:
        # # renko_data = data.copy()
        # # renko_data.reset_index(drop=True, inplace=True)
        # # renko_data.set_index('Date', inplace=True)
        # # renko_data.drop(["PreClose", "Color"], axis=1, inplace=True)
        # for key, value in kwargs.items():
        #     if key == 'size':
        #         size = value
        #     if key == 'atr':
        #         atr = True
        #     if key == 'atr_length':
        #         atr_length = value
        # fig, ax = mpl.plot(data, type="renko", style='yahoo', figsize=(
        #     15, 10), returnfig=True)  # , volume=True)
        # # plotly_fig = tls.mpl_to_plotly(fig)
        # # st.plotly_chart(plotly_fig, use_container_width=True)
        # st.pyplot(fig)
        # return fig
        # data_df = data.copy()
        data.columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        # def format_timestamp(x): return x.strftime("%d/%m %H:%M")
        # timestamps = data['date'].apply(format_timestamp)
        fig = go.Figure(data=[go.Candlestick(x=data['date'], open=data['open'], high=data[["open", "close"]].max(
            axis=1), low=data[["open", "close"]].min(axis=1), close=data['close'], name='Historical Data')])
        st.plotly_chart(fig, use_container_width=True)
        return fig
    except Exception as e:
        raise e
#!!E------------------------------------------------------------------------------------------------------------------------------------
