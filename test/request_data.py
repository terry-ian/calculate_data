#!/usr/bin/env python
# coding: utf-8

# In[91]:


import requests
import telepot
import datetime
import time
import pandas as pd
import numpy as np
from skpy import Skype


# # YABO

# In[92]:


LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            }
payload = {
    'username': 'bbtorin',
    'password': 'qwe123',
}


# In[93]:


#發送請求
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
print(response)
ddd=(datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y-%m-%d") 
ddd_delayone=(datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d") 
#時間
delay_oneday = (datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y-%m-%d, %H") 

check_time=(datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%H") 
if check_time == '00':
    ddd=(datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d") 
    ddd_delayone=(datetime.datetime.now() - datetime.timedelta(hours=60)).strftime("%Y-%m-%d")  
    delay_oneday = (datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d, %H") 
    time.sleep(3) 


# In[94]:


#測試帳號撈取
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
ttt = session_requests.get("https://yb01.88lard.com/api/v1/player/list?level=581&enable=1&first_deposit=3&country_code=0&search=user&first_result=0&max_results=1000&sort=id&order=desc&use_cache=true&fields=bankrupt&fields=blacklist&fields=cash&fields=enable&fields=id&fields=last_city_id&fields=last_country&fields=last_ip&fields=last_login&fields=last_online&fields=level&fields=locked&fields=parent&fields=tied&fields=username&fields=upper" , headers=headers )
output_data=ttt.json()['ret']
test_user=pd.DataFrame(output_data)[['username','enable']]

#計算有效投注人數
ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+str(ddd)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd)+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=20" , headers=headers )
output_data=ttt.json()['ret']
parent_id=pd.DataFrame(output_data)[['parent_id','user_count']]

total_list=[]
list_data_all=[]
for i in range(parent_id.shape[0]) : 
    p_id=parent_id.iloc[i,0]
    u_count=parent_id.iloc[i,1]
    list_data_all=[]
    for j in range(0,int(u_count),1000): 
        ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/agent/"+str(p_id)+"/children/wager_report?start_at="+str(ddd)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd)+"T23%3A59%3A59-04%3A00&canceled=0&first_result="+str(j)+"&max_results=1000&currency=&to_CNY=true" , headers=headers )
        output_data=ttt.json()['ret']
        list_data_all=list_data_all+output_data
    total_list=total_list+list_data_all
all_bet_user=pd.DataFrame(total_list)[['username','payoff','valid_bet']]
formal_user_bet=pd.merge(all_bet_user,test_user,on = 'username',how = 'left')
user_bet_total=formal_user_bet[~(formal_user_bet['enable']==True)]


# In[95]:


#deposite withdraw
list_data_all=[]
for i in range(0, 10000, 1000) : 
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd_delayone+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)

df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['level_id'] != 581]  #測試會員 
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值
deposit=sum(df_all['amount'].astype('float'))
user_count_dep=df_all['user_id'].nunique()

#withdraw
list_data_all=[]
for i in range(0, 10000, 1000) :  
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_created_at="+ddd+"T00%3A00%3A00-04%3A00&end_created_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)
df_all=df_all[df_all['status']=='成功']    #成功單
df_all=df_all[df_all['level_id'] != 581]  #測試會員 
withdraw=sum(df_all['amount'].astype('float'))


# In[96]:


#獲取訊息
payoff=round(float(str( sum(user_bet_total['payoff'].astype('float')) ).replace("None",'0'))*-1,1)
valid_bet=round(float(str( sum(user_bet_total['valid_bet'].astype('float')) ).replace("None",'0')),1)
user_count_bet=str( user_bet_total.shape[0] ).replace("NaN",'0')

withdraw=float(str(withdraw).replace("None",'0'))
deposit=float(str(deposit).replace("None",'0'))
user_count_dep=str(user_count_dep).replace("None",'0')


# In[97]:


def send_telegrame():
    tele_chatid=['-408673375']         #测试 -451149494   #正式 -空 
    tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
    bot = telepot.Bot(tele_token)
    bot.sendMessage(chat_id=tele_chatid[0],
        text= 'YABO-'+'美東時間 : '+ str(delay_oneday) +'時'+ "\n" +
              '派彩 : '+ str(payoff) + "\n" +
              '有效投注金額 : '+ str(valid_bet) + "\n" +
              '有效投注人數 : '+ str(user_count_bet) + "\n" +
              '存款金額 : '+ str(deposit) + "\n" +
              '存提差 : '+ str(deposit-withdraw) + "\n" +
              '充值人數 : '+ str(user_count_dep) + "\n"    
              )
send_telegrame()


# # SG

# In[98]:


LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            }
payload = {
    'username': 'bbtorin',
    'password': 'qwe123',
}


# In[99]:


#發送請求
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
print(response)
ddd=(datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y-%m-%d") 
ddd_delayone=(datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d") 
#時間
delay_oneday = (datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%Y-%m-%d, %H") 

check_time=(datetime.datetime.now() - datetime.timedelta(hours=12)).strftime("%H") 
if check_time == '00':
    ddd=(datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d") 
    ddd_delayone=(datetime.datetime.now() - datetime.timedelta(hours=60)).strftime("%Y-%m-%d")  
    delay_oneday = (datetime.datetime.now() - datetime.timedelta(hours=36)).strftime("%Y-%m-%d, %H") 
    time.sleep(3) 


# In[100]:


#測試帳號撈取
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
ttt1 = session_requests.get("https://sg.88lard.com/api/v1/player/list?level=797&enable=1&first_deposit=3&country_code=0&search=user&first_result=0&max_results=1000&sort=id&order=desc&use_cache=true&fields=bankrupt&fields=blacklist&fields=cash&fields=enable&fields=id&fields=last_city_id&fields=last_country&fields=last_ip&fields=last_login&fields=last_online&fields=level&fields=locked&fields=parent&fields=tied&fields=username&fields=upper" , headers=headers )
output_data=ttt1.json()['ret']
test_user=pd.DataFrame(output_data)[['username','enable']]

#計算有效投注人數          
ttt2 = session_requests.get("https://sg.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+str(ddd)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd)+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=20" , headers=headers )
output_data=ttt2.json()['ret']
parent_id=pd.DataFrame(output_data)[['parent_id','user_count']]

total_list=[]
list_data_all=[]
for i in range(parent_id.shape[0]) : 
    p_id=parent_id.iloc[i,0]
    u_count=parent_id.iloc[i,1]
    list_data_all=[]
    for j in range(0,int(u_count),1000): 
        ttt3 = session_requests.get("https://sg.88lard.com/api/v1/stats/agent/"+str(p_id)+"/children/wager_report?start_at="+str(ddd)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd)+"T23%3A59%3A59-04%3A00&canceled=0&first_result="+str(j)+"&max_results=1000&currency=&to_CNY=true" , headers=headers )
        output_data=ttt3.json()['ret']
        list_data_all=list_data_all+output_data
    total_list=total_list+list_data_all
all_bet_user=pd.DataFrame(total_list)[['username','payoff','valid_bet']]
formal_user_bet=pd.merge(all_bet_user,test_user,on = 'username',how = 'left')
user_bet_total=formal_user_bet[~(formal_user_bet['enable']==True)]


# In[101]:


#deposite 
list_data_all=[]
for i in range(0, 10000, 1000) : 
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd_delayone+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)
df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['level_id'] != 797]  #測試會員 
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值
deposit=sum(df_all['amount'].astype('float'))
user_count_dep=df_all['user_id'].nunique()

#withdraw
list_data_all=[]
for i in range(0, 10000, 1000) : 
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_created_at="+ddd+"T00%3A00%3A00-04%3A00&end_created_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)
df_all=df_all[df_all['status']=='成功']    #成功單
df_all=df_all[df_all['level_id'] != 797]  #測試會員 
withdraw=sum(df_all['amount'].astype('float'))


# In[102]:


#獲取訊息
payoff=round(float(str( sum(user_bet_total['payoff'].astype('float')) ).replace("None",'0'))*-1,1)
valid_bet=round(float(str( sum(user_bet_total['valid_bet'].astype('float')) ).replace("None",'0')),1)
user_count_bet=str( user_bet_total.shape[0] ).replace("NaN",'0')

withdraw=float(str(withdraw).replace("None",'0'))
deposit=float(str(deposit).replace("None",'0'))
user_count_dep=str(user_count_dep).replace("None",'0')


# In[103]:


def send_telegrame():
    tele_chatid=['-408673375']         #测试 -451149494   #正式 -空 
    tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
    bot = telepot.Bot(tele_token)
    bot.sendMessage(chat_id=tele_chatid[0],
        text= 'SG-'+'美東時間 : '+ str(delay_oneday) +'時'+ "\n" +
              '派彩 : '+ str(payoff) + "\n" +
              '有效投注金額 : '+ str(valid_bet) + "\n" +
              '有效投注人數 : '+ str(user_count_bet) + "\n" +
              '存款金額 : '+ str(deposit) + "\n" +
              '存提差 : '+ str(deposit-withdraw) + "\n" +
              '充值人數 : '+ str(user_count_dep) + "\n"    
              )
send_telegrame()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


'''
sk = Skype('troy30222@gmail.com' , 'sancho130222')
sk.chats.chat('19:4f608eb0d3564058911ccc1961edd76a@thread.skype').sendMsg(
'YABO-'+'美東時間 : '+ str(delay_oneday) +'時'+ "\n" +
'派彩 : '+ str(payoff) + "\n" +
'有效投注金額 : '+ str(valid_bet) + "\n" +
'有效投注人數 : '+ str(user_count_bet) + "\n" +
'存款金額 : '+ str(round(deposit,1)) + "\n" +
'存提差 : '+ str(round(deposit-withdraw,1)) + "\n" +
'充值人數 : '+ str(user_count_dep) + "\n" 
)

sk = Skype('troy30222@gmail.com' , 'sancho130222')
sk.chats.chat('19:4f608eb0d3564058911ccc1961edd76a@thread.skype').sendMsg(
'SG-'+'美東時間 : '+ str(delay_oneday) +'時'+ "\n" +
'派彩 : '+ str(payoff) + "\n" +
'有效投注金額 : '+ str(valid_bet) + "\n" +
'有效投注人數 : '+ str(user_count_bet) + "\n" +
'存款金額 : '+ str(round(deposit,1)) + "\n" +
'存提差 : '+ str(round(deposit-withdraw,1)) + "\n" +
'充值人數 : '+ str(user_count_dep) + "\n" 
)

'''


# In[ ]:


#sk.chats.recent() 
#sk.chats.chat('19:4f608eb0d3564058911ccc1961edd76a@thread.skype').sendFile(open("song.mp3", "rb"), "song.mp3") 

