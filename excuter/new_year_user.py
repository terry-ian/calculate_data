#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime
import os
import telepot
import requests
from skpy import Skype
import time


# In[2]:


#time
ddd_1=(datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y-%m-%d") 
ddd_2=(datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d") 
delay_oneday = (datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y-%m-%d, %H") 

check_time=(datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%H") 
if check_time == '00':
    ddd_1=(datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d") 
    ddd_2=(datetime.datetime.now() - datetime.timedelta(hours=60)).strftime("%Y-%m-%d")  
    delay_oneday = (datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d, %H")+'~'+str(24)
    time.sleep(3) 


#time now 
today_day=datetime.datetime.now().strftime("%Y-%m-%d")   
#login information
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
}
payload = {
    'username': 'bbbtorin',
    'password': 'qwe123',
}

downloadpath='C:/Users/btorin/Desktop/download_csv'
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# # YABO

# In[3]:


####登入
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)

##檢查存款細項 deposite withdraw
list_data_all=[]
for i in range(0, 10000, 1000) : 
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd_2+"T00%3A00%3A00-04%3A00&submit_end="+ddd_1+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd_1+"T00%3A00%3A00-04%3A00&updated_end="+ddd_1+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)

df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['level_id'] != 581]  #測試會員 
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值 人工充值
df_all['amount']=df_all['amount'].astype('float')
deposite_user=df_all[['username','amount']]
deposite_user=deposite_user.groupby(['username']).agg({'amount':'sum'}).reset_index()
deposite_user.columns = ['会员帐号','充值金额']


# In[4]:


#計算有效投注人數
ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+str(ddd_1)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd_1)+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=20" , headers=headers )
output_data=ttt.json()['ret']
parent_id=pd.DataFrame(output_data)[['parent_id','user_count']]

total_list=[]
list_data_all=[]
for i in range(parent_id.shape[0]) : 
    p_id=parent_id.iloc[i,0]
    u_count=parent_id.iloc[i,1]
    list_data_all=[]
    for j in range(0,int(u_count),1000): 
        ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/agent/"+str(p_id)+"/children/wager_report?start_at="+str(ddd_1)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd_1)+"T23%3A59%3A59-04%3A00&canceled=0&first_result="+str(j)+"&max_results=1000&currency=&to_CNY=true" , headers=headers )
        output_data=ttt.json()['ret']
        list_data_all=list_data_all+output_data
    total_list=total_list+list_data_all
all_bet_user=pd.DataFrame(total_list)[['username','valid_bet']]
all_bet_user.columns = ['会员帐号','打码量']

#測試帳號撈取
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
ttt = session_requests.get("https://yb01.88lard.com/api/v1/player/list?level=581&enable=1&bankrupt=0&locked=0&tied=0&first_deposit=4&country_code=0&search=user&first_result=0&max_results=1000&sort=id&order=desc&use_cache=true&fields=bankrupt&fields=blacklist&fields=cash&fields=enable&fields=id&fields=last_city_id&fields=last_country&fields=last_ip&fields=last_login&fields=last_online&fields=level&fields=locked&fields=parent&fields=tied&fields=username&fields=upper" , headers=headers )
output_data=ttt.json()['ret']
test_user=pd.DataFrame(output_data)[['username','enable']]
test_user.columns = ['会员帐号','是否啟用']

formal_user_bet=pd.merge(all_bet_user,test_user,on = '会员帐号',how = 'left')
user_bet_total=formal_user_bet[~(formal_user_bet['是否啟用']==True)]
user_bet_total['打码量']=round(user_bet_total['打码量'].astype(float),2)

#outer join 合併最後結果
final_data=pd.merge(deposite_user,user_bet_total,on = '会员帐号',how = 'outer')
final_data1=final_data.fillna(0)
final_data1=final_data1[['会员帐号','充值金额','打码量']]


# # SIGUA

# In[5]:


####登入
LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)

##檢查存款細項 deposite withdraw
list_data_all=[]
for i in range(0, 10000, 1000) : 
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd_2+"T00%3A00%3A00-04%3A00&submit_end="+ddd_1+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd_1+"T00%3A00%3A00-04%3A00&updated_end="+ddd_1+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)

df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['level_id'] != 797]  #測試會員 
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值 人工充值
df_all['amount']=df_all['amount'].astype('float')
deposite_user=df_all[['username','amount']]
deposite_user=deposite_user.groupby(['username']).agg({'amount':'sum'}).reset_index()
deposite_user.columns = ['会员帐号','充值金额']


# In[6]:


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

#outer join 合併最後結果
final_data=pd.merge(deposite_user,user_bet_total,on = '会员帐号',how = 'outer')
final_data2=final_data.fillna(0)
final_data2=final_data2[['会员帐号','充值金额','打码量']]


# # 輸出程csv和傳送到skype

# In[7]:


with pd.ExcelWriter(downloadpath+"/auto_data.xlsx" ) as auto_data: #, index=False
    final_data1.to_excel(auto_data, sheet_name="YABO", index=False)
    final_data2.to_excel(auto_data, sheet_name="SIGUA", index=False)
    auto_data.save()


# In[8]:


sk = Skype('troy302222@gmail.com' , 'sancho1302222')
sk.chats.chat('19:719b1838a5f44c2792f2649b2c58cb87@thread.skype').sendMsg(
'美東時間 : '+ str(delay_oneday) +'時'+ "\n" )
sk.chats.chat('19:719b1838a5f44c2792f2649b2c58cb87@thread.skype').sendFile(open(downloadpath+"/auto_data.xlsx", "rb"), "auto_data.xlsx") 


# In[9]:


#sk = Skype('troy30222@gmail.com' , 'sancho130222')
#sk.chats.recent() 


# In[ ]:




