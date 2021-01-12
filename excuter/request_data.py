#!/usr/bin/env python
# coding: utf-8

# In[9]:


import requests
import telepot
import datetime
import time
import pandas as pd
import numpy as np


# In[10]:


LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            }
payload = {
    'username': 'bbtorin',
    'password': 'qwe123',
}


# In[11]:


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
    time.sleep(5) 


# In[12]:


ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/daily_report?start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00" ,headers=headers)


# In[13]:


ttt_bet = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_settle_at="+ddd+"T00%3A00%3A00-04%3A00&end_settle_at="+ddd+"T23%3A59%3A59-04%3A00&timeOption=settleAt&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=5" ,headers=headers)


# In[14]:


#存款資料
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


# In[15]:


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


# In[16]:


#獲取訊息
valid_bet=round(float(str(ttt.json()['ret'][ddd]['valid_bet']).replace("None",'0')),1)
payoff=round(float(str(ttt.json()['ret'][ddd]['payoff']).replace("None",'0'))*-1,1)

withdraw=float(str(ttt.json()['ret'][ddd]['withdraw']).replace("None",'0'))
user_count_bet=str(ttt_bet.json()['total']['user_count']).replace("NaN",'0')

deposit=float(str(deposit).replace("None",'0'))
user_count_dep=str(user_count_dep).replace("None",'0')
#傳送到TG
send_telegrame()


# In[22]:


from skpy import Skype
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


# In[ ]:


#sk.chats.recent() 
#sk.chats.chat('19:4f608eb0d3564058911ccc1961edd76a@thread.skype').sendFile(open("song.mp3", "rb"), "song.mp3") 


# In[ ]:




