#!/usr/bin/env python
# coding: utf-8

# In[29]:


import requests
import telepot
import datetime
import time
import pandas as pd
import numpy as np
import random
import os

import datetime
import string
#google sheet 專用
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains


# In[30]:


headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
            }
payload = {
    'username': 'bbbtorin',
    'password': 'qwe123',
}

#帳號密碼
username="bbbtorin" 
passwd="qwe123"
downloadpath="C:/Users/btorin/Desktop/download_csv"
gekodriverpath=r'C:/Users/btorin/Desktop/excuter/geckodriver.exe'
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[31]:


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

# In[14]:


#獲取cookies id
payid=log_in_web('https://yb01.88lard.com/')

headerss = {
'cookie': 'lang=zh-cn; payid='+payid,
#'referer': weblink,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
} 

ddd=(datetime.datetime.now() - datetime.timedelta(days=0)).strftime("%Y-%m-%d") 
ddd_2=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d") 

####登入
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headerss)


# In[17]:


####申請時間####
c_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt111_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt111_2.json()['ret']
    c_data_all_f=c_data_all_f+output_data_f
three_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt222_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt222_2.json()['ret']
    three_data_all_f=three_data_all_f+output_data_f
e_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt333_2.json()['ret']
    e_data_all_f=e_data_all_f+output_data_f
m_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt444_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/crypto/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&display_merge_data=true&first_result="+str(i)+"&max_results=1000" , headers=headerss )
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


# In[20]:


#發送請求
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
##deposite withdraw
#list_data_all=[]
#for i in range(0, 10000, 1000) : 
#    ttt= session_requests.get("https://yb01.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd_2+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00&level_id=599" , headers=headers )
#    output_data=ttt.json()['ret']
#    list_data_all=list_data_all+output_data
#df_all=pd.DataFrame(list_data_all)[['username','user_id','amount']]
#df_all['amount']=df_all['amount'].astype(float)
df_unique_user=pd.DataFrame(df_all.groupby(by=['username','user_id'])['amount'].sum()).reset_index().rename(columns={ "amount": "amount"})


# In[21]:


df_user_infor= pd.DataFrame(columns=['username','user_id','phone','phone_confirm','name','created_at','cash.balance'])

for user_idd in df_unique_user['user_id'] :
    ttt111= session_requests.get("https://yb01.88lard.com/api/v1/player/"+str(user_idd)+"/info" , headers=headers )
    output_data=ttt111.json()['ret']
    if output_data.get('phone',False) == False: output_data['phone']=None 
    if output_data.get('phone_confirm',False) == False: output_data['phone_confirm']=None 
    if output_data.get('name',False) == False: output_data['name']=None 
    df_user_infor=df_user_infor.append(pd.json_normalize(output_data)[['username','user_id','phone','phone_confirm','name','created_at','cash.balance']])


# In[23]:


#時間轉換
df_user_infor['created_at']=(pd.to_datetime(df_user_infor['created_at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")
#随机打乱  寫入新的 index
random_df=df_user_infor.reset_index(drop=True)
#random_df=random_df.sample(frac=1.0)


# In[24]:


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


# In[26]:


random_df=random_df[['username','phone_confirm','created_at']]
part3=random_df.iloc[offices[0]]
part4=random_df.iloc[offices[1]]
part6=random_df.iloc[offices[2]]
part7=random_df.iloc[offices[3]]
part9=random_df.iloc[offices[4]]
part11=random_df.iloc[offices[5]]
part12=random_df.iloc[offices[6]]
part14=random_df.iloc[offices[7]]
part15=random_df.iloc[offices[8]]


# In[ ]:


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly',
      'https://www.googleapis.com/auth/drive',
      'https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1d_5ir6jdHuBsM3KfzBg7yNnaAE7nSKHiMTokNZ_Es24'
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


# In[ ]:


#寫入 data 進入 google sheet #美東時間
def insert_data(value_range_body,sheetname,colname1,colname2,col1,col2) :
    SAMPLE_RANGE_NAME = 'ts'+str(sheetname)+'!'+colname1+str(col1)+':'+colname2+str(col2)
    request= sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption='USER_ENTERED',range=SAMPLE_RANGE_NAME , body=value_range_body).execute()

def clear_data(value_range_body,sheetname,colname1,colname2,col1,col2):
    SAMPLE_RANGE_NAME = 'ts'+str(sheetname)+'!'+colname1+str(col1)+':'+colname2+str(col2)
    request = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute() #, body=value_range_body


# In[ ]:


#分段寫入
abclist=[3,4,6,7,9,11,12,14,15]
alldata=[part3,part4,part6,part7,part9,part11,part12,part14,part15]
j=0
for i in abclist :
    clear_data(value_range_body,i,'A','C',3,300)
    #填入時間
    value_range_body = {"majorDimension":"COLUMNS","values":[[ddd]]}
    insert_data(value_range_body,i,'B','B',1,1)
    #填入資料
    value_range_body = {"majorDimension":"ROWS","values": alldata[j].to_dict('split')['data'] } 
    insert_data(value_range_body,i,'A','C',3,300)
    j=j+1


# # SIGUA

# In[32]:


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
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headerss)


# In[33]:


####申請時間####
c_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt111_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt111_2.json()['ret']
    c_data_all_f=c_data_all_f+output_data_f
three_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt222_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt222_2.json()['ret']
    three_data_all_f=three_data_all_f+output_data_f
e_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt333_2.json()['ret']
    e_data_all_f=e_data_all_f+output_data_f
m_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt444_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/crypto/entry/list?created_at_start="+ddd_2+"T12%3A00%3A00%2B0800&created_at_end="+ddd+"T11%3A59%3A59%2B0800&display_merge_data=true&first_result="+str(i)+"&max_results=1000" , headers=headerss )
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


# In[35]:


#發送請求
LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
##deposite withdraw
#list_data_all=[]
#for i in range(0, 10000, 1000) : #https://sg.88lard.com/api/v1/wallet/invoice/list
#    ttt= session_requests.get("https://sg.88lard.com/api/v1/wallet/invoice/list?submit_start="+ddd_2+"T00%3A00%3A00-04%3A00&submit_end="+ddd+"T23%3A59%3A59-04%3A00&first_result="+str(i)+"&max_results=1000&updated_start="+ddd+"T00%3A00%3A00-04%3A00&updated_end="+ddd+"T23%3A59%3A59-04%3A00&level_id=868" , headers=headers )
#    output_data=ttt.json()['ret']
#    list_data_all=list_data_all+output_data
#df_all=pd.DataFrame(list_data_all)[['username','user_id','amount']]
#df_all['amount']=df_all['amount'].astype(float)
df_unique_user=pd.DataFrame(df_all.groupby(by=['username','user_id'])['amount'].sum()).reset_index().rename(columns={ "amount": "amount"})


# In[36]:


df_user_infor= pd.DataFrame(columns=['username','user_id','phone','phone_confirm','name','created_at','cash.balance'])

jj=0
for user_idd in df_unique_user['user_id'] :
    ttt111= session_requests.get("https://sg.88lard.com/api/v1/player/"+str(user_idd)+"/info" , headers=headers )
    output_data=ttt111.json()['ret']
    if output_data.get('phone',False) == False: output_data['phone']=None 
    if output_data.get('phone_confirm',False) == False: output_data['phone_confirm']=None 
    if output_data.get('name',False) == False: output_data['name']=None 
    df_user_infor=df_user_infor.append(pd.json_normalize(output_data)[['username','user_id','phone','phone_confirm','name','created_at','cash.balance']])
    if jj%200 == 0:
        #發送請求
        session_requests = requests.session()
        response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
    jj=jj+1


# In[38]:


#時間轉換
df_user_infor['created_at']=(pd.to_datetime(df_user_infor['created_at'])+datetime.timedelta(hours=-12)).dt.strftime("%Y-%m-%d %H:%M:%S")
#随机打乱  寫入新的 index
random_df=df_user_infor.reset_index(drop=True)
#random_df=random_df.sample(frac=1.0)


# In[39]:


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


# In[40]:


random_df=random_df[['username','phone_confirm','created_at']]
part1=random_df.iloc[offices[0]]
part2=random_df.iloc[offices[1]]
part3=random_df.iloc[offices[2]]
part4=random_df.iloc[offices[3]]
part5=random_df.iloc[offices[4]]


# In[325]:


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly',
      'https://www.googleapis.com/auth/drive',
      'https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '10R6sKyHpZGo31LZsylWI_W3Sf6rqLchJR1E5fZPJN2s'
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


# In[326]:


#寫入 data 進入 google sheet #美東時間
def insert_data(value_range_body,sheetname,colname1,colname2,col1,col2) :
    SAMPLE_RANGE_NAME = 'ts'+str(sheetname)+'!'+colname1+str(col1)+':'+colname2+str(col2)
    request= sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption='USER_ENTERED',range=SAMPLE_RANGE_NAME , body=value_range_body).execute()

def clear_data(value_range_body,sheetname,colname1,colname2,col1,col2):
    SAMPLE_RANGE_NAME = 'ts'+str(sheetname)+'!'+colname1+str(col1)+':'+colname2+str(col2)
    request = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute() #, body=value_range_body


# In[327]:


#分段寫入
abclist=[1,2,3,4,5]
alldata=[part1,part2,part3,part4,part5]
j=0
for i in abclist :
    clear_data(value_range_body,i,'A','C',3,500)
    #填入時間
    value_range_body = {"majorDimension":"COLUMNS","values":[[ddd]]}
    insert_data(value_range_body,i,'B','B',1,1)
    #填入資料
    value_range_body = {"majorDimension":"ROWS","values": alldata[j].to_dict('split')['data'] } 
    insert_data(value_range_body,i,'A','C',3,500)
    j=j+1


# In[ ]:





# In[42]:


#結束所有 firefox 瀏覽器
os.system("taskkill /im firefox.exe")


# In[ ]:




