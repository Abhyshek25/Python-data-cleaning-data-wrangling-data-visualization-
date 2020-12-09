#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime

lookup = pd.read_excel('Lookup_Table.xlsx')
lookup2 = pd.read_excel('Lookup_Table.xlsx',sheet_name=1)
trans = pd.read_csv('Transactions.csv')
active = pd.read_csv('active_members_(1).csv')

print(lookup.shape[0] == len(lookup['Profit Center'].unique()))

print(lookup2.shape[0] == len(lookup2['Membership Type'].unique()))

#Transactions.csv- add a column to this data structure titled “consolidated_profit_centers” using the file “Lookup Table”, Tab = “Transactions”
dict_lookup = dict(zip(lookup['Profit Center'], lookup['Consolidated Profit Centers']))
trans['consolidated_profit_centers'] = trans['Profit Center'].map(dict_lookup)

#Active_members(1).csv- add a column to this data structure titled “consolidated_mem_types” using the file “Lookup Table”, Tab = “Membership_Types”
dict_lookup2 = dict(zip(lookup2['Membership Type'], lookup2['Membership Type Consolidated']))
active['consolidated_mem_types'] = active['Membership Type'].map(dict_lookup2)


# In[2]:


active.info()


# In[3]:


#MISSING OR IMPROPER VALUES IN AGREEMENT NUMBER COLUMN
trans.info()


# In[4]:


#New trans table free of contamination
transn = trans[trans['Agreement Number'].str.isdigit()==True]
transn['Agreement Number'] = transn['Agreement Number'].astype(int)
#Merge the active_members(1) file to the transactions file using agreement number
trans['Agreement Number'].replace('#VALUE!',0,inplace = True)
trans['Agreement Number'] = pd.to_numeric(trans['Agreement Number'])
df = pd.merge(trans,active,on = 'Agreement Number')


# In[5]:


#Summarize transactions by consolidated_profit_centers
dff = trans.groupby(['consolidated_profit_centers'])['Payment Amount'].sum().reset_index()
print(dff)

#Summarize transactions by consolidated_profit_centers
dff = df.groupby(['consolidated_profit_centers'])['Payment Amount'].sum().reset_index()
print(dff)


# In[6]:


fig, ax = plt.subplots()
fig.set_size_inches(20,20)

sns.barplot(x = 'consolidated_profit_centers' , y = 'Payment Amount',data = dff)


# In[7]:


#What is the $ value of transactions broken out by the “payment made at” field?
dff = trans.groupby(['Payment Made At'])['Payment Amount'].sum().reset_index()
print(dff)

#41 new
dff = df.groupby(['Payment Made At'])['Payment Amount'].sum().reset_index()
print(dff)


# In[8]:


#What is the unique count of agreement numbers within each consolidated_profit_center
agree_profit = trans.drop_duplicates(subset=['consolidated_profit_centers','Agreement Number'],keep='first')
[print(i,' : ',agree_profit[agree_profit['consolidated_profit_centers']==i].shape[0]) for i in agree_profit['consolidated_profit_centers'].unique()] 


# In[9]:


#total $ amount
agree_profit.groupby('consolidated_profit_centers')['Payment Amount'].sum().reset_index()


# In[10]:


#unique count
print(agree_profit['consolidated_profit_centers'].value_counts())


# In[11]:


agree_profit['consolidated_profit_centers'].value_counts().plot.bar()


# In[12]:


#average value
print(agree_profit.groupby('consolidated_profit_centers')['Payment Amount'].sum()/agree_profit['consolidated_profit_centers'].value_counts())


# In[13]:


(agree_profit.groupby('consolidated_profit_centers')['Payment Amount'].sum()/agree_profit['consolidated_profit_centers'].value_counts()).plot.bar()


# In[14]:


#What is the $ value of each consolidated_profit_center  by “Membership_Types”
dff = df.groupby(['Membership Type','consolidated_profit_centers'])['Payment Amount'].sum().reset_index()
print(dff)


# In[15]:


import matplotlib.pyplot as plt
fig, ax = plt.subplots()
# the size of A4 paper
fig.set_size_inches(20,20)

sns.barplot(x = 'Membership Type', y ='Payment Amount',data = dff)


# In[16]:


# Adjust payment date to show as a serial date (ex: 09/01/2020)
def timerang(strc):
    temp = datetime.datetime.strptime(str(strc), "%m%d%Y")
    return temp

df['Payment Date'] = df['Payment Date'].apply(timerang)


# In[17]:


df['Payment Date']


# In[18]:


import datetime


# In[19]:


#Create a new field in the merged transactions and active_members datasets called “time_range”. This field will be a calculation (shown in years) of today minus the “since date” column in the active_members(1) file. Make sure this field is rounded to the nearest integer. So for example an agreement with a since date of 12/20/2018 would have a “time_range” equal to “2”

def timerange(strc):
    temp = datetime.datetime.strptime(strc, "%m/%d/%Y")
    now = datetime.datetime.now() 
    a = now - temp
    return round(a.days/365)
a = df['Since Date'].astype(str)
df['time_range'] = a.apply(timerange)


# In[20]:


sns.boxplot(x = df['time_range'])


# In[21]:


#Summarize $ value of transactions by time_range- include sum total and unique agreement numbers 
def time_split(time):
    if time>0 and time<1:
        return '0-1'
    elif time>=1 and time<2:
        return '1-2'
    elif time>=3 and time<5:
        return '3-5'
    elif time >=5:
        return '5+'
    elif time  == np.NaN:
        return 'NA'
    
df['time split'] = df['time_range'].apply(time_split)

df.groupby(['time split'])['Payment Amount'].sum()


# In[22]:


df.groupby(['time split'])['Payment Amount'].sum().plot.bar()


# In[23]:


#What is the $ value of the consolidated profit center “fitness” based on payment date? Filter for payment made at = 8144
dff = df[df['Payment Made At']==8144].groupby(['consolidated_profit_centers'])['Payment Amount'].sum().reset_index()
print(dff)


# In[24]:


fig, ax = plt.subplots()
# the size of A4 paper
fig.set_size_inches(20,20)

sns.barplot(x = 'consolidated_profit_centers' , y = 'Payment Amount', data = dff)


# In[25]:


#Unique count of agreement numbers in the consolidated profit center “fitness” based on payment date (include unique count of N/A values). Filter for payment made at = 8144
dff = df[df['Payment Made At']==8144]
print(len(dff[df['consolidated_profit_centers'] == "Fitness"]['Agreement Number'].unique()))


# In[26]:


pwd


# In[ ]:




