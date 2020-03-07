# In[4]:


import pandas as pd
import pandas_datareader as web
import statistics as stats
import math
import datetime as dt


# In[5]:

"""
This function takes in a dataframe and returns a list of of daily returns,
which is the percentage change from the old adjusted closing price to the 
new adjusted closing price. Using, the pct_change() function created a new
dataframe of daily returns, which I had to transfer into a list, using a for
loop, excluding the first one, which was NaN. 
"""
def DailyReturns(df):
    returns=[]
    dailyReturns=df['Adj Close'].pct_change()*100
    for val in dailyReturns:
        returns.append(val)
    return returns[1:]

"""
This function takes in the ticker and confidence level. I downloaded
all the information about the stock from Yahoo Finance, using the 
DataReader() function. Then, I got the list of Daily Returns, using the 
previous function. In order to calculate the monthly VaR, I first calculated the daily VaR. 
To do that, I sorted the list of daily returns and found the index at which the VaR
occurs by multiply the confidence level by the number of trading days in
a year, 252 days. Using the index, I found the daily VaR and multiplied that by the
square of root of 20, since there are around 20 trading days every month. 
"""

def Monthly_VaR(ticker,confidence=.05):
    df = web.DataReader(ticker, 'yahoo', dt.datetime(2019,1,1), dt.datetime(2019,12,31))
    dailyReturns=DailyReturns(df)
    dailyReturns=sorted(dailyReturns)
    VaR=dailyReturns[int(confidence*252)]
    return VaR*math.sqrt(20)

"""
To get the Monthly CVaR, I followed a similar strategy to the previous
function. Instead, I took the mean of all values from the lowest daily 
return to the daily VaR, which represents the daily CVaR. To get the 
monthly CVaR, I multplied the daily CVaR by the square root of the 
time period, which is 20. 
"""

def Monthly_CVaR(ticker, confidence=.05):
    df = web.DataReader(ticker, 'yahoo', dt.datetime(2019,1,1), dt.datetime(2019,12,31))
    dailyReturns=DailyReturns(df)
    dailyReturns=sorted(dailyReturns)
    CVaR=stats.mean(dailyReturns[:int(confidence*252)])
    return CVaR*math.sqrt(20)

"""
This function takes in the ticker and gets the list of daily return. In
order to calculate the volatility, I used the stats function pstdev(), 
which calculates the population standard deviation of the daily returns. 
This value represents the dispersion of the total number of returns for
2019, which is the volatility.
"""

def Monthly_Volatility(ticker):
    df = web.DataReader(ticker, 'yahoo', dt.datetime(2019,1,1), dt.datetime(2019,12,31))
    dailyReturns=DailyReturns(df)
    dailyReturns=sorted(dailyReturns)
    return stats.pstdev(dailyReturns)*math.sqrt(20)
    
# In[7]:

print(Monthly_VaR("TSLA"))
print(Monthly_CVaR("TSLA"))
print(Monthly_Volatility("TSLA"))

