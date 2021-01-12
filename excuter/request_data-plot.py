#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import telepot
import datetime
import pandas as pd
import numpy as np
import json
from pandas import json_normalize

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
from selenium.webdriver.common.action_chains import ActionChains


# In[2]:


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15"
profile = webdriver.FirefoxProfile()
profile.set_preference("general.useragent.override", user_agent)
#帳號密碼
username="bbtorin" 
passwd="qwe123"
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[3]:


###################  登入系統  ################
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
fp.set_preference("browser.download.dir", "F:\Desktop\download_csv") 
options = Options()
options.add_argument('--headless')
options.binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
browser = webdriver.Firefox(executable_path=r'F:\Desktop\python_code\geckodriver.exe', options=options,firefox_profile = fp)
browser.maximize_window()
browser.get('https://yb01.88lard.com/')
time.sleep(3)

#elem=browser.find_element_by_id("username")
elem=browser.find_element_by_name("username")
elem.send_keys(username)
#elem=browser.find_element_by_id("password")
elem=browser.find_element_by_name("password")
elem.send_keys(passwd)
elem=browser.find_element_by_class_name("ui.large.fluid.button.submit")
elem.click()
time.sleep(3)


# In[4]:


#點選進入迅付
browser.find_element_by_class_name('item.sidebar-tab.extension-menu').click()
time.sleep(1)
browser.find_element_by_xpath('//div[@class="sidebar-text"][text()="迅付"]').click() 
time.sleep(1) 


# In[5]:


#換分頁
browser1=browser.window_handles[1]
time.sleep(1)
browser.switch_to_window(browser1) 
time.sleep(1)


# In[6]:


#抵達會員入款訊息 
time.sleep(5)
browser.find_element_by_xpath('//*[@id="site-container"]/nav/div[2]/div[1]/div[2]/div/ul/li[5]/div/div[1]/a').click()
time.sleep(2)
browser.find_element_by_xpath('//*[@id="site-content"]/div/div[1]/button[3]').click()


# In[7]:


cookies = browser.get_cookies()  # 获取浏览器cookies
payid=cookies[0]['value']


# In[8]:


#登入訊息
headers = {
'cookie': 'lang=zh-cn; payid='+payid,
#'referer': weblink,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
} 

#北京時間
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")  #hours=12


# In[9]:


#抓取更動
session_requests = requests.session()
ttt = session_requests.get("https://a.inpay-pro.com/api/trade/v1/monitor/account_log?created_at_start="+ddd+"T00%3A00%3A00%2B0800&created_at_end="+ddd+"T23%3A59%3A59%2B0800&vendor_id=81&purpose=payment&first_result=0&max_results=200&sort=created_at&order=desc" , headers=headers )
#抓取上限下限                  
ttt222 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/merchant/deposit/list?first_result=0&max_results=200&sort=id&order=asc" , headers=headers )


# In[10]:


list_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd+"T00%3A00%3A00%2B0800&created_at_end="+ddd+"T23%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_f=ttt333.json()['ret']
    list_data_all_f=list_data_all_f+output_data_f


# In[11]:


list_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt444 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?state_at_start="+ddd+"T00%3A00%3A00%2B0800&state_at_end="+ddd+"T23%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data_s=ttt444.json()['ret']
    list_data_all_s=list_data_all_s+output_data_s


# In[12]:


all_channel=pd.DataFrame(list_data_all_f)[['merchant_alias','bank_name']]
all_channel=all_channel[all_channel['merchant_alias'] != '代客充值-鸭脖银行卡支援']


# In[13]:


all_channel=pd.DataFrame(all_channel.groupby(['merchant_alias', 'bank_name']).size().reset_index().rename(columns={"size": "total_count"}))
all_channel.columns = ['Resource','bank_name','total_count']
all_channel=all_channel[['Resource','bank_name']]


# In[14]:


browser.close()
time.sleep(1)
browser.switch_to_window(browser.window_handles[0]) 
time.sleep(1)
browser.close()


# In[15]:


df_data=pd.DataFrame(ttt.json()['ret'])
df_data=df_data[['alias','status','created_at']]


# In[16]:


name_list=np.unique(df_data['alias'])
name_list


# In[17]:


emptylist= pd.DataFrame(columns=['Resource','Start','Finish'])

for j in name_list :
    test_data=df_data[df_data['alias']==j].sort_index(axis=0, ascending=False)
    data_len=test_data.shape[0]
    for i in range(data_len):
        if test_data['status'].iloc[0]=='disable' or test_data['status'].iloc[0]=='suspend':
            if i == 0 :
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":ddd+'T00:00:00+0800', "Finish":test_data['created_at'].iloc[0]},ignore_index=True)
            if test_data['status'].iloc[i]=='disable' and test_data['status'].iloc[i]=='suspend':
                continue
            if test_data['status'].iloc[i] == 'enable' and i != data_len-1: 
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if i == data_len-1 and test_data['status'].iloc[i] == 'enable':
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":ddd+'T23:59:59+0800'},ignore_index=True)

    
        if test_data['status'].iloc[0]=='enable':
            if i == 0 and i != data_len-1:
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if test_data['status'].iloc[i]=='disable' and test_data['status'].iloc[i]=='suspend':
                continue
            if test_data['status'].iloc[i] == 'enable' and i != data_len-1 and i != 0: 
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":test_data['created_at'].iloc[i+1]},ignore_index=True)
            if i == data_len-1 and test_data['status'].iloc[i] == 'enable':
                emptylist=emptylist.append({"Resource":test_data['alias'].iloc[0],"Start":test_data['created_at'].iloc[i], "Finish":ddd+'T23:59:59+0800'},ignore_index=True)


# In[18]:


emptylist['time_open'] = pd.to_datetime(emptylist['Finish'])-pd.to_datetime(emptylist['Start'])


# In[19]:


final_data=pd.DataFrame(emptylist.groupby(by=['Resource']).agg({'time_open': ['count','sum']})).reset_index().rename(columns={ "count": "total_count","sum": "total_time"})
final_data.columns = ['Resource', 'total_count', 'total_time']


# In[20]:


#合併通道金額大小
df_min_max=pd.DataFrame(ttt222.json()['ret'])[['alias','per_trade_min','per_trade_max']]
df_min_max.columns =  ['Resource', 'per_trade_min', 'per_trade_max'] 
df_finaldata=pd.merge(all_channel,final_data,on = 'Resource',how = 'outer')
df_finaldata=pd.merge(df_finaldata,df_min_max,on = 'Resource',how = 'left')


# In[21]:


df_finaldata['total_count']=df_finaldata['total_count'].fillna(1)
df_finaldata['total_time']=df_finaldata['total_time'].fillna('1 days 00:00:00')
df_finaldata=df_finaldata.fillna('銀行卡系列')


# In[22]:


#list_data_all_s list_data_all_f
df_data_s=pd.DataFrame(list_data_all_s)[['merchant_alias','user_id','level_name','confirm','amount']]
df_data_f=pd.DataFrame(list_data_all_f)[['merchant_alias','user_id','level_name','confirm']]

#排除測試和代客
df_data_s=df_data_s[(df_data_s['merchant_alias'] != '代客充值-鸭脖银行卡支援') & (df_data_s['level_name'] != '測試帳號') & (df_data_s['confirm'] == True)]
df_data_f=df_data_f[(df_data_f['merchant_alias'] != '代客充值-鸭脖银行卡支援') & (df_data_f['level_name'] != '測試帳號') & (df_data_f['confirm'] == False)] 
df_data_s['amount'] = df_data_s['amount'].astype('float').astype('int')

#groupby 
df_data_s_count=pd.DataFrame(df_data_s.groupby(by=['merchant_alias']).agg({'amount': ['count','sum']})).rename(columns={ "user_id": "success_total"}).reset_index()
df_data_f_count=pd.DataFrame(df_data_f.groupby(by=['merchant_alias'])['user_id'].count()).rename(columns={ "user_id": "fail_total"}).reset_index()
df_data_s_people=pd.DataFrame(df_data_s.groupby(by=['merchant_alias'])['user_id'].nunique()).rename(columns={ "user_id": "success_user"}).reset_index()
df_data_s_count.columns = ['Resource','success_total','success_amount']
df_data_f_count.columns = ['Resource','fail_total']
df_data_s_people.columns = ['Resource','success_user']

#merge
all_resource_df=pd.merge(df_finaldata,df_data_s_count,on = 'Resource',how = 'left')
all_resource_df=pd.merge(all_resource_df,df_data_f_count,on = 'Resource',how = 'left')
all_resource_df=all_resource_df.fillna(0)
all_resource_df['total_s_f']=(all_resource_df['success_total']+all_resource_df['fail_total'])
all_resource_df['success_rate']=round(all_resource_df['success_total'] / all_resource_df['total_s_f'] *100,1)
all_resource_df['fail_rate']=round(all_resource_df['fail_total'] / all_resource_df['total_s_f'] *100,1)
all_resource_df=pd.merge(all_resource_df,df_data_s_people,on = 'Resource',how = 'left')

#remove na
all_resource_df=all_resource_df.fillna(0)


# In[23]:


column_add=pd.DataFrame(df_finaldata[df_finaldata['total_time']=='1 days 00:00:00']['Resource'])
column_add['Start']=ddd+'T00:00:00+0800'
column_add['Finish']=ddd+'T23:59:59+0800'
column_add['time_open']='1 days 00:00:00'
testdata_all=emptylist.append(column_add)


# In[24]:


testdata_all=pd.merge(testdata_all,df_min_max,on = 'Resource',how = 'left')
testdata_all=pd.merge(testdata_all,all_channel,on = 'Resource',how = 'left')
testdata_all=testdata_all.fillna(0) # pd.to_numeric(testdata_all['per_trade_min'], errors='ignore').astype(str)
testdata_all['per_trade_min']=pd.to_numeric(testdata_all['per_trade_min'], downcast='integer')
testdata_all['Resource_name']=testdata_all['Resource']+'-'+testdata_all['per_trade_min'].astype(str)
testdata_all.sort_values(by=["per_trade_min",'bank_name'],inplace=True)


# In[25]:


import plotly.express as px
import pandas as pd

fig = px.timeline(testdata_all, x_start="Start", x_end="Finish", y="Resource_name", color="Resource" ,title='Channel Timeline Beijing')
#fig.show()


# In[26]:


#存取到本地
import plotly
import plotly.graph_objs as go
plotly.offline.plot(fig, filename = 'F:/Desktop/download_csv/filename.html', auto_open=False)
all_resource_df.to_csv('F:/Desktop/download_csv/channel_data.csv' ,encoding="utf_8_sig" )
emptylist.to_csv('F:/Desktop/download_csv/channel_alldata_list.csv' ,encoding="utf_8_sig" )


# In[27]:


#傳送到 TG
import telepot
tele_chatid=['-408461960']         #测试 -451149494   #正式 -空 
tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
bot = telepot.Bot(tele_token)
bot.sendMessage(chat_id=tele_chatid[0],text= '北京時間 : '+ str(ddd) +"\n" ) 
bot.sendDocument(chat_id=tele_chatid[0] , document= open('F:/Desktop/download_csv/filename.html','rb')) 
bot.sendDocument(chat_id=tele_chatid[0] , document= open('F:/Desktop/download_csv/channel_data.csv','rb'))
bot.sendDocument(chat_id=tele_chatid[0] , document= open('F:/Desktop/download_csv/channel_alldata_list.csv','rb'))
#,encoding = 'utf-8'

import os 
try:
    os.system("taskkill /im firefox.exe")
except :
    print('all kill')
# In[ ]:


import sys
sys.exit()

