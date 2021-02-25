#!/usr/bin/env python
# coding: utf-8

# In[132]:


import requests
import telepot
import datetime
import time
import pandas as pd
import numpy as np
import random
import os
from skpy import Skype

import datetime
import string

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains


# In[133]:


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
gekodriverpath= r'F:/Desktop/python_code/geckodriver.exe'
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[134]:


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

# In[135]:


#獲取cookies id
payid=log_in_web('https://yb01.88lard.com/')

headerss = {
'cookie': 'lang=zh-cn; payid='+payid,
#'referer': weblink,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
} 

ddd=(datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d") 
ddd_2=(datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d") 

####登入
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headerss)


# In[136]:


####申請時間####
c_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt111_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=337&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt111_2.json()['ret']
    c_data_all_f=c_data_all_f+output_data_f
three_data_all_f=[]
for i in range(0, 50000, 1000) :   
    ttt222_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=337&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt222_2.json()['ret']
    three_data_all_f=three_data_all_f+output_data_f
e_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=337&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt333_2.json()['ret']
    e_data_all_f=e_data_all_f+output_data_f
m_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt444_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/crypto/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=337&display_merge_data=true&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt444_2.json()['ret']
    m_data_all_f=m_data_all_f+output_data_f

def changetodataframe(df):
    if len(df)==0 :
        output=pd.DataFrame(columns=['username','user_id','amount'])
    else:
        output=pd.DataFrame(df)[['username','user_id','amount']]
        output.columns = ['username','user_id','amount']
        output['amount']=output['amount'].astype('float')
    return(output)

register_deposite_c=changetodataframe(c_data_all_f)
register_deposite_3=changetodataframe(three_data_all_f)
register_deposite_e=changetodataframe(e_data_all_f)
register_deposite_m=changetodataframe(m_data_all_f)
df_all=register_deposite_c.append(register_deposite_3).append(register_deposite_e).append(register_deposite_m)
df_unique_user=pd.DataFrame(df_all.groupby(by=['username','user_id'])['amount'].sum()).reset_index().rename(columns={ "amount": "amount"})


# In[137]:


#發送請求
ddd_3=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)

#user confirm telephone
list_data_all=[]
for i in range(0, 20000, 1000) : 
    ttt= session_requests.get("https://yb01.88lard.com/api/v1/execution_log?item_id=1&method=PUT&start_at="+ddd_3+"T00%3A00%3A00-04%3A00&end_at="+ddd_3+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data=ttt.json()['ret']
    list_data_all=list_data_all+output_data
df_confirm=pd.DataFrame(list_data_all)[['operator','message','table_name']]
df_confirm=df_confirm[df_confirm['table_name'] == 'user_phone']
df_confirm['operator']=df_confirm['operator'].str[2:]
df_confirm=df_confirm[df_confirm['message'].str.contains("已验证")]
df_confirm['phone_confirm'] = 1
df_confirm.columns = ['username', 'message', 'table_name','phone_confirm']


# In[138]:


#合併未送單未存款存款會員
df_total=pd.merge(df_confirm,df_unique_user,on = 'username',how = 'left')
df_total=df_total[df_total['amount'].isnull()][['username','phone_confirm']]

#随机打乱  寫入新的 index
random_df=df_total.reset_index(drop=True)


# In[139]:


#分組名單序列
n=random_df.shape[0]
offices = [[],[],[],[],[],[],[],[],[]]
people_number= int(n/9)

#用來分配參數
teachersName = list(np.random.permutation(n)) #lsitdata=
#取出數值，放置到随机的群里,用循环语句
j = 0
while j <n:
    #使用随机函数，生成列表群的索引号
    index1 = random.randint(0,8)
    #如果这个群已经分配了两个人，或不少于两个人，则进入下一步，否则把參數取出放到群内。
    if offices[index1].__len__() > people_number and offices[index1].__len__() < people_number+2:
        continue
    else :
        offices[index1].append(teachersName[j])
    #一直执行完毕为止
    j += 1


# In[140]:


random_df=random_df[['username','phone_confirm']]
part3=random_df.iloc[offices[0]]
part4=random_df.iloc[offices[1]]
part6=random_df.iloc[offices[2]]
part7=random_df.iloc[offices[3]]
part9=random_df.iloc[offices[4]]
part11=random_df.iloc[offices[5]]
part12=random_df.iloc[offices[6]]
part14=random_df.iloc[offices[7]]
part15=random_df.iloc[offices[8]]


# # SIGUA

# In[141]:


#獲取cookies id
payid=log_in_web('https://sg.88lard.com/')

headerss = {
'cookie': 'lang=zh-cn; payid='+payid,
#'referer': weblink,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
} 

ddd=(datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d") 
ddd_2=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 

####登入
LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headerss)


# In[142]:


####申請時間####
c_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt111_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=598&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt111_2.json()['ret']
    c_data_all_f=c_data_all_f+output_data_f
three_data_all_f=[]
for i in range(0, 50000, 1000) :   
    ttt222_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=598&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt222_2.json()['ret']
    three_data_all_f=three_data_all_f+output_data_f
e_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=598&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt333_2.json()['ret']
    e_data_all_f=e_data_all_f+output_data_f
m_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt444_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/crypto/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&vendor_user_level_id=598&display_merge_data=true&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt444_2.json()['ret']
    m_data_all_f=m_data_all_f+output_data_f

def changetodataframe(df):
    if len(df)==0 :
        output=pd.DataFrame(columns=['username','user_id','amount'])
    else:
        output=pd.DataFrame(df)[['username','user_id','amount']]
        output.columns = ['username','user_id','amount']
        output['amount']=output['amount'].astype('float')
    return(output)

register_deposite_c=changetodataframe(c_data_all_f)
register_deposite_3=changetodataframe(three_data_all_f)
register_deposite_e=changetodataframe(e_data_all_f)
register_deposite_m=changetodataframe(m_data_all_f)
df_all=register_deposite_c.append(register_deposite_3).append(register_deposite_e).append(register_deposite_m)
df_unique_user=pd.DataFrame(df_all.groupby(by=['username','user_id'])['amount'].sum()).reset_index().rename(columns={ "amount": "amount"})


# In[143]:


#發送請求
ddd_3=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 
LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)

#user confirm telephone
list_data_all=[]
for i in range(0, 20000, 1000) : 
    ttt= session_requests.get("https://sg.88lard.com/api/v1/execution_log?item_id=1&method=PUT&start_at="+ddd_3+"T00%3A00%3A00-04%3A00&end_at="+ddd_3+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data=ttt.json()['ret']
    list_data_all=list_data_all+output_data
df_confirm=pd.DataFrame(list_data_all)[['operator','message','table_name']]
df_confirm=df_confirm[df_confirm['table_name'] == 'user_phone']
df_confirm['operator']=df_confirm['operator'].str[2:]
df_confirm=df_confirm[df_confirm['message'].str.contains("已验证")]
df_confirm['phone_confirm'] = 1
df_confirm.columns = ['username', 'message', 'table_name','phone_confirm']


# In[144]:


#合併未送單未存款存款會員
df_total=pd.merge(df_confirm,df_unique_user,on = 'username',how = 'left')
df_total=df_total[df_total['amount'].isnull()][['username','phone_confirm']]

#随机打乱  寫入新的 index
random_df=df_total.reset_index(drop=True)


# In[177]:


#分組名單序列
n=random_df.shape[0]
offices = [[],[],[],[],[]]
people_number= int(n/5)

#用來分配參數
teachersName = list(np.random.permutation(n)) #lsitdata=
#取出數值，放置到随机的群里,用循环语句
j = 0
while j <n:
    #使用随机函数，生成列表群的索引号
    index1 = random.randint(0,4)
    #如果这个群已经分配了两个人，或不少于两个人，则进入下一步，否则把參數取出放到群内。
    if offices[index1].__len__() > people_number and offices[index1].__len__() < people_number+2:
        continue
    else :
        offices[index1].append(teachersName[j])
    #一直执行完毕为止
    j += 1


# In[146]:


random_df=random_df[['username','phone_confirm']]
part1_s=random_df.iloc[offices[0]]
part2_s=random_df.iloc[offices[1]]
part3_s=random_df.iloc[offices[2]]
part4_s=random_df.iloc[offices[3]]
part5_s=random_df.iloc[offices[4]]


# # SKYPE insert

# In[147]:


with pd.ExcelWriter(downloadpath+"/YABO_data.xlsx" ) as YABO_data: #, index=False
    part3.to_excel(YABO_data, sheet_name="ts3", index=False)
    part4.to_excel(YABO_data, sheet_name="ts4", index=False)
    part6.to_excel(YABO_data, sheet_name="ts6", index=False)
    part7.to_excel(YABO_data, sheet_name="ts7", index=False)
    part9.to_excel(YABO_data, sheet_name="ts9", index=False)
    part11.to_excel(YABO_data, sheet_name="ts11", index=False)
    part12.to_excel(YABO_data, sheet_name="ts12", index=False)
    part14.to_excel(YABO_data, sheet_name="ts14", index=False)
    part15.to_excel(YABO_data, sheet_name="ts15", index=False)
    YABO_data.save()
    
with pd.ExcelWriter(downloadpath+"/SIGUA_data.xlsx" ) as SIGUA_data: #, index=False
    part1_s.to_excel(SIGUA_data, sheet_name="ts1", index=False)
    part2_s.to_excel(SIGUA_data, sheet_name="ts2", index=False)
    part3_s.to_excel(SIGUA_data, sheet_name="ts3", index=False)
    part4_s.to_excel(SIGUA_data, sheet_name="ts4", index=False)
    part5_s.to_excel(SIGUA_data, sheet_name="ts5", index=False)
    SIGUA_data.save()


# In[148]:


sk = Skype('troy60333@gmail.com' , 'sancho160333')
sk.chats.chat('19:d0dd2c705d7241a8befddfbc733aad9e@thread.skype').sendMsg(
'美東時間 : '+ str(ddd_3)+ "\n" )
sk.chats.chat('19:d0dd2c705d7241a8befddfbc733aad9e@thread.skype').sendFile(open("F:/Desktop/download_csv/YABO_data.xlsx", "rb"), "YABO_data.xlsx")
sk.chats.chat('19:d0dd2c705d7241a8befddfbc733aad9e@thread.skype').sendFile(open("F:/Desktop/download_csv/SIGUA_data.xlsx", "rb"), "SIGUA_data.xlsx")


# In[149]:


#結束所有 firefox 瀏覽器
os.system("taskkill /im firefox.exe")


# In[150]:


#sk = Skype('troy60333@gmail.com' , 'sancho160333')
#sk.chats.recent() 

