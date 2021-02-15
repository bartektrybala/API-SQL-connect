#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymssql
import pandas as pd
import requests
import json
from datetime import date, timedelta
import numpy as np
import matplotlib.pyplot as plt


# In[3]:


conn = pymssql.connect(server = 'DESKTOP-IKOGFMH', database = 'lista6')
cursor = conn.cursor()


# In[4]:


startDate = '2019-11-11'
endDate = '2020-10-18'
resp2_USD = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/USD/'+startDate+'/'+endDate+'/?format=json')
resp1_USD = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/USD/2018-11-12/2019-11-11/?format=json')
print(resp1_USD)
print(resp2_USD)


# In[5]:


usd_rates = []
usd_dates = []

for i in resp1_USD.json()['rates']:
    usd_rates.append(i['mid'])
    usd_dates.append(i['effectiveDate'])
    
for i in resp2_USD.json()['rates']:
    usd_rates.append(i['mid'])
    usd_dates.append(i['effectiveDate'])


# In[6]:


dates = []

sdate = date(2018, 11, 12)
edate= date(2020, 10, 18)

delta = edate-sdate
for i in range(delta.days + 1):
    day = sdate + timedelta(days=i)
    dates.append(day)


# In[7]:


#skopiowanie istniejących wartości
rates = np.zeros_like(dates)

for i in range(len(dates)):
    for j in range(len(usd_dates)):
        if(dates[i].strftime('%Y-%m-%d') == usd_dates[j]):
            rates[i] = usd_rates[j]


# In[8]:


#uzupełnianie pustych wartości
for i in range(len(rates)):
    if(rates[i] == 0):
        rates[i] = rates[i-1]


# In[9]:


for i in range(len(dates)):
    mySql_insert_query = """insert into dbo.CurrencyRateData values(%s, %s, %s, %s, %s)"""
    recordTuple = (i, 'pln', 'usd', rates[i], dates[i])
    cursor.execute(mySql_insert_query, recordTuple)


# In[22]:


conn.commit()


# In[14]:


cursor.execute('select * from dbo.CurrencyRateData')
row = cursor.fetchone()
while(row):
    print(row)
    row = cursor.fetchone()

