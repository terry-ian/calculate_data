#!/usr/bin/env python
# coding: utf-8

# In[43]:


import requests
import datetime
import time
import pandas as pd
import numpy as np
import random
import os
from skpy import Skype


# In[44]:


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
            }
payload = {
    'username': 'torin001',
    'password': 'qwe123',
}

#帳號密碼
username="torin001"
passwd="qwe123"
downloadpath='F:/Desktop/download_csv'
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#time
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 


# # YABO

# In[54]:


#登入
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)


# In[55]:


#withdraw
list_data_all=[]
for i in range(0, 2000, 1000) :  
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_created_at="+ddd+"T00%3A00%3A00-04%3A00&end_created_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)[['id','username','level_name','vip_level_name','at','risk_check_at','holding_operator','risk_status']]
df_all['at']=(pd.to_datetime(df_all['at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")
df_all['risk_check_at']=(pd.to_datetime(df_all['risk_check_at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")
df_all['check_time_zone']=pd.to_datetime(df_all['risk_check_at'])-pd.to_datetime(df_all['at'])
df_all['check_time_seconds']=(pd.to_datetime(df_all['risk_check_at'])-pd.to_datetime(df_all['at'])).dt.total_seconds()
df_all.columns = ['訂單編號','會員帳號','會員層級','會員VIP','申請時間','風控時間','風控人員','風控結果','時間差統計','時間差統計(秒)']
df_all['時間差統計']=df_all['時間差統計'].astype('str')
df_all_yabo=df_all


# # SIGUA

# In[56]:


#登入
LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)


# In[57]:


#withdraw
list_data_all=[]
for i in range(0, 2000, 1000) :  
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_created_at="+ddd+"T00%3A00%3A00-04%3A00&end_created_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)[['id','username','level_name','vip_level_name','at','risk_check_at','holding_operator','risk_status']]
df_all['at']=(pd.to_datetime(df_all['at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")
df_all['risk_check_at']=(pd.to_datetime(df_all['risk_check_at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")
df_all['check_time_zone']=pd.to_datetime(df_all['risk_check_at'])-pd.to_datetime(df_all['at'])
df_all['check_time_seconds']=(pd.to_datetime(df_all['risk_check_at'])-pd.to_datetime(df_all['at'])).dt.total_seconds()
df_all.columns = ['訂單編號','會員帳號','會員層級','會員VIP','申請時間','風控時間','風控人員','風控結果','時間差統計','時間差統計(秒)']
df_all['時間差統計']=df_all['時間差統計'].astype('str')
df_all_sigua=df_all


# In[65]:


with pd.ExcelWriter(downloadpath+"/risk_data.xlsx" ) as risk_data: #, index=False
    df_all_yabo.to_excel(risk_data, sheet_name="yabo", index=False)
    df_all_sigua.to_excel(risk_data, sheet_name="sigua", index=False)
    risk_data.save()


# In[66]:


sk = Skype('troy603333@gmail.com' , 'sancho1603333')
sk.chats.chat('19:ebd42b2ba9b04810ace68fb4637a006f@thread.skype').sendMsg('美東時間 : '+ str(ddd)+ "\n" )
sk.chats.chat('19:ebd42b2ba9b04810ace68fb4637a006f@thread.skype').sendFile(open(downloadpath+"/risk_data.xlsx", "rb"), "risk_data.xlsx")
#sk.chats.recent() 


# In[ ]:




