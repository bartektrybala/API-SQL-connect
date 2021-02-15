#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymssql
import requests
import json
import numpy as np
from datetime import date, timedelta


# In[2]:


conn = pymssql.connect(server = 'DESKTOP-IKOGFMH', database = 'lista6')
cursor = conn.cursor()


# In[14]:


cursor.execute('create table rates(date date, rates float)')


# In[36]:


cursor.execute('alter table dbo.Facts add pln_value float')


# In[3]:


cursor.execute('select TimeID from dbo.Facts')


# In[4]:


#pobieranie dat
A = []
row = cursor.fetchone()
while row:
    A.append(row[0].strftime('%Y-%m-%d'))
    row = cursor.fetchone()


# In[5]:


dates = sorted(list(dict.fromkeys(A)))


# In[6]:


rates = np.zeros_like(dates)
for i in range(len(dates)):
    try:
        resp = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/USD/'+dates[i]+'/?format=json')
        x = resp.json()['rates'][0]['mid']
        rates[i] = x
    except:
        continue


# In[7]:


#uzupełnianie kursów
for i in range(len(rates)):
    if rates[i] == '':
        rates[i] = rates[i-1]


# In[34]:


#wprowadzanie danych do tablicy SQL
for i in range(len(rates)):
    q = """insert into rates(date, rates) values (%s, %s)"""
    r_tuple = (dates[i], rates[i])
    
    cursor.execute(q, r_tuple)


# In[38]:


#polecenie wyliczające wartość w PLN
cursor.execute('UPDATE dbo.Facts set pln_value = R.rates * F.TotalDue from dbo.rates as R inner join dbo.Facts as F on R.date = F.TimeID')


# In[39]:


conn.commit()

