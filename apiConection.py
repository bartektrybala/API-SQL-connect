#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import json
import matplotlib.pyplot as plt


# In[2]:


startDate = '2020-04-11'
endDate = '2020-10-18'
resp_USD = requests.get('http://api.nbp.pl/api/exchangerates/rates/A/USD/'+startDate+'/'+endDate+'/?format=json')
resp_EUR= requests.get('http://api.nbp.pl/api/exchangerates/rates/A/EUR/'+startDate+'/'+endDate+'/?format=json')
print(resp_USD)


# In[6]:


def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


# In[7]:


jprint(resp_USD.json())


# In[148]:


usd_rates = []
usd_dates = []
euro_rates = []
euro_dates = []

for i in resp_USD.json()['rates']:
    usd_rates.append(i['mid'])
    usd_dates.append(i['effectiveDate'])

for i in resp_EUR.json()['rates']:
    euro_rates.append(i['mid'])
    euro_dates.append(i['effectiveDate'])


# In[157]:


beingsaved = plt.figure()
plt.plot(usd_dates, usd_rates, label='usd')
plt.plot(euro_dates, euro_rates, label='euro')
plt.xlabel('date')
plt.ylabel('kurs')
plt.title('2020-04-11 to 2020-10-18')
plt.legend()
plt.show()


# In[159]:


beingsaved.savefig('zad3_plot.eps', format='eps')


# In[ ]:




