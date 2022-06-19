#!/usr/bin/env python
# coding: utf-8

# <h1>Extracting and Visualizing Stock Data</h1>
# <h2>Description</h2>
# 

# Extracting essential data from a dataset and displaying it is a necessary part of data science; therefore individuals can make correct decisions based on the data. In this assignment, you will extract some stock data, you will then display this data in a graph.
# 

# In[1]:


get_ipython().system('pip install yfinance==0.1.67')
#!pip install pandas==1.3.3
#!pip install requests==2.26.0
get_ipython().system('mamba install bs4==4.10.0 -y')
#!pip install plotly==5.3.1


# In[2]:


import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# ## Define Graphing Function
# 

# In this section, we define the function `make_graph`. You don't have to know how the function works, you should only care about the inputs. It takes a dataframe with stock data (dataframe must contain Date and Close columns), a dataframe with revenue data (dataframe must contain Date and Revenue columns), and the name of the stock.
# 

# In[3]:


def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()


# 
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is Tesla and its ticker symbol is `TSLA`.
# 

# In[4]:


Tesla = yf.Ticker("TSLA")


# In[5]:


Tesla_info= Tesla.info
Tesla_info


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `tesla_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[6]:


Tesla_data = Tesla.history(period="max")


# 
# 

# In[7]:


Tesla_data.reset_index(inplace=True)


# In[8]:


Tesla_data.head()


# ## Use Webscraping to Extract Tesla Revenue Data
# 

# Use the `requests` library to download the webpage [https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue](https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork23455606-2022-01-01). Save the text of the response as a variable named `html_data`.
# 

# In[9]:


url = "https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue?utm_medium=Exinfluencer&utm_source=Exinfluencer&utm_content=000026UJ&utm_term=10006555&utm_id=NA-SkillsNetwork-Channel-SkillsNetworkCoursesIBMDeveloperSkillsNetworkPY0220ENSkillsNetwork23455606-2022-01-01"
html_data  = requests.get(url).text


# Parse the html data using `beautiful_soup`.
# 

# In[10]:


soup = BeautifulSoup(html_data, 'html5lib')


# Using `BeautifulSoup` or the `read_html` function extract the table with `Tesla Quarterly Revenue` and store it into a dataframe named `tesla_revenue`. The dataframe should have columns `Date` and `Revenue`.
# 

# 
# 

# In[18]:


Tesla_revenue = pd.DataFrame(columns = ["Date", "Revenue"])

for row in soup.find_all("tbody")[1].find_all('tr'):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")
    
    Tesla_revenue = Tesla_revenue.append({"Date":date, "Revenue":revenue}, ignore_index=True)
Tesla_revenue.head()


# Execute the following line to remove the comma and dollar sign from the `Revenue` column.
# 

# In[ ]:


tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(',|\$',"")


# Execute the following lines to remove an null or empty strings in the Revenue column.
# 

# In[19]:


Tesla_revenue.dropna(inplace=True)

Tesla_revenue = Tesla_revenue[Tesla_revenue['Revenue'] != ""]


# 
# 

# In[20]:


Tesla_revenue.tail()


# ##  Use yfinance to Extract Stock Data
# 

# Using the `Ticker` function enter the ticker symbol of the stock we want to extract data on to create a ticker object. The stock is GameStop and its ticker symbol is `GME`.
# 

# In[21]:


GameStop = yf.Ticker("GME")


# Using the ticker object and the function `history` extract stock information and save it in a dataframe named `gme_data`. Set the `period` parameter to `max` so we get information for the maximum amount of time.
# 

# In[22]:


gme_data = GameStop.history(period = 'max')


# 
# 

# In[23]:


gme_data.reset_index(inplace = True)
gme_data.head()


# ##  Use Webscraping to Extract GME Revenue Data
# 

# Use the `requests` library to download the webpage <https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html>. Save the text of the response as a variable named `html_data`.
# 

# In[24]:


url1 = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
html_data1 = requests.get(url1).text


# Parse the html data using `beautiful_soup`.
# 

# In[25]:


soup = BeautifulSoup(html_data1, "html.parser")
soup.find_all('title')


# 
# 

# 
# 

# In[26]:


gme_revenue = pd.DataFrame(columns = ['Date', 'Revenue'])

for row in soup.find_all("tbody")[1].find_all("tr"):
    col = row.find_all("td")
    date = col[0].text
    revenue = col[1].text.replace("$", "").replace(",", "")
    
    gme_revenue = gme_revenue.append({"Date": date, "Revenue": revenue}, ignore_index = True)


# Display the last five rows of the `gme_revenue` dataframe using the `tail` function. Take a screenshot of the results.
# 

# In[29]:


gme_revenue.dropna(inplace=True)
gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]


# In[30]:


gme_revenue.tail()


# ##  Plot Tesla Stock Graph
# 

# In[31]:


make_graph(Tesla_data, Tesla_revenue, 'Tesla')


# ## Question 6: Plot GameStop Stock Graph
# 

# In[32]:


make_graph(gme_data, gme_revenue, 'GameStop')

