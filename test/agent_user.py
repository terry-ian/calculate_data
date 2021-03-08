#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import telepot
import datetime
import time
import pandas as pd
import numpy as np
import random
import os

#google sheet 專用
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import oauth2client


# In[6]:


#帳號密碼
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
            }
payload = {
    'username': 'torin001',
    'password': 'qwe123',
}
#登入
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)


# In[12]:


#帳號密碼
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
            }
payload = {
    'username': 'torin001',
    'password': 'qwe123',
}

#time
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 
ddd_2=(datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d") 

dtd = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y%m%d")  


# In[8]:


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly',
      'https://www.googleapis.com/auth/drive',
      'https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1EpUYvDhoT2jWLLnZ1VeetUQCQ6leJGzgPVlNSASwdnE'
creds = None
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

service = build('sheets', 'v4', credentials=creds)
# Call the Sheets API
sheet = service.spreadsheets()


# In[13]:


#寫入 data 進入 google sheet #美東時間
def insert_data(value_range_body,sheetname,colname1,colname2,col1,col2) :
    SAMPLE_RANGE_NAME = str(sheetname)+'!'+colname1+str(col1)+':'+colname2+str(col2)
    request= sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption='USER_ENTERED',range=SAMPLE_RANGE_NAME , body=value_range_body).execute()

def clear_data(sheetname,colname1,colname2,col1,col2):
    SAMPLE_RANGE_NAME = str(sheetname)+'!'+colname1+str(col1)+':'+colname2+str(col2)
    request = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute() #, body=value_range_body

def read_data(sheetname,colname1,colname2,col1,col2):
    SAMPLE_RANGE_NAME = str(sheetname)+'!'+colname1+str(col1)+':'+colname2+str(col2)
    request= sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,range=SAMPLE_RANGE_NAME ).execute()
    values = request.get('values')
    return(values)   


# # YABO

# In[146]:


#登入
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)


# In[173]:


# google sheet list  抓取名單
testuserlist=read_data('YABO會員名單','A','A',2,1000)
df_user_5level = pd.DataFrame(columns=['username','created_at','friend_count','friend_level'])  #,'level.name'
all_data_user_5 = pd.DataFrame(columns=['main','friend_level','username','created_at','friend_count'])
#user 5 level  #yu249375984
for userlist in testuserlist:
    user_list=userlist[0]
    for j in range(1,6,1) :
        list_data_all=[]
        for i in range(0, 2000, 1000) :
            ttt= session_requests.get("https://yb01.88lard.com/api/v1/player/list?upper="+str(user_list)+"&depth="+str(j)+"&first_result="+str(i)+"&max_results=1000&fields=id&fields=parent_id&fields=username&fields=name&fields=memo&fields=created_at&fields=locked&fields=enable&fields=bankrupt&fields=created_ip&fields=last_login&fields=last_ip&fields=last_country&fields=last_city_id&fields=upper&fields=friend_count&fields=last_wage&fields=cash&fields=level&fields=friend_parent&fields=tied" , headers=headers )
            output_data=ttt.json()['ret']
            list_data_all=list_data_all+output_data
        if len(list_data_all) == 0 : continue
        df_data_level=pd.json_normalize(list_data_all)[['username','created_at','friend_count']]  #,'level.name'
        df_data_level['friend_level']=j
        df_user_5level=df_user_5level.append(df_data_level)
    df_user_5level['main']=user_list
    df_user_5level=df_user_5level[['main','friend_level','username','created_at','friend_count']]
    #不同代理加總
    all_data_user_5=all_data_user_5.append(df_user_5level)

#處理時間 
all_data_user_5['created_at']=(pd.to_datetime(all_data_user_5['created_at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")


# In[106]:


#deposite withdraw
list_data_all=[]
for i in range(0, 2000, 1000) : 
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)[['username','amount','status','level_id','opcode']]
df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值
df_all['amount']=df_all['amount'].astype(float)
deposite_df=pd.DataFrame(df_all.groupby(by=['username'])['amount'].sum()).reset_index().rename(columns={ "amount": "deposite_amount"})
#增加轉讓金額
df_all=pd.DataFrame(list_data_all)[['username','amount','status','level_id','opcode']]
df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['opcode'] == 1049]   #轉讓充值
df_all['amount']=df_all['amount'].astype(float)
deposite_df_transfer=pd.DataFrame(df_all.groupby(by=['username'])['amount'].sum()).reset_index().rename(columns={ "amount": "transfer_amount"})
df_total_deposite=pd.merge(deposite_df,deposite_df_transfer,on = 'username',how = 'left')
df_total_deposite['transfer_amount']=df_total_deposite['transfer_amount'].fillna(0)

#withdraw
list_data_all=[]
for i in range(0, 2000, 1000) :  
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_updated_at="+ddd+"T00%3A00%3A00-04%3A00&end_updated_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)[['username','real_amount','status','level_id']]
df_all=df_all[df_all['status']=='成功']    #成功單
df_all['real_amount']=df_all['real_amount'].astype(float)
withdraw_df=pd.DataFrame(df_all.groupby(by=['username'])['real_amount'].sum()).reset_index().rename(columns={ "real_amount": "withdraw_amount"})


# In[107]:


#有效投注和損益
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


# In[177]:


#合併欄位
df_total_final=pd.merge(all_data_user_5,df_total_deposite,on = 'username',how = 'left')
df_total_final=pd.merge(df_total_final,withdraw_df,on = 'username',how = 'left')
df_total_final=pd.merge(df_total_final,all_bet_user,on = 'username',how = 'left')
df_total_final=df_total_final.fillna(0)


# In[179]:


clear_data('YABO資料結果','A','J',2,100000)
#填入時間
value_range_body = {"majorDimension":"COLUMNS","values":[[ddd]]}
insert_data(value_range_body,'YABO資料結果','M','M',1,1)
#填入資料
value_range_body = {"majorDimension":"ROWS","values": df_total_final.to_dict('split')['data'] } 
insert_data(value_range_body,'YABO資料結果','A','J',2,100000)


# # SIGUA

# In[10]:


#登入
LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)


# In[14]:


# google sheet list  抓取名單
testuserlist=read_data('SIGUA會員名單','A','A',2,1000)
df_user_5level = pd.DataFrame(columns=['username','created_at','friend_count','friend_level'])  #,'level.name'
all_data_user_5 = pd.DataFrame(columns=['main','friend_level','username','created_at','friend_count'])
#user 5 level  #yu249375984
for userlist in testuserlist:
    user_list=userlist[0]
    for j in range(1,6,1) :
        list_data_all=[]
        for i in range(0, 2000, 1000) :
            ttt= session_requests.get("https://sg.88lard.com/api/v1/player/list?upper="+str(user_list)+"&depth="+str(j)+"&first_result="+str(i)+"&max_results=1000&fields=id&fields=parent_id&fields=username&fields=name&fields=memo&fields=created_at&fields=locked&fields=enable&fields=bankrupt&fields=created_ip&fields=last_login&fields=last_ip&fields=last_country&fields=last_city_id&fields=upper&fields=friend_count&fields=last_wage&fields=cash&fields=level&fields=friend_parent&fields=tied" , headers=headers )
            output_data=ttt.json()['ret']
            list_data_all=list_data_all+output_data
        if len(list_data_all) == 0 : continue
        df_data_level=pd.json_normalize(list_data_all)[['username','created_at','friend_count']]  #,'level.name'
        df_data_level['friend_level']=j
        df_user_5level=df_user_5level.append(df_data_level)
    df_user_5level['main']=user_list
    df_user_5level=df_user_5level[['main','friend_level','username','created_at','friend_count']]
    #不同代理加總
    all_data_user_5=all_data_user_5.append(df_user_5level)

#處理時間 
all_data_user_5['created_at']=(pd.to_datetime(all_data_user_5['created_at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")


# In[15]:


#deposite withdraw
list_data_all=[]
for i in range(0, 2000, 1000) : 
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)[['username','amount','status','level_id','opcode']]
df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值
df_all['amount']=df_all['amount'].astype(float)
deposite_df=pd.DataFrame(df_all.groupby(by=['username'])['amount'].sum()).reset_index().rename(columns={ "amount": "deposite_amount"})
#增加轉讓金額
df_all=pd.DataFrame(list_data_all)[['username','amount','status','level_id','opcode']]
df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['opcode'] == 1049]   #轉讓充值
df_all['amount']=df_all['amount'].astype(float)
deposite_df_transfer=pd.DataFrame(df_all.groupby(by=['username'])['amount'].sum()).reset_index().rename(columns={ "amount": "transfer_amount"})
df_total_deposite=pd.merge(deposite_df,deposite_df_transfer,on = 'username',how = 'left')
df_total_deposite['transfer_amount']=df_total_deposite['transfer_amount'].fillna(0)

#withdraw
list_data_all=[]
for i in range(0, 2000, 1000) :  
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_updated_at="+ddd+"T00%3A00%3A00-04%3A00&end_updated_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)[['username','real_amount','status','level_id']]
df_all=df_all[df_all['status']=='成功']    #成功單
df_all['real_amount']=df_all['real_amount'].astype(float)
withdraw_df=pd.DataFrame(df_all.groupby(by=['username'])['real_amount'].sum()).reset_index().rename(columns={ "real_amount": "withdraw_amount"})


# In[16]:


#有效投注和損益
#計算有效投注人數
ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+str(ddd)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd)+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=20" , headers=headers )
output_data=ttt.json()['ret']
parent_id=pd.DataFrame(output_data)[['parent_id','user_count']]

total_list=[]
list_data_all=[]
for i in range(parent_id.shape[0]) : 
    p_id=parent_id.iloc[i,0]
    u_count=parent_id.iloc[i,1]
    list_data_all=[]
    for j in range(0,int(u_count),1000): 
        ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/agent/"+str(p_id)+"/children/wager_report?start_at="+str(ddd)+"T00%3A00%3A00-04%3A00&end_at="+str(ddd)+"T23%3A59%3A59-04%3A00&canceled=0&first_result="+str(j)+"&max_results=1000&currency=&to_CNY=true" , headers=headers )
        output_data=ttt.json()['ret']
        list_data_all=list_data_all+output_data
    total_list=total_list+list_data_all
all_bet_user=pd.DataFrame(total_list)[['username','payoff','valid_bet']]


# In[17]:


#合併欄位
df_total_final=pd.merge(all_data_user_5,df_total_deposite,on = 'username',how = 'left')
df_total_final=pd.merge(df_total_final,withdraw_df,on = 'username',how = 'left')
df_total_final=pd.merge(df_total_final,all_bet_user,on = 'username',how = 'left')
df_total_final=df_total_final.fillna(0)


# In[19]:


clear_data('SIGUA資料結果','A','J',2,100000)
#填入時間
value_range_body = {"majorDimension":"COLUMNS","values":[[ddd]]}
insert_data(value_range_body,'SIGUA資料結果','M','M',1,1)
#填入資料
value_range_body = {"majorDimension":"ROWS","values": df_total_final.to_dict('split')['data'] } 
insert_data(value_range_body,'SIGUA資料結果','A','J',2,100000)


# In[150]:


#sk = Skype('troy60333@gmail.com' , 'sancho160333')
#sk.chats.recent() 


#返利
#list_data_all=[]
#for i in range(0,2000,1000):  #https://yb01.88lard.com/api/v1/wage/entry/list/by_user?period=20210119&first_result=0&max_results=20
#    ttt = session_requests.get("https://yb01.88lard.com/api/v1/wage/entry/list/by_user?period="+str(dtd)+"&first_result="+str(i)+"&max_results=1000" , headers=headers )
#    output_data=ttt.json()['ret']
#    list_data_all=list_data_all+output_data
#user_rebate_list_yabo=pd.DataFrame(list_data_all)[['username','user_id','amount']]#'amount','real_amount','period_amount'
#user_rebate_list_yabo['amount']=user_rebate_list_yabo['amount'].astype(float)
#user_rebate_list_yabo=user_rebate_list_yabo[user_rebate_list_yabo['amount'] != 0]

