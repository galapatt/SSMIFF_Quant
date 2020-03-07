# In[1]:

import sqlite3
from pandas import pandas
import pandas_datareader as web
import math
import datetime as dt
from datetime import datetime

# In[2]:

conn = sqlite3.connect('SSMIF.db')
c = conn.cursor()
c.execute("""CREATE TABLE "Stock_Data" (
            "Timestamp" INTEGER NOT NULL,
            "Open" DECIMAL(10, 2),
            "High" DECIMAL(10, 2),
            "Low" DECIMAL(10, 2),
            "Close" DECIMAL(10, 2),
            "Adj_Close" DECIMAL(10, 2));""")
conn.commit()
conn.close()

# In[20]:

"""
This function takes in a ticker symbol. Using the DataReader() function, I created a pandas dataframe of the stock. The 
index of the dataframe is the datetime and the different columns are Open, High, Low, Close, Adj Close, Volume. In order
to upload this dataframe into the SQL database, I had to make sure that all the headers matched with the SQL Table, created
in the previous code. I got rid of the Volume column and renamed the Adj Close header to Adj_Close. Then, using the indices,
I create a new column, which contained the timestamp of each date, using the datetime function timestamp(). With this newly
arranged dataframe, I connected to the SQL database and converted the pandas dataframe into the SQL Table. 
"""

def fillTable(ticker):
    df = web.DataReader(ticker, 'yahoo', dt.datetime(2019,1,1), dt.datetime(2019,12,31))
    df.drop('Volume',axis=1,inplace=True)
    df.rename(columns={'Adj Close':"Adj_Close"},inplace=True)
    timestamp=[]
    for i in range(len(df)):
        timestamp.append(int(datetime.timestamp(df.index[i])))
    df.insert(0,"Timestamp",timestamp)
    conn=sqlite3.connect('SSMIF.db')
    df.to_sql('Stock_Data',conn,index=False,if_exists='replace')
    conn.close()
    
"""
This function takes in a list of the adjusted closing prices and returns a list of daily returns (percentage change). 
I was able to accomplish this by using a for loop, which found the percent change between each day's adjusted closing 
price and the next day's adjusted closing price and appended it to a list. 
"""
def DailyReturns_SQL(adjClose):
    returns=[]
    for i in range(len(adjClose)-1):
        returns.append((adjClose[i+1]-adjClose[i])/adjClose[i]*100)
    return returns

"""
This function only takes in a confidence interval to get the monthly VaR. First, I established a connection to the SQL 
database and created a cursor, which collected the entire Adj_Close column into the variable, data. Since the information
came in a list of tuples, I had a for loop that extracted the Adj_Close for each day and appended it to the adjClose 
list that I made. Then, I use the previous function to get the list of daily returns from the list of adjusted closing 
prices and calculated the Monthly VaR, using the same method as in Question 1. 
"""
def Monthly_VaR_SQL(confidence=.05):
    adjClose=[]
    conn = sqlite3.connect('SSMIF.db')
    c = conn.cursor()
    c.execute("SELECT Adj_Close FROM Stock_Data")
    data=c.fetchall()
    for i in data:
        adjClose.append(i[0])
    dailyReturns=DailyReturns_SQL(adjClose)
    dailyReturns=sorted(dailyReturns)
    VaR=dailyReturns[int(confidence*252)]
    return VaR*math.sqrt(20)


# In[23]:
fillTable("TSLA")
Monthly_VaR_SQL()
