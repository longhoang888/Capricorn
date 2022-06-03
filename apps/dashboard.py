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

#!!B------------------------------------------------------------------------------------------------------------------------------------
#!!
#!! INPUT:


def tableau(data, checkbox=False, theme='material', height=350, pivot=True):
    try:
        gb = GridOptionsBuilder.from_dataframe(data)
        # Pagination setting
        gb.configure_pagination(paginationAutoPageSize=True)
        # Columns setting
        gb.configure_default_column(
            groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=True)
        
        gb.configure_column("Datetime", header_name="Date Time", type=[
                                "dateColumnFilter", "customDateTimeFormat"],custom_format_string='yyyy-MM-dd HH:mm zzz', pivot=True)

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
