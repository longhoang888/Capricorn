import numpy as np
import matplotlib
import sys
# https://numpy.org/doc/stable/user/quickstart.html

import pandas as pd
import plotly

import plotly.graph_objs as go
import plotly.subplots as ms
import plotly.express as pe

from datetime import datetime


# a = np.arange(4).reshape(2, 2)

# df = pd.DataFrame(a)


# df.columns = ["x", "y"]
# df["c"] = ""
# df["c"] = ["red" if (x > y) else t for x, y,
#            t in zip(df["x"], df["y"], df["c"])]
# df["c"] = ["green" if (x < y) else t for x, y,
#            t in zip(df["x"], df["y"], df["c"])]
# print(df)

# colors = df.c.tolist()
# df['p'] = [colors[0]]+colors[:(len(colors)-1)]
# df.loc[((df.x == df.y) & (df.c == '')), 'c'] = [z for x, y, z, t in zip(
#     df['x'], df['y'], df['p'], df['c']) if (x == y and t == '')]


# print(colors)
# print(df)
# help(go.Bar)

# y = np.array([10, 12, 15, 19, 28, 25, 31, 33, 43])
# color = np.array(['rgb(255,255,255)']*y.shape[0])
# color[y < 20] = 'rgb(204,204, 205)'
# color[y >= 20] = 'rgb(130, 0, 0)'

# data = [dict(type='bar',
#              y=y,
#              marker=dict(color=color.tolist())
#              )]
# print(df)
# chart_data = df[["x","y"]]

# a = [("2022-06-10T16:45", 2218.61905864), ("2022-06-13T14:45", 2219.1703486), ("2022-06-10T16:00", 2217.49397467)]
# line_data = pd.DataFrame(a)
# line_data.columns = ["x", "y"]
# print(line_data)
# fig = pe.line(line_data, x= line_data["x"],y=line_data["y"],render_mode='auto')
# fig.show()
# fig = pe.line(chart_data,x=chart_data["x"], y =chart_data["y"])
# fig.show()
# print(chart_data)
date_rng = pd.date_range(start='1/6/2022', end=datetime.today(), freq='H')
df = pd.DataFrame(date_rng, columns=['date'])
df['data'] = np.random.randint(0,100,size=len(date_rng))
fig = pe.line(df, x= df["date"],y=df["data"])
fig.show()
print(df)