
# coding: utf-8

# ## Houston - House Price Index vs Energy Industry
# ----
# 
# ### Analysis
# * This study shall focus on the correlation between fluctuations in oil and gas prices and the strength of the correlation with house prices in Houston.
# * Houston is the oil and gas capital of the USA - and it would be interesting to investigate the impact of oil prices on the local economy with respect to the housing market.
# * In addition to focussing on the city of Houston, other major cities in Texas, such as Dallas and Austin shall be used to confirm the strength of the impact emanating from the energy industry.
# * A comparison of the labor market involved in the oil/gas sector by each of the cities is a good starting point on which to base the argument.
# 
# ---
# 
# #### Note
# * The FRED API shall be utilized for gathering the data.

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
import time
import requests
import json

# Import API key
import config
from config import api_key

# Output File (CSV)
output_data_file = "output_data/quarter_data.csv"
output_data_file_2 = "output_data/annual_data.csv"


# In[2]:


# New Dependency! Use this to pretty print the JSON
# https://docs.python.org/3/library/pprint.html
from pprint import pprint


# In[3]:


# The URL for the FRED API
base = 'https://api.stlouisfed.org/fred/series/observations?series_id='

# List of FRED series IDs and their description
q_dict = {'ATNHPIUS26420Q': 'House Price Index for Houston',
          'HOUS448UR':'Unemployment Rate in Houston',
          #Thousands of Persons (monthly), 
           'SMU48264201000000001SA': 'Mining and Logging',
           'HOUS448MFG': 'Manufacturing',
           'HOUS448TRAD': 'Trade, Transportation, and Utilities',
           'HOUS448FIRE': 'Financial Activities',
           'HOUS448PBSV': 'Professional and Business Services',
           'HOUS448EDUH': 'Education and Health Services',          
           'HOUS448LEIH': 'Leisure and Hospitality',
           'HOUS448GOVT': 'Government',
           'SMU48264201021100001SA':'Oil and Gas Extraction',
           'SMU48264202000000001SA':'Construction in Houston',
           #Dollars (monthly)
           'WTISPLC': 'Global price of WTI Crude',
           #Percent (monthly)
           'MORTGAGE30US': '30Yr Fixed Mortgage Rate',
           #CPI (monthly)
           'CUURA318SA0':'CPI for Houston'
          }

# Include start date, API key from config.py file and file type json
start_date = '1990-01-01'
s_dates = '&observation_start={}'.format(start_date)
end_date = '2017-01-01'
e_dates = '&observation_end={}'.format(end_date)

api_key = '&api_key={}'.format(config.api_key)

ftype = '&file_type=json'
frequency = 'q'
freq = '&frequency={}'.format(frequency)
#aggregation = 'eop'
#agg = '&aggregation_method={}'.format(aggregation)


# In[4]:


df = pd.DataFrame()
for code, name in q_dict.items():
    url = '{}{}{}{}{}{}{}'.format(base, code, s_dates,e_dates, api_key, ftype,freq)
    r = requests.get(url).json()['observations']
    df[name] = [i['value'] for i in r]
df.index = pd.to_datetime([i['date'] for i in r])
df.head()
df.to_csv('output_data/general.csv')
len(df)


# In[5]:


# List of FRED series IDs and their description
a_dict = {#'HOUS448PCPI':'Per Capita Personal Income - Houston',#2001 (annual)
          # 
          # Population and Unemployment is annual only
           'TXHARR1POP':'Population in Harris County',
           'TXFORT5POP':'Population in Fort Bend County',
           'TXMONT0POP':'Population in Montgomery County',
           'TXGALV7POP':'Population in Galveston County',
           'TXBRAZ0POP':'Population in Brazoria County',
           'TXLIBE1POP':'Population in Liberty County',
           'TXWALL3POP':'Population in Waller County',
           'TXCHAM1POP':'Population in Chambers County',
           'TXAUST5POP':'Population in Austin County',
           'HOUS448LFN':'Labor Force'
           }

# Include start date, API key from config.py file and file type json
start_date = '1990-01-01'
s_dates = '&observation_start={}'.format(start_date)
end_date = '2017-01-01'
e_dates = '&observation_end={}'.format(end_date)
api_key = '&api_key={}'.format(config.api_key)
ftype = '&file_type=json'
frequency = 'a'
freq = '&frequency={}'.format(frequency)
#aggregation = 'eop'
#agg = '&aggregation_method={}'.format(aggregation)


# In[6]:


dff = pd.DataFrame()
for code, name in a_dict.items():
    url = '{}{}{}{}{}{}{}'.format(base, code, s_dates,e_dates, api_key, ftype,freq)
    r = requests.get(url).json()['observations']
    dff[name] = [i['value'] for i in r]
dff.index = pd.to_datetime([i['date'] for i in r])
dff.to_csv('output_data/population.csv')
dff.head()
len(dff)
#dff.index.values


# ### Plotting the Data
# * Use proper labeling of the plots using plot titles (including date of analysis) and axes labels.
# * Save the plotted figures as .pngs.

# #### House Price Index vs. Oil Price

# In[7]:


x1_axis = df.index.values
x2_axis =dff.index.values


# In[8]:


df.dtypes
cols = df.columns[df.dtypes.eq(object)]
cols
for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')
df.dtypes


# In[9]:


dff.dtypes
cols = dff.columns[dff.dtypes.eq(object)]
cols
for d in cols:
    dff[d] = pd.to_numeric(dff[d], errors='coerce')
dff.dtypes


# In[10]:


df.to_csv(output_data_file)
dff.to_csv(output_data_file_2)


# In[11]:


x1_axis = df.index.values

#plt.plot(x_axis, y_axis)
plt.plot(x1_axis, df["House Price Index for Houston"],color="blue", label="Houston" )
plt.plot(x1_axis, df["Global price of WTI Crude"],color='black')

plt.legend(loc="best")

plt.title(f"House Price Index vs Oil Price")
plt.ylabel("House Price Index")
plt.xlabel("Date")

#plt.savefig("Latitude_v_MaxTemp.png")
plt.savefig("output_data/House price Index vs WTI Oil Price.png")
plt.show()


# In[12]:


df['MA'] = df.rolling(window=3)["Global price of WTI Crude"].mean()
df.tail()


# In[13]:


fig, ax = plt.subplots(figsize=(14,2.5), linewidth=5)
plt.plot(x1_axis, df["MA"],color='black',label = "Oil Price")
plt.plot(x1_axis, df["House Price Index for Houston"],color="blue", label="HPI" )


plt.legend(loc="best")

plt.title(f"HPI vs Oil Price")
plt.ylabel("HPI")
#plt.xlabel("Date")

plt.savefig("output_data/House price Index vs MA WTA Oil Price.png")
plt.show()


# In[14]:


width = 0.000001       # the width of the bars
chart1 = df[["House Price Index for Houston","Global price of WTI Crude","Mining and Logging"]]
years = chart1.index.values
oil_price = chart1["Global price of WTI Crude"]
HPI = chart1["House Price Index for Houston"]
Mining_and_Logging = chart1["Mining and Logging"]
#fourth_year = (years % 4 == 0)
#years_4 = years[fourth_year]


#fig1, ax = plt.subplots(figsize=(14,4), linewidth=5, edgecolor='.5')
fig1, ax = plt.subplots(figsize=(14,2.5), linewidth=5)
#ax.bar(years, Mining_and_Logging,275 ,facecolor='0', alpha=.3, label='Oil Price')
ax.plot(years, Mining_and_Logging, linestyle='-', linewidth=1.3, color='red', label='Oil & Gas Workers')
#ax.plot(years, oil_price, linestyle='-', linewidth=3, color='.2', label='Oil Price')
#ax.plot(years, HPI, linestyle='--', linewidth=3, color='.2', label='HPI')


ax.set_title('Oil and Gas Workers')
ax.set_ylabel('Thousand')
ax.legend()

#for x, y, v in zip(years, oil_price, oil_price):
#    ax.text(x, y + .5, str(v), ha='center')
plt.savefig("output_data/Bar_Chart_House price Index vs Oil Price.png")
plt.show()


# In[15]:


plot_cols = df[["House Price Index for Houston","MA"]]
plot_cols
fig, axes = plt.subplots(2,1, figsize=(10,7), sharex=True)
plot_cols.plot(subplots=True, ax=axes)
#for ax in axes:
#    ax.axvspan(x1_axis, df["House Price Index for Houston"], color=sns.xkcd_rgb['grey'], alpha=0.5)
#    ax.axvspan(x1_axis, df["MA"],  color=sns.xkcd_rgb['grey'], alpha=0.5)


# In[16]:


plt.plot(x1_axis, df["House Price Index for Houston"],color="blue", label="Houston Price Index" )
plt.plot(x1_axis, df["Construction in Houston"],color="green", label="Construction" )
plt.plot(x1_axis, df["Education and Health Services"],color="orange", label="Education-Health" )
plt.plot(x1_axis, df["Trade, Transportation, and Utilities"],color="brown", label="TTU" )
plt.plot(x1_axis, df["Mining and Logging"],color="purple", label="Mining and Logging" )
plt.plot(x1_axis, df["Manufacturing"],color="red", label="Manufacturing" )
plt.plot(x1_axis, df["Oil and Gas Extraction"],color="black", label="Oil and Gas Extraction" )

plt.legend(loc="best")

plt.title(f"House Price Index vs Industry Employment")
plt.ylabel("House Price Index")
plt.xlabel("Date")

plt.savefig("output_data/House Price Index vs Industry Employment")
plt.show()


# In[33]:


df2 = df.tail(1)
df2

cols = [0,1,10,12,13,14,15,16]
df2.drop(df2.columns[cols],axis=1,inplace=True)

df2 = df2.reset_index(drop=True).T
df2=df2.sort_values(by=[0], ascending=True)

#fig2, df2 = plt.subplots(figsize=(14,4), linewidth=5)

df2.plot(kind='barh',  title ='Employment by Industry in Houston',legend=None)
plt.xlabel("Thousands")
plt.show()
df2


# In[18]:


fig3, ax = plt.subplots(figsize=(14,4), linewidth=5)
ax.plot(x1_axis, df["House Price Index for Houston"],color="blue", label="Houston Price Index" )
#ax.plot(x1_axis, df["30Yr Fixed Mortgage Rate"],color="green", label="Mortgage Rate" )
ax.plot(x1_axis, df["CPI for Houston"],color="green", label="CPI for Houston" )

plt.legend(loc="best")

plt.title(f"HPI & CPI")
plt.ylabel("Index Value")
plt.xlabel("Date")

plt.savefig("output_data/HPI vs Mortagage vs CPI")
plt.show()


# In[19]:


dff.head()


# In[20]:


import datetime as dt
dff.columns
dff['Houston_Population']=dff['Population in Harris County']                        +dff['Population in Fort Bend County']                        +dff['Population in Montgomery County']+dff['Population in Galveston County']+dff['Population in Brazoria County']+dff['Population in Liberty County']+dff['Population in Waller County']+dff['Population in Chambers County']+dff['Population in Austin County']


dff['Difference'] = dff['Houston_Population'].diff()


dff.head()


# In[21]:


import datetime as dt
dates = pd.Series(range(1990,2018))
dates
dates[1]
pop = dff.iloc[:,0:8]
pop.head()
#cols = [9,10]
#pop = pop.drop(pop.columns[cols],axis=1,inplace=True)
#pop
fig2, ax = plt.subplots(figsize=(20,4), linewidth=5)

ax.plot(years, HPI, linestyle='--', linewidth=3, color='.2', label='HPI')
plt.xlabel("Year")
plt.ylabel("HPI")




pop.plot.bar(stacked=True, figsize=(14,8))
plt.xticks(np.arange(28), dates[0:28])


#plt.xticks([dates])

plt.ylabel("Thousand")
plt.xlabel("Year")
plt.show()


# In[22]:


#plot_cols = [df["House Price Index for Houston"],dff["Houston_Population"]]
#plot_cols
#df["House Price Index for Houston"].describe
#dff["Houston_Population"].describe
#plot_cols = [df["House Price Index for Houston"],dff["Houston_Population"]]
df_all_cols = pd.concat([df["House Price Index for Houston"],dff["Houston_Population"]], axis = 1)
#df_all_cols
fig, axes = plt.subplots(2,1, figsize=(10,7), sharex=True)
df_all_cols.plot(subplots=True, ax=axes)

#plt.subplot(2, 1, 1)
#plt.plot(x1_axis, df_all_cols["House Price Index for Houston"], 'o-')
#plt.title('A tale of 2 subplots')
plt.ylabel('House Price Index')

#plt.subplot(2, 1, 2)
#plt.plot(x1_axis, df_all_cols["Houston_Population"], '.-')
plt.xlabel('Year')
plt.ylabel('Thousands')

plt.show()


# In[23]:


new_df = df["House Price Index for Houston"]
new_df['Houston_Population'] = None
#new_df


# In[24]:


df["Houston_Population"] = dff['Difference']
df.to_csv('output_data/Houston_df.csv')
df.head()


# In[25]:


x2_axis =dff.index.values
plt.plot(x2_axis, dff["Houston_Population"],color="red", label="Houston Population" )
plt.plot(x1_axis, df["House Price Index for Houston"].values*20,color="blue", label="Houston Price Index" )
plt.legend(loc="best")

plt.title(f"Houston Population")
plt.ylabel("Thousands")
plt.xlabel("Year")

plt.savefig("Houston Population")
plt.show()


# In[26]:


plt.plot(x1_axis, df["Unemployment Rate in Houston"],color="blue", label="Unemployment Rate in Houston" )

plt.legend(loc="best")

plt.title(f"Unemployment Rate in Houston")
plt.ylabel("Percent")
plt.xlabel("Year")

plt.savefig("output_data/Unemployment Rate in Houston")
plt.show()


# In[27]:


BP = pd.read_csv('building_permits - annual - 1990.csv')
BP.head()


# In[28]:


#plt.plot(BP['DATE'], BP["Total_Units"],color="blue", label="Building Permits" )

#plt.legend(loc="best")

fig4, ax = plt.subplots(figsize=(14,4), linewidth=5)
ax.plot(BP['DATE'], BP["Total_Units"],color="blue", label="Building Permits" )

plt.title(f"Building Permits For Housing Units Issued for Houston")
plt.ylabel("Units")
plt.xlabel("Year")
plt.locator_params(axis='x', nbins=100)
plt.savefig("output_data/Unemployment Rate in Houston")
dates = pd.Series(range(1990,2018))
plt.xticks(np.arange(28), dates[0:28])

plt.show()


# In[29]:


LF = pd.read_csv('Civilian labor Force - monthly - 1990.csv')
LF.head()


# In[30]:


LF_axis = LF['DATE'].values

fig4, ax = plt.subplots(figsize=(14,4), linewidth=5)
ax.plot(LF_axis, LF["HOUS448LFN"],color="blue", label="Labor Force" )

plt.title(f"Labor Force for Houston")
plt.ylabel("Personnel")
plt.xlabel("Year")
#plt.locator_params(axis='x', nbins=100)
#dates = pd.Series(range(1990,2018))
#plt.xticks(np.arange(28), dates[0:28])

plt.show()


# In[31]:


EC = pd.read_csv('Economic conditions Index - monthly.csv')
EC.head()

