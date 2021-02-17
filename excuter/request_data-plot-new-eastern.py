#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
import telepot
import datetime
import pandas as pd
import numpy as np
import json

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains

import plotly
import plotly.graph_objs as go
import plotly.express as px


# In[6]:


#登入訊息
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", user_agent)
#帳號密碼
username="bbtorin"
passwd="qwe123"
downloadpath='C:/Users/btorin/Desktop/download_csv'
gekodriverpath= r'C:/Users/btorin/Desktop/excuter/geckodriver.exe'
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[7]:


def log_in_web(login_url):
    #登入頁面
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList", 2) # 0 means to download to the desktop, 1 means to download to the default "Downloads" directory, 2 means to use the directory 
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")
    fp.set_preference("browser.download.manager.showWhenStarting",False)
    fp.set_preference("browser.helperApps.neverAsk.openFile","text/plain,text/x-csv,text/csv,application/vnd.ms-excel,application/csv,application/x-csv,text/csv,text/comma-separated-values,text/x-comma-separated-values,text/tab-separated-values,application/pdf")
    fp.set_preference("browser.helperApps.alwaysAsk.force", False)
    fp.set_preference("browser.download.manager.useWindow", False)
    fp.set_preference("browser.download.manager.focusWhenStarting", False)
    fp.set_preference("browser.helperApps.neverAsk.openFile", "")
    fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
    fp.set_preference("browser.download.manager.showAlertOnComplete", False)
    fp.set_preference("browser.download.manager.closeWhenDone", True)
    fp.set_preference("browser.download.dir", downloadpath) 
    options = Options()
    options.add_argument('--headless')
    options.binary = FirefoxBinary(r'C:/Program Files/Mozilla Firefox/firefox.exe')
    browser = webdriver.Firefox(executable_path=gekodriverpath, options=options,firefox_profile = fp)
    browser.maximize_window()
    browser.get(login_url)
    time.sleep(3)
    elem=browser.find_element_by_name("username")
    elem.send_keys(username)
    elem=browser.find_element_by_name("password")
    elem.send_keys(passwd)
    elem=browser.find_element_by_class_name("ui.large.fluid.button.submit")
    elem.click()
    time.sleep(3)
    
    #點選進入迅付
    browser.find_element_by_class_name('item.sidebar-tab.extension-menu').click()
    time.sleep(1)
    browser.find_element_by_xpath('//div[@class="sidebar-text"][text()="迅付"]').click() 
    time.sleep(1) 
    
    #換分頁
    browser1=browser.window_handles[1]
    time.sleep(1)
    browser.switch_to_window(browser1) 
    time.sleep(1)
    
    #抵達會員入款訊息 
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="site-container"]/nav/div[2]/div[1]/div[2]/div/ul/li[5]/div/div[1]/a').click()
    time.sleep(2)
    browser.find_element_by_xpath('//*[@id="site-content"]/div/div[1]/button[3]').click()
    
    #获取浏览器cookies
    cookies = browser.get_cookies()  
    payid=cookies[0]['value']
    
    #關閉瀏覽器
    browser.close()
    time.sleep(1)
    browser.switch_to_window(browser.window_handles[0]) 
    time.sleep(1)
    browser.close()
    
    return(payid)


# # YABO

# In[8]:


#獲取cookies id
payid=log_in_web('https://yb01.88lard.com/')


# In[9]:


#登入訊息
headers = {
'cookie': 'lang=zh-cn; payid='+payid,
#'referer': weblink,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
} 
#北京時間
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")  #hours=12
ddd_today=(datetime.datetime.now()).strftime("%Y-%m-%d")
#抓取更動  #抓取以兩百筆為準!!
session_requests = requests.session()
ttt = session_requests.get("https://a.inpay-pro.com/api/trade/v1/monitor/account_log?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&vendor_id=81&purpose=payment&first_result=0&max_results=200&sort=created_at&order=desc" , headers=headers )
#抓取上限下限  alias enable  per_trade_min per_trade_max
ttt111 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/account/list?first_result=0&max_results=200&sort=id&order=asc" , headers=headers )
ttt222 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/merchant/deposit/list?first_result=0&max_results=200&sort=id&order=asc" , headers=headers )
ttt333 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/deposit/list?vendor_id=81&first_result=0&max_results=10&removed=false&sort=id&order=asc&deposit=true" , headers=headers )

#合併檔案
df_min_max = pd.concat( [pd.DataFrame(ttt111.json()['ret'])[['alias','method_name','per_trade_min','per_trade_max']],
                         pd.DataFrame(ttt222.json()['ret'])[['alias','method_name','per_trade_min','per_trade_max']], 
                         pd.DataFrame(ttt333.json()['ret'])[['alias','method_name','per_trade_min','per_trade_max']]])

###公司 第三方 電子錢包 入款
#公司
c_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt111_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_f=ttt111_2.json()['ret']
    c_data_all_f=c_data_all_f+output_data_f
c_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt111_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_s=ttt111_1.json()['ret']
    c_data_all_s=c_data_all_s+output_data_s
#第三方
three_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt222_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_f=ttt222_2.json()['ret']
    three_data_all_f=three_data_all_f+output_data_f
three_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt222_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_s=ttt222_1.json()['ret']
    three_data_all_s=three_data_all_s+output_data_s
#電子錢包
e_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_f=ttt333_2.json()['ret']
    e_data_all_f=e_data_all_f+output_data_f
e_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt333_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_s=ttt333_1.json()['ret']
    e_data_all_s=e_data_all_s+output_data_s


# In[10]:


#匯種細項 排除取消代客測試  成功
if len(c_data_all_s)==0 :
    c_data_all_s_df=pd.DataFrame(columns=['alias','bank_name','confirm','amount','user_id','level_name'])
else:
    c_data_all_s_df=pd.DataFrame(c_data_all_s)[['remit_account_alias','type_name','confirm','amount','user_id','level_name']].rename(columns={ "remit_account_alias": "alias","type_name": "bank_name"})
if len(three_data_all_s)==0 :
    three_data_all_s_df=pd.DataFrame(columns=['alias','bank_name','confirm','amount','user_id','level_name'])
else:
    three_data_all_s_df=pd.DataFrame(three_data_all_s)[['merchant_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "merchant_alias": "alias"})
if len(e_data_all_s)==0 :
    e_data_all_s_df=pd.DataFrame(columns=['alias','bank_name','confirm','amount','user_id','level_name'])
else:
    e_data_all_s_df=pd.DataFrame(e_data_all_s)[['wallet_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "wallet_alias": "alias"})

total_deposite_df=pd.concat([c_data_all_s_df,three_data_all_s_df,e_data_all_s_df])
total_deposite_df=total_deposite_df[total_deposite_df['confirm']==True]
total_deposite_df=total_deposite_df[total_deposite_df['alias'] != '代客充值-鸭脖银行卡支援']
total_deposite_df=total_deposite_df[total_deposite_df['level_name'] != '測試帳號']

#失敗
c_data_all_f_df=pd.DataFrame(c_data_all_f)[['remit_account_alias','type_name','confirm','amount','user_id','level_name']].rename(columns={ "remit_account_alias": "alias","type_name": "bank_name"})
three_data_all_f_df=pd.DataFrame(three_data_all_f)[['merchant_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "merchant_alias": "alias"})
e_data_all_f_df=pd.DataFrame(e_data_all_f)[['wallet_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "wallet_alias": "alias"})
total_deposite_df_f=pd.concat([c_data_all_f_df,three_data_all_f_df,e_data_all_f_df])
total_deposite_df_f=total_deposite_df_f[total_deposite_df_f['confirm']==False]
total_deposite_df_f=total_deposite_df_f[total_deposite_df_f['alias'] != '代客充值-鸭脖银行卡支援']
total_deposite_df_f=total_deposite_df_f[total_deposite_df_f['level_name'] != '測試帳號']

#抓出渠道名稱
all_channel=pd.DataFrame(total_deposite_df.groupby(['alias']).size().reset_index().rename(columns={"size": "total_count"}))
all_channel=all_channel[['alias']]
all_channel_f=pd.DataFrame(total_deposite_df_f.groupby(['alias']).size().reset_index().rename(columns={"size": "total_count"}))
all_channel_f=all_channel_f[['alias']]

#操作紀錄數據整理
df_data=pd.DataFrame(ttt.json()['ret'])
df_data=df_data[['alias','status','created_at']]
name_list=np.unique(df_data['alias'])


# In[11]:


emptylist= pd.DataFrame(columns=['Resource','Start','Finish'])
for j in name_list :
    test_data=df_data[df_data['alias']==j].sort_index(axis=0, ascending=False)
    data_len=test_data.shape[0]
    for i in range(data_len):
        if test_data['status'].iloc[0]=='disable' or test_data['status'].iloc[0]=='suspend':
            if i == 0 :
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":ddd+'T12:00:00+0800', "Finish":test_data['created_at'].iloc[0]},ignore_index=True)
            if test_data['status'].iloc[i]=='disable' and test_data['status'].iloc[i]=='suspend':
                continue
            if test_data['status'].iloc[i] == 'enable' and i != data_len-1: 
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if i == data_len-1 and test_data['status'].iloc[i] == 'enable':
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":ddd_today+'T11:59:59+0800'},ignore_index=True)

    
        if test_data['status'].iloc[0]=='enable':
            if i == 0 and i != data_len-1:
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if test_data['status'].iloc[i]=='disable' and test_data['status'].iloc[i]=='suspend':
                continue
            if test_data['status'].iloc[i] == 'enable' and i != data_len-1 and i != 0: 
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if i == data_len-1 and test_data['status'].iloc[i] == 'enable':
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":ddd_today+'T11:59:59+0800'},ignore_index=True)

#輸出操作紀錄資料
emptylist['time_open'] = pd.to_datetime(emptylist['Finish'])-pd.to_datetime(emptylist['Start'])
emptylist['Finish']=(pd.to_datetime(emptylist['Finish'])- datetime.timedelta(hours=12)).dt.strftime("%Y-%m-%d %H:%M:%S") 
emptylist['Start']=(pd.to_datetime(emptylist['Start'])- datetime.timedelta(hours=12)).dt.strftime("%Y-%m-%d %H:%M:%S") 
final_data=pd.DataFrame(emptylist.groupby(by=['Resource']).agg({'time_open': ['count','sum']})).reset_index().rename(columns={ "count": "total_count","sum": "total_time"})
final_data.columns = ['alias', 'total_count', 'total_time']  


# In[12]:


#通道合併 final_data all_channel_f
df_finaldata=pd.merge(all_channel,final_data,on = 'alias',how = 'outer')
#處理空缺的細項
df_finaldata['total_count']=df_finaldata['total_count'].fillna(1)
df_finaldata['total_time']=df_finaldata['total_time'].fillna('1 days 00:00:00')
df_finaldata=pd.merge(df_finaldata,all_channel_f,on = 'alias',how = 'outer')
#處理空缺的細項
df_finaldata['total_count']=df_finaldata['total_count'].fillna(0)
df_finaldata['total_time']=df_finaldata['total_time'].fillna('0 days 00:00:00')

df_finaldata=pd.merge(df_finaldata,df_min_max,on = 'alias',how = 'left')
df_finaldata['method_name']=df_finaldata['method_name'].replace(r'', '收银台')
df_finaldata=df_finaldata.fillna('銀行卡系列')


# In[13]:


#通道合併 final_data 
df_finaldata=pd.merge(all_channel,final_data,on = 'alias',how = 'outer')
#處理空缺的細項
df_finaldata['total_count']=df_finaldata['total_count'].fillna(1)
df_finaldata['total_time']=df_finaldata['total_time'].fillna('1 days 00:00:00')
df_finaldata=pd.merge(df_finaldata,all_channel_f,on = 'alias',how = 'outer')
#處理空缺的細項
df_finaldata['total_count']=df_finaldata['total_count'].fillna(0)
df_finaldata['total_time']=df_finaldata['total_time'].fillna('0 days 00:00:00')

df_finaldata=pd.merge(df_finaldata,df_min_max,on = 'alias',how = 'left')
df_finaldata['method_name']=df_finaldata['method_name'].replace(r'', '收银台')
df_finaldata=df_finaldata.fillna('銀行卡系列')


#list_data_all_s list_data_all_f
df_data_s=total_deposite_df[['alias','user_id','level_name','confirm','amount']]
df_data_f=total_deposite_df_f[['alias','user_id','level_name','confirm']]

#金額轉換為數值
df_data_s['amount'] = df_data_s['amount'].astype('float').astype('int')

#groupby 
df_data_s_count=pd.DataFrame(df_data_s.groupby(by=['alias']).agg({'amount': ['count','sum']})).rename(columns={ "user_id": "success_total"}).reset_index()
df_data_f_count=pd.DataFrame(df_data_f.groupby(by=['alias'])['user_id'].count()).rename(columns={ "user_id": "fail_total"}).reset_index()
df_data_s_people=pd.DataFrame(df_data_s.groupby(by=['alias'])['user_id'].nunique()).rename(columns={ "user_id": "success_user"}).reset_index()
df_data_s_count.columns = ['alias','success_total','success_amount']
df_data_f_count.columns = ['alias','fail_total']
df_data_s_people.columns = ['alias','success_user']

#merge
all_resource_df=pd.merge(df_finaldata,df_data_s_count,on = 'alias',how = 'left')
all_resource_df=pd.merge(all_resource_df,df_data_f_count,on = 'alias',how = 'left')
all_resource_df=all_resource_df.fillna(0)
all_resource_df['total_s_f']=(all_resource_df['success_total']+all_resource_df['fail_total'])
all_resource_df['success_rate']=round(all_resource_df['success_total'] / all_resource_df['total_s_f'] *100,1)
all_resource_df['fail_rate']=round(all_resource_df['fail_total'] / all_resource_df['total_s_f'] *100,1)
all_resource_df=pd.merge(all_resource_df,df_data_s_people,on = 'alias',how = 'left')

#remove na
all_resource_df=all_resource_df.fillna(0)

emptylist=emptylist.rename(columns={ "Resource": "alias"})
column_add=pd.DataFrame(df_finaldata[df_finaldata['total_time']=='1 days 00:00:00']['alias'])
column_add['Start']=ddd+'T00:00:00+0800'
column_add['Finish']=ddd+'T23:59:59+0800'
column_add['time_open']='1 days 00:00:00'
testdata_all=emptylist.append(column_add)

testdata_all=pd.merge(testdata_all,df_min_max,on = 'alias',how = 'left')
testdata_all=pd.merge(testdata_all,all_channel,on = 'alias',how = 'left')
testdata_all=testdata_all.fillna(0) # pd.to_numeric(testdata_all['per_trade_min'], errors='ignore').astype(str)
testdata_all['per_trade_min']=pd.to_numeric(testdata_all['per_trade_min'], downcast='integer')
testdata_all['alias_name']=testdata_all['alias']+'-'+testdata_all['per_trade_min'].astype(str)
testdata_all.sort_values(by=["per_trade_min",'method_name'],inplace=True)


# In[14]:


#畫圖
fig = px.timeline(testdata_all, x_start="Start", x_end="Finish", y="alias_name", color="alias" ,title='Channel Timeline Eastern')
#fig.show()

#存取到本地
plotly.offline.plot(fig, filename = downloadpath+'/filename_yabo_eastern.html', auto_open=False)
all_resource_df.to_csv(downloadpath+'/channel_data_yabo_eastern.csv' ,encoding="utf_8_sig" )
emptylist.to_csv(downloadpath+'/channel_alldata_list_yabo_eastern.csv' ,encoding="utf_8_sig" )


# In[27]:


#傳送到 TG
tele_chatid=['-408461960']         #测试 -451149494   
tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
bot = telepot.Bot(tele_token)
bot.sendMessage(chat_id=tele_chatid[0],text= 'YABO-美東時間 : '+ str(ddd) +"\n" ) 
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/filename_yabo_eastern.html','rb')) 
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/channel_data_yabo_eastern.csv','rb'))
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/channel_alldata_list_yabo_eastern.csv','rb'))

tele_chatid=['-451149494']            
tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
bot = telepot.Bot(tele_token)
bot.sendMessage(chat_id=tele_chatid[0],text= 'YABO,SIGUA-美東時間 : '+ str(ddd) +"\n" ) 
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/filename_yabo_eastern.html','rb')) 
# # SIGUA

# In[188]:


#獲取cookies id
payid=log_in_web('https://sg.88lard.com/')


# In[192]:


#登入訊息
headers = {
'cookie': 'lang=zh-cn; payid='+payid,
#'referer': weblink,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
} 
#北京時間
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")  #hours=12

#抓取操作更動  #抓取以兩百筆為準!!
session_requests = requests.session()
ttt = session_requests.get("https://a.inpay-pro.com/api/trade/v1/monitor/account_log?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&vendor_id=90&purpose=payment&first_result=0&max_results=200&sort=created_at&order=desc" , headers=headers )
#抓取上限下限  alias enable  per_trade_min per_trade_max 
ttt111 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/account/list?first_result=0&max_results=200&sort=id&order=asc" , headers=headers )
ttt222 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/merchant/deposit/list?first_result=0&max_results=200&sort=id&order=asc" , headers=headers )
ttt333 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/deposit/list?vendor_id=90&first_result=0&max_results=10&removed=false&sort=id&order=asc&deposit=true" , headers=headers )

#合併檔案
df_min_max = pd.concat( [pd.DataFrame(ttt111.json()['ret'])[['alias','method_name','per_trade_min','per_trade_max']],
                         pd.DataFrame(ttt222.json()['ret'])[['alias','method_name','per_trade_min','per_trade_max']], 
                         pd.DataFrame(ttt333.json()['ret'])[['alias','method_name','per_trade_min','per_trade_max']]])

###公司 第三方 電子錢包 入款
#公司
c_data_all_f=[]
for i in range(0, 10000, 1000) :    
    ttt111_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_f=ttt111_2.json()['ret']
    c_data_all_f=c_data_all_f+output_data_f
c_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt111_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_s=ttt111_1.json()['ret']
    c_data_all_s=c_data_all_s+output_data_s
#第三方
three_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt222_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_f=ttt222_2.json()['ret']
    three_data_all_f=three_data_all_f+output_data_f
three_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt222_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_s=ttt222_1.json()['ret']
    three_data_all_s=three_data_all_s+output_data_s
#電子錢包
e_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_f=ttt333_2.json()['ret']
    e_data_all_f=e_data_all_f+output_data_f
e_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt333_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+ddd_today+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_s=ttt333_1.json()['ret']
    e_data_all_s=e_data_all_s+output_data_s


# In[199]:


#匯種細項 排除取消代客測試  成功
if len(c_data_all_s)==0 :
    c_data_all_s_df=pd.DataFrame(columns=['alias','bank_name','confirm','amount','user_id','level_name'])
else:
    c_data_all_s_df=pd.DataFrame(c_data_all_s)[['remit_account_alias','type_name','confirm','amount','user_id','level_name']].rename(columns={ "remit_account_alias": "alias","type_name": "bank_name"})

if len(three_data_all_s)==0 :
    three_data_all_s_df=pd.DataFrame(columns=['alias','bank_name','confirm','amount','user_id','level_name'])
else:
    three_data_all_s_df=pd.DataFrame(three_data_all_s)[['merchant_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "merchant_alias": "alias"})

if len(e_data_all_s)==0 :
    e_data_all_s_df=pd.DataFrame(columns=['alias','bank_name','confirm','amount','user_id','level_name'])
else:
    e_data_all_s_df=pd.DataFrame(e_data_all_s)[['wallet_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "wallet_alias": "alias"})

total_deposite_df=pd.concat([c_data_all_s_df,three_data_all_s_df,e_data_all_s_df])
total_deposite_df=total_deposite_df[total_deposite_df['confirm']==True]
total_deposite_df=total_deposite_df[total_deposite_df['alias'] != '代客充值-丝瓜银行卡支援']
total_deposite_df=total_deposite_df[total_deposite_df['level_name'] != '测试账号']

#失敗
if len(c_data_all_f)==0 :
    c_data_all_f_df=pd.DataFrame(columns=['alias','bank_name','confirm','amount','user_id','level_name'])
else:
    c_data_all_f_df=pd.DataFrame(c_data_all_f)[['remit_account_alias','type_name','confirm','amount','user_id','level_name']].rename(columns={ "remit_account_alias": "alias","type_name": "bank_name"})
three_data_all_f_df=pd.DataFrame(three_data_all_f)[['merchant_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "merchant_alias": "alias"})
e_data_all_f_df=pd.DataFrame(e_data_all_f)[['wallet_alias','bank_name','confirm','amount','user_id','level_name']].rename(columns={ "wallet_alias": "alias"})
total_deposite_df_f=pd.concat([c_data_all_f_df,three_data_all_f_df,e_data_all_f_df])
total_deposite_df_f=total_deposite_df_f[total_deposite_df_f['confirm']==False]
total_deposite_df_f=total_deposite_df_f[total_deposite_df_f['alias'] != '代客充值-丝瓜银行卡支援']
total_deposite_df_f=total_deposite_df_f[total_deposite_df_f['level_name'] != '测试账号']

#抓出渠道名稱
all_channel=pd.DataFrame(total_deposite_df.groupby(['alias']).size().reset_index().rename(columns={"size": "total_count"}))
all_channel=all_channel[['alias']]
all_channel_f=pd.DataFrame(total_deposite_df_f.groupby(['alias']).size().reset_index().rename(columns={"size": "total_count"}))
all_channel_f=all_channel_f[['alias']]

#操作紀錄數據整理
df_data=pd.DataFrame(ttt.json()['ret'])
df_data=df_data[['alias','status','created_at']]
name_list=np.unique(df_data['alias'])


# In[200]:


emptylist= pd.DataFrame(columns=['Resource','Start','Finish'])
for j in name_list :
    test_data=df_data[df_data['alias']==j].sort_index(axis=0, ascending=False)
    data_len=test_data.shape[0]
    for i in range(data_len):
        if test_data['status'].iloc[0]=='disable' or test_data['status'].iloc[0]=='suspend':
            if i == 0 :
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":ddd+'T12:00:00+0800', "Finish":test_data['created_at'].iloc[0]},ignore_index=True)
            if test_data['status'].iloc[i]=='disable' and test_data['status'].iloc[i]=='suspend':
                continue
            if test_data['status'].iloc[i] == 'enable' and i != data_len-1: 
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if i == data_len-1 and test_data['status'].iloc[i] == 'enable':
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":ddd_today+'T11:59:59+0800'},ignore_index=True)

    
        if test_data['status'].iloc[0]=='enable':
            if i == 0 and i != data_len-1:
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if test_data['status'].iloc[i]=='disable' and test_data['status'].iloc[i]=='suspend':
                continue
            if test_data['status'].iloc[i] == 'enable' and i != data_len-1 and i != 0: 
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if i == data_len-1 and test_data['status'].iloc[i] == 'enable':
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":ddd_today+'T11:59:59+0800'},ignore_index=True)

#輸出操作紀錄資料
emptylist['time_open'] = pd.to_datetime(emptylist['Finish'])-pd.to_datetime(emptylist['Start'])
emptylist['Finish']=(pd.to_datetime(emptylist['Finish'])- datetime.timedelta(hours=12)).dt.strftime("%Y-%m-%d %H:%M:%S") 
emptylist['Start']=(pd.to_datetime(emptylist['Start'])- datetime.timedelta(hours=12)).dt.strftime("%Y-%m-%d %H:%M:%S") 
final_data=pd.DataFrame(emptylist.groupby(by=['Resource']).agg({'time_open': ['count','sum']})).reset_index().rename(columns={ "count": "total_count","sum": "total_time"})
final_data.columns = ['alias', 'total_count', 'total_time']  


# In[201]:


#通道合併 final_data 
df_finaldata=pd.merge(all_channel,final_data,on = 'alias',how = 'outer')
#處理空缺的細項
df_finaldata['total_count']=df_finaldata['total_count'].fillna(1)
df_finaldata['total_time']=df_finaldata['total_time'].fillna('1 days 00:00:00')
df_finaldata=pd.merge(df_finaldata,all_channel_f,on = 'alias',how = 'outer')
#處理空缺的細項
df_finaldata['total_count']=df_finaldata['total_count'].fillna(0)
df_finaldata['total_time']=df_finaldata['total_time'].fillna('0 days 00:00:00')

df_finaldata=pd.merge(df_finaldata,df_min_max,on = 'alias',how = 'left')
df_finaldata['method_name']=df_finaldata['method_name'].replace(r'', '收银台')
df_finaldata=df_finaldata.fillna('銀行卡系列')
#list_data_all_s list_data_all_f
df_data_s=total_deposite_df[['alias','user_id','level_name','confirm','amount']]
df_data_f=total_deposite_df_f[['alias','user_id','level_name','confirm']]

#金額轉換為數值
df_data_s['amount'] = df_data_s['amount'].astype('float').astype('int')

#groupby 
df_data_s_count=pd.DataFrame(df_data_s.groupby(by=['alias']).agg({'amount': ['count','sum']})).rename(columns={ "user_id": "success_total"}).reset_index()
df_data_f_count=pd.DataFrame(df_data_f.groupby(by=['alias'])['user_id'].count()).rename(columns={ "user_id": "fail_total"}).reset_index()
df_data_s_people=pd.DataFrame(df_data_s.groupby(by=['alias'])['user_id'].nunique()).rename(columns={ "user_id": "success_user"}).reset_index()
df_data_s_count.columns = ['alias','success_total','success_amount']
df_data_f_count.columns = ['alias','fail_total']
df_data_s_people.columns = ['alias','success_user']

#merge
all_resource_df=pd.merge(df_finaldata,df_data_s_count,on = 'alias',how = 'left')
all_resource_df=pd.merge(all_resource_df,df_data_f_count,on = 'alias',how = 'left')
all_resource_df=all_resource_df.fillna(0)
all_resource_df['total_s_f']=(all_resource_df['success_total']+all_resource_df['fail_total'])
all_resource_df['success_rate']=round(all_resource_df['success_total'] / all_resource_df['total_s_f'] *100,1)
all_resource_df['fail_rate']=round(all_resource_df['fail_total'] / all_resource_df['total_s_f'] *100,1)
all_resource_df=pd.merge(all_resource_df,df_data_s_people,on = 'alias',how = 'left')

#remove na
all_resource_df=all_resource_df.fillna(0)

emptylist=emptylist.rename(columns={ "Resource": "alias"})
column_add=pd.DataFrame(df_finaldata[df_finaldata['total_time']=='1 days 00:00:00']['alias'])
column_add['Start']=ddd+'T00:00:00+0800'
column_add['Finish']=ddd+'T23:59:59+0800'
column_add['time_open']='1 days 00:00:00'
testdata_all=emptylist.append(column_add)

testdata_all=pd.merge(testdata_all,df_min_max,on = 'alias',how = 'left')
testdata_all=pd.merge(testdata_all,all_channel,on = 'alias',how = 'left')
testdata_all=testdata_all.fillna(0) # pd.to_numeric(testdata_all['per_trade_min'], errors='ignore').astype(str)
testdata_all['per_trade_min']=pd.to_numeric(testdata_all['per_trade_min'], downcast='integer')
testdata_all['alias_name']=testdata_all['alias']+'-'+testdata_all['per_trade_min'].astype(str)
testdata_all.sort_values(by=["per_trade_min",'method_name'],inplace=True)


# In[202]:


#畫圖
fig = px.timeline(testdata_all, x_start="Start", x_end="Finish", y="alias_name", color="alias" ,title='Channel Timeline Eastern')
#fig.show()

#存取到本地
plotly.offline.plot(fig, filename = downloadpath+'/filename_sigua_eastern.html', auto_open=False)
all_resource_df.to_csv(downloadpath+'/channel_data_sigua_eastern.csv' ,encoding="utf_8_sig" )
emptylist.to_csv(downloadpath+'/channel_alldata_list_sigua_eastern.csv' ,encoding="utf_8_sig" )


# In[ ]:


#傳送到 TG
tele_chatid=['-408461960']         #测试 -451149494   
tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
bot = telepot.Bot(tele_token)
bot.sendMessage(chat_id=tele_chatid[0],text= 'SIGUA-美東時間 : '+ str(ddd) +"\n" ) 
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/filename_sigua_eastern.html','rb')) 
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/channel_data_sigua_eastern.csv','rb'))
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/channel_alldata_list_sigua_eastern.csv','rb'))

tele_chatid=['-451149494']            
tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
bot = telepot.Bot(tele_token)
bot.sendDocument(chat_id=tele_chatid[0] , document= open(downloadpath+'/filename_sigua_eastern.html','rb')) 
# In[ ]:


import os 
os.system("taskkill /im firefox.exe")

