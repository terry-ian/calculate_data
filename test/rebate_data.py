#!/usr/bin/env python
# coding: utf-8

# In[28]:


import pandas as pd
import numpy as np
import datetime
import requests


# In[29]:


LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
}
payload = {
    'username': 'bbtorin',
    'password': 'qwe123',
}


# In[30]:


#登入
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)

#返利
dtd = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")  
list_data_all=[]
for i in range(0,2000,1000):  #https://yb01.88lard.com/api/v1/wage/entry/list/by_user?period=20210119&first_result=0&max_results=20
    ttt = session_requests.get("https://yb01.88lard.com/api/v1/wage/entry/list/by_user?period="+str(dtd)+"&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data=ttt.json()['ret']
    list_data_all=list_data_all+output_data
user_rebate_csv_yabo=pd.DataFrame(list_data_all)[['username','amount','real_amount','period_amount']]
user_rebate_csv_yabo.columns = ['会员帐号', '已领返利','实时返利','周期返-返利']
user_rebate_csv_yabo[['已领返利','实时返利','周期返-返利']]=user_rebate_csv_yabo[['已领返利','实时返利','周期返-返利']].astype(float)


# In[31]:


LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
}
payload = {
    'username': 'bbtorin',
    'password': 'qwe123',
}


# In[32]:


#登入
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)

#返利
dtd = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d")  
list_data_all=[]
for i in range(0,2000,1000): 
    ttt = session_requests.get("https://sg.88lard.com/api/v1/wage/entry/list/by_user?period="+str(dtd)+"&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data=ttt.json()['ret']
    list_data_all=list_data_all+output_data
user_rebate_csv_sigua=pd.DataFrame(list_data_all)[['username','amount','real_amount','period_amount']]
user_rebate_csv_sigua.columns = ['会员帐号', '已领返利','实时返利','周期返-返利']
user_rebate_csv_sigua[['已领返利','实时返利','周期返-返利']]=user_rebate_csv_sigua[['已领返利','实时返利','周期返-返利']].astype(float)


# In[33]:


with pd.ExcelWriter("F:/Desktop/download_csv_sigua/rebate_data.xlsx") as rebate_data:
    user_rebate_csv_yabo.to_excel(rebate_data, sheet_name="yabo返利")
    user_rebate_csv_sigua.to_excel(rebate_data, sheet_name="sigua返利")


# In[ ]:


#傳送文件
def send_telegrame_file(text,title):
    tele_chatid=['-451149494 ','-123456789']         #测试 -451149494   #正式 -空 
    tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
    bot = telepot.Bot(tele_token)
    bot.sendMessage(chat_id=tele_chatid[0],text= title) 
    bot.sendDocument(chat_id=tele_chatid[0] , document= open(text,'rb')) #,encoding = 'utf-8'


# In[ ]:


#傳送資料
send_telegrame_file("F:/Desktop/download_csv_sigua/rebate_data.xlsx",str(delay_oneday)+'-返利數據')


# In[ ]:




