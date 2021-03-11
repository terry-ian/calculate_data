#!/usr/bin/env python
# coding: utf-8

# In[66]:


import requests
import telepot
import datetime
import time
import pandas as pd
import numpy as np


# In[ ]:


downloadpath='F:/Desktop/download_csv'

headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
            }
payload = {
    'username': 'torin001',
    'password': 'qwe123',
}


# # YABO

# In[67]:


LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'


# In[68]:


#發送請求
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
#time
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 


# In[69]:


#deposite withdraw
list_data_all=[]
for i in range(0, 10000, 1000) : 
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)

df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['level_id'] != 581]  #測試會員 
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值
df_all['amount']=df_all['amount'].astype('float')
df_all_deposite=df_all[['username','user_id','amount']]
df_all_deposite=pd.DataFrame(df_all_deposite.groupby(by=['username','user_id'])['amount'].sum()).reset_index().rename(columns={ "amount": "amount"})
#withdraw
list_data_all=[]
for i in range(0, 10000, 1000) :  
    ttt333 = session_requests.get("https://yb01.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_updated_at="+ddd+"T00%3A00%3A00-04%3A00&end_updated_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)
df_all=df_all[df_all['status']=='成功']    #成功單
df_all=df_all[df_all['level_id'] != 581]  #測試會員 
df_all['real_amount']=df_all['real_amount'].astype('float')
df_all_withdraw=df_all[['username','user_id','real_amount']]
df_all_withdraw=pd.DataFrame(df_all_withdraw.groupby(by=['username','user_id'])['real_amount'].sum()).reset_index().rename(columns={ "real_amount": "real_amount"})

#合併 出款 入款資料
df_total=pd.merge(df_all_deposite,df_all_withdraw,on = ['username','user_id'],how = 'outer')
df_total=df_total.fillna(0)
df_total['diff']=df_total['amount']-df_total['real_amount']


# In[70]:


#計算有效投注
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
all_bet_user['payoff']=all_bet_user['payoff'].astype('float')*-1
all_bet_user['valid_bet']=all_bet_user['valid_bet'].astype('float')

#合併投注數據
df_total=pd.merge(df_total,all_bet_user,on = 'username',how = 'left')
df_total=df_total.fillna(0)
df_total['payoff_rate']=round((df_total['payoff']/df_total['valid_bet'])*100,2)


# In[71]:


#優惠明細拉取
ttt = session_requests.get('''https://yb01.88lard.com/api/v1/cash/entry/all?start_at='''+str(ddd)+'''T00%3A00%3A00-04%3A00&end_at='''+str(ddd)+'''T23%3A59%3A59-04%3A00&first_result=0&max_results=20&opcode=1011&opcode=1012&opcode=1030&opcode=1044&opcode=1051&opcode=3009&opcode=5001&opcode=5002&opcode=5003&opcode=5004&opcode=5005&opcode=5006&opcode=5007&opcode=5008&opcode=5009&opcode=5010&opcode=5011&opcode=5012&opcode=5013&opcode=5014&opcode=5015&opcode=5016&opcode=5017&opcode=5018&opcode=5019&opcode=5020&opcode=5021&opcode=5022&opcode=5023&opcode=5024&opcode=5025&opcode=5026&opcode=5027&opcode=5801&opcode=5802&opcode=5901&opcode=5902&opcode=6000&opcode=7000&opcode=7001&opcode=7003&trans_id=&ref_id=''' , headers=headers )
total_ccc=int(ttt.json()['pagination']['total'])
list_data_all=[]
for i in range(0, total_ccc, 1000) :  
    ttt333 = session_requests.get('''https://yb01.88lard.com/api/v1/cash/entry/all?start_at='''+str(ddd)+'''T00%3A00%3A00-04%3A00&end_at='''+str(ddd)+'''T23%3A59%3A59-04%3A00&first_result='''+str(i)+'''&max_results=1000&opcode=1011&opcode=1012&opcode=1030&opcode=1044&opcode=1051&opcode=3009&opcode=5001&opcode=5002&opcode=5003&opcode=5004&opcode=5005&opcode=5006&opcode=5007&opcode=5008&opcode=5009&opcode=5010&opcode=5011&opcode=5012&opcode=5013&opcode=5014&opcode=5015&opcode=5016&opcode=5017&opcode=5018&opcode=5019&opcode=5020&opcode=5021&opcode=5022&opcode=5023&opcode=5024&opcode=5025&opcode=5026&opcode=5027&opcode=5801&opcode=5802&opcode=5901&opcode=5902&opcode=6000&opcode=7000&opcode=7001&opcode=7003&trans_id=&ref_id=''', headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_promotion=pd.DataFrame(list_data_all)[['username','amount']]
df_promotion['amount']=df_promotion['amount'].astype('float')
df_promotion=pd.DataFrame(df_promotion.groupby(by=['username'])['amount'].sum()).reset_index().rename(columns={ "amount": "promotion_amount"})

#合併投注數據
df_total=pd.merge(df_total,df_promotion,on = 'username',how = 'left')
df_total=df_total.fillna(0)
df_total['promotion_rate']=round((df_total['promotion_amount']/df_total['valid_bet'])*100,2)

df_total.columns = ['會員帳號','會員ID','存款金額','實際出款金額','存提差','損益','有效投注','損益率(損益/有效投注)','優惠金額','優惠佔比(優惠金額/有效投注) ']
df_total_yabo=df_total


# # SG

# In[72]:


LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'


# In[73]:


#發送請求
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
#time
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 


# In[74]:


#deposite withdraw
list_data_all=[]
for i in range(0, 10000, 1000) : 
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)

df_all=df_all[df_all['status']==True]    #成功單
df_all=df_all[df_all['level_id'] != 581]  #測試會員 
df_all=df_all[df_all['opcode'] != 1049]   #轉讓充值
df_all['amount']=df_all['amount'].astype('float')
df_all_deposite=df_all[['username','user_id','amount']]
df_all_deposite=pd.DataFrame(df_all_deposite.groupby(by=['username','user_id'])['amount'].sum()).reset_index().rename(columns={ "amount": "amount"})
#withdraw
list_data_all=[]
for i in range(0, 10000, 1000) :  
    ttt333 = session_requests.get("https://sg.88lard.com/api/v1/withdraw/list?status_total=true&first_result="+str(i)+"&max_results=1000&start_updated_at="+ddd+"T00%3A00%3A00-04%3A00&end_updated_at="+ddd+"T23%3A59%3A59-04%3A00" , headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_all=pd.DataFrame(list_data_all)
df_all=df_all[df_all['status']=='成功']    #成功單
df_all=df_all[df_all['level_id'] != 581]  #測試會員 
df_all['real_amount']=df_all['real_amount'].astype('float')
df_all_withdraw=df_all[['username','user_id','real_amount']]
df_all_withdraw=pd.DataFrame(df_all_withdraw.groupby(by=['username','user_id'])['real_amount'].sum()).reset_index().rename(columns={ "real_amount": "real_amount"})

#合併 出款 入款資料
df_total=pd.merge(df_all_deposite,df_all_withdraw,on = ['username','user_id'],how = 'outer')
df_total=df_total.fillna(0)
df_total['diff']=df_total['amount']-df_total['real_amount']


# In[75]:


#計算有效投注
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
all_bet_user['payoff']=all_bet_user['payoff'].astype('float')*-1
all_bet_user['valid_bet']=all_bet_user['valid_bet'].astype('float')

#合併投注數據
df_total=pd.merge(df_total,all_bet_user,on = 'username',how = 'left')
df_total=df_total.fillna(0)
df_total['payoff_rate']=round((df_total['payoff']/df_total['valid_bet'])*100,2)


# In[76]:


#優惠明細拉取
ttt = session_requests.get('''https://sg.88lard.com/api/v1/cash/entry/all?start_at='''+str(ddd)+'''T00%3A00%3A00-04%3A00&end_at='''+str(ddd)+'''T23%3A59%3A59-04%3A00&first_result=0&max_results=20&opcode=1011&opcode=1012&opcode=1030&opcode=1044&opcode=1051&opcode=3009&opcode=5001&opcode=5002&opcode=5003&opcode=5004&opcode=5005&opcode=5006&opcode=5007&opcode=5008&opcode=5009&opcode=5010&opcode=5011&opcode=5012&opcode=5013&opcode=5014&opcode=5015&opcode=5016&opcode=5017&opcode=5018&opcode=5019&opcode=5020&opcode=5021&opcode=5022&opcode=5023&opcode=5024&opcode=5025&opcode=5026&opcode=5027&opcode=5801&opcode=5802&opcode=5901&opcode=5902&opcode=6000&opcode=7000&opcode=7001&opcode=7003&trans_id=&ref_id=''' , headers=headers )
total_ccc=int(ttt.json()['pagination']['total'])
list_data_all=[]
for i in range(0, total_ccc, 1000) :  
    ttt333 = session_requests.get('''https://sg.88lard.com/api/v1/cash/entry/all?start_at='''+str(ddd)+'''T00%3A00%3A00-04%3A00&end_at='''+str(ddd)+'''T23%3A59%3A59-04%3A00&first_result='''+str(i)+'''&max_results=1000&opcode=1011&opcode=1012&opcode=1030&opcode=1044&opcode=1051&opcode=3009&opcode=5001&opcode=5002&opcode=5003&opcode=5004&opcode=5005&opcode=5006&opcode=5007&opcode=5008&opcode=5009&opcode=5010&opcode=5011&opcode=5012&opcode=5013&opcode=5014&opcode=5015&opcode=5016&opcode=5017&opcode=5018&opcode=5019&opcode=5020&opcode=5021&opcode=5022&opcode=5023&opcode=5024&opcode=5025&opcode=5026&opcode=5027&opcode=5801&opcode=5802&opcode=5901&opcode=5902&opcode=6000&opcode=7000&opcode=7001&opcode=7003&trans_id=&ref_id=''', headers=headers )
    output_data=ttt333.json()['ret']
    list_data_all=list_data_all+output_data
df_promotion=pd.DataFrame(list_data_all)[['username','amount']]
df_promotion['amount']=df_promotion['amount'].astype('float')
df_promotion=pd.DataFrame(df_promotion.groupby(by=['username'])['amount'].sum()).reset_index().rename(columns={ "amount": "promotion_amount"})

#合併投注數據
df_total=pd.merge(df_total,df_promotion,on = 'username',how = 'left')
df_total=df_total.fillna(0)
df_total['promotion_rate']=round((df_total['promotion_amount']/df_total['valid_bet'])*100,2)

df_total.columns = ['會員帳號','會員ID','存款金額','實際出款金額','存提差','損益','有效投注','損益率(損益/有效投注)','優惠金額','優惠佔比(優惠金額/有效投注) ']
df_total_sigua=df_total


# In[77]:


with pd.ExcelWriter(downloadpath+"/user_data_all.xlsx" ) as user_data_all: #, index=False
    df_total_yabo.to_excel(user_data_all, sheet_name="yabo", index=False)
    df_total_sigua.to_excel(user_data_all, sheet_name="sigua", index=False)
    user_data_all.save()


# In[79]:


#傳送文件
def send_telegrame_file(text,title):
    tele_chatid=['-451149494 ','-123456789']         #测试 -451149494   #正式 -空 
    tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
    bot = telepot.Bot(tele_token)
    bot.sendMessage(chat_id=tele_chatid[0],text= title) 
    bot.sendDocument(chat_id=tele_chatid[0] , document= open(text,'rb')) #,encoding = 'utf-8'


# In[80]:


#傳送資料
send_telegrame_file(downloadpath+"/user_data_all.xlsx",str(ddd)+'-當日會員數據')


# In[ ]:




