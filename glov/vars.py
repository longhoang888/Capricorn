# Created by: Long Hoang
# Created on: 2022-05-19
# Description: Global constants, variables definition

#!! CONSTANTS
#--------------------------------------------------------------------------------------------------------------------------------------
#Page title, layout
import logging


page_title = "S+"
page_layout = "wide"

#Default symbol
ini_Symbol = "GOOGL"

#Control indicators
F8 = "F8"
Run = "exe"
noGO = "noGo"

# User input indicators
xPeriod = "xPeriod"
Symbol = "symbol"
Period = "period"
Start = "start"
End = "end"
High = "High"
Low = "Low"
AdjClose = "Adj Close"
summary_labs = ["previousClose", "open", "bid","bidSize", "ask", "askSize","volume","averageVolume"]
path = "logs/"


#Plot style
LINE = 'line' # line plot (default)'bar' # vertical bar plot
BAR = 'barh' # horizontal bar plot
HISTOGRAM = 'hist' # histogram
BOX = 'box' # boxplot
KDE = 'kde' # Kernel Density Estimation plot
DESNITY = 'density' # same as 'kde'
AREA = 'area' # area plot
PIE = 'pie' # pie plot
SCATTER = 'scatter' # scatter plot (DataFrame only)
HEXBIN = 'hexbin' # hexbin plot (DataFrame only)

#END-CONSTANTS-SECTION-----------------------------------------------------------------------------------------------------------------

#!! VARIANTS
#--------------------------------------------------------------------------------------------------------------------------------------
time_window = 0
days = 0

interval = "1d"

#Date time format
datefmt = '%m/%d/%Y %I:%M:%S %p'
# Error Logger - Need to update in logging.conif
the_writer = "main"
logger = logging.getLogger()

# #Error Log file name
error_log =  "{}error.log".format(path)
# #Log message format
logformat="%(asctime)s : %(levelname)s : %(module)s : %(funcName)s : %(lineno)d : (Process Details : (%(process)d, %(processName)s), Thread Details : (%(thread)d, %(threadName)s))\nLog Message : %(message)s"
#END-VARIANTS-SECTION-------------------------------------------------------------------------------------------------------------------