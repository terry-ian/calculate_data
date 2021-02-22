#!/usr/bin/env python
# coding: utf-8

# In[279]:


import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import os
import telepot
import requests
import time
from skpy import Skype


# In[280]:


# 上周第一天和最后一天 now美東時間
now = datetime.datetime.now()-timedelta(hours=12) # -timedelta(hours=3)#- timedelta(days=12)  -timedelta(hours=-5)
ddd_1 = (now - timedelta(days=now.weekday() ) ).strftime("%Y-%m-%d") #now_week_start
ddd_2 = (now ).strftime("%Y-%m-%d") #now_week_end
delay_oneday =ddd_1+', 00時'+' ~ '+(now ).strftime("%Y-%m-%d, %H")+'時'

check_time=(now).strftime("%H") 

if check_time == '00' :
    ddd_1 = (now - timedelta(days=now.weekday() ) ).strftime("%Y-%m-%d") #now_week_start
    ddd_2 = (now - timedelta(days=1)).strftime("%Y-%m-%d")
    delay_oneday =ddd_1+', 00時'+' ~ '+ddd_2+', 24時'
    time.sleep(1)

if check_time == '00' and now.weekday()==0:
    ddd_1=(now - timedelta(days=now.weekday() + 7)).strftime("%Y-%m-%d") #last_week_start
    ddd_2=(now - timedelta(days=now.weekday() +1)).strftime("%Y-%m-%d")   #last_week_end
    delay_oneday =ddd_1+', 00時'+' ~ '+ddd_2+', 24時'
    time.sleep(1) 

#login information
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
}
payload = {
    'username': 'bbbtorin',
    'password': 'qwe123',
}

downloadpath='F:/Desktop/download_csv'
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[281]:


####登入
LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)


# In[282]:


#計算有效投注人數
ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+str(ddd_1)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd_1)+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=20" , headers=headers )
output_data=ttt.json()['ret']
parent_id=pd.DataFrame(output_data)[['parent_id','user_count']]

total_list=[]
list_data_all=[]
for i in range(parent_id.shape[0]) : 
    p_id=parent_id.iloc[i,0]
    u_count=parent_id.iloc[i,1]
    list_data_all=[]
    for j in range(0,int(u_count),1000): 
        ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/agent/"+str(p_id)+"/children/wager_report?start_at="+str(ddd_1)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd_1)+"T23%3A59%3A59-04%3A00&canceled=0&first_result="+str(j)+"&max_results=1000&currency=&to_CNY=true" , headers=headers )
        output_data=ttt.json()['ret']
        list_data_all=list_data_all+output_data
    total_list=total_list+list_data_all
all_bet_user=pd.DataFrame(total_list)[['username','valid_bet']]
all_bet_user.columns = ['会员帐号','打码量']

#測試帳號撈取
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
ttt = session_requests.get("https://sg.88lard.com/api/v1/player/list?level=797&enable=1&bankrupt=0&locked=0&tied=0&first_deposit=4&country_code=0&search=user&first_result=0&max_results=1000&sort=id&order=desc&use_cache=true&fields=bankrupt&fields=blacklist&fields=cash&fields=enable&fields=id&fields=last_city_id&fields=last_country&fields=last_ip&fields=last_login&fields=last_online&fields=level&fields=locked&fields=parent&fields=tied&fields=username&fields=upper" , headers=headers )
output_data=ttt.json()['ret']
test_user=pd.DataFrame(output_data)[['username','enable']]
test_user.columns = ['会员帐号','是否啟用']

formal_user_bet=pd.merge(all_bet_user,test_user,on = '会员帐号',how = 'left')
user_bet_total=formal_user_bet[~(formal_user_bet['是否啟用']==True)]
user_bet_total['打码量']=round(user_bet_total['打码量'].astype(float),2)
user_bet_total=user_bet_total[['会员帐号','打码量']]


# In[283]:


with pd.ExcelWriter(downloadpath+"/auto_data.xlsx" ) as auto_data: #, index=False
    user_bet_total.to_excel(auto_data, sheet_name="SIGUA", index=False)
    auto_data.save()


# In[ ]:


sk = Skype('troy302222@gmail.com' , 'sancho1302222')
sk.chats.chat('19:719b1838a5f44c2792f2649b2c58cb87@thread.skype').sendMsg(
'美東時間 : '+ str(delay_oneday) + "\n" )
sk.chats.chat('19:719b1838a5f44c2792f2649b2c58cb87@thread.skype').sendFile(open(downloadpath+"/auto_data.xlsx", "rb"), "auto_data.xlsx") 


# In[ ]:




