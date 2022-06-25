<<<<<<< HEAD
# python-streamlit

This project is built on yfinance, an open source API to access the financial data available on Yahoo Finance.
As mentioned, this free API has no guarantee if it breaks it will be maintained.
This project mainly discover the solutions and get a touch to the financial python world.
Polygon and IEX might make good bets in future for the platform.

https://www.alphavantage.co/documentation/
https://algotrading101.com/learn/iex-api-guide/
https://algotrading101.com/learn/yfinance-guide/
https://polygon.io/
Link to stocktrend github page

https://github.com/ChillarAnand/stocktrends

Links to sources discussed in the lecture videos

TA-Lib website: http://ta-lib.org/
TA-Lib Python Wrapper Github Page: https://mrjbq7.github.io/ta-lib/
TA-Lib documentation of pattern recognition: https://mrjbq7.github.io/ta-lib/func_groups/pattern_recognition.html
Discussion on installation problems: https://github.com/mrjbq7/ta-lib/issues/127
Command to install TA-lib for python 3.5 and 3.6: pip install -i https://pypi.anaconda.org/masdeseiscaracteres/simple ta-lib
Good website on chart patterns: http://thepatternsite.com

Project LEO

Libraries: streamlit, yfinance, pnadas, numpy, mplfinance, stocktrends, talib
=======
# Capricorn
Project Capricorn 
Libraries: streamlit, yfinance, pnadas, numpy
>>>>>>> 7274c02307a166a2772935ecf76f2b0f603b9d3e

pip install streamlit

pip install pipenv

streamlit run app.py

pip install pipwin
pipwin install TA-Lib
https://www.lfd.uci.edu/~gohlke/pythonlibs/#ta-lib

To fix the issue with mplexporter not getting Collection offset position due to matplotlib API changes in v3.5
(https://github.com/plotly/plotly.py/issues/3624
replacing in this exporter.py file
offset_order = offset_dict[collection.get_offset_position()]
offset_order = offset_dict[collection._offset_position] ) -->not working

I have decided to uninstall matplotlib 3.5 and downgrade it to 3.4.0 to fix the issue

from st_aggrid import AgGrid
