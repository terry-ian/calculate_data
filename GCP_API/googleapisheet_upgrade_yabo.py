#!/usr/bin/env python
# coding: utf-8

# In[434]:


import pandas as pd
import numpy as np
import datetime
import os
import telepot
import requests

import selenium
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains


# In[435]:


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


# In[436]:


#time now 
day = datetime.datetime.now()
today_day=datetime.datetime.now().strftime("%Y-%m-%d")   
delay_oneday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")  
ddd_delayone = (datetime.datetime.now() - datetime.timedelta(days=2)).strftime("%Y-%m-%d")  
#美東時間
ddd=(datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
#login information
LOGIN_URL = 'https://yb01.88lard.com/api/v1/manager/login'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
}
payload = {
    'username': 'bbbtorin',
    'password': 'qwe123',
}

#帳號密碼
username="bbtorin"
passwd="qwe123"
downloadpath='F:/Desktop/download_csv'
gekodriverpath= r'F:/Desktop/python_code/geckodriver.exe'
nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# In[437]:


####登入
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)

####投注資料
ttt_count123 = session_requests.get("https://yb01.88lard.com/api/v1/stats/vendors/game_report?start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00&to_CNY=true" , headers=headers )
wager_platform=ttt_count123.json()['ret']
wager_platform=pd.DataFrame(wager_platform)[['kind','payoff','valid_bet','counts']]
wager_platform[['payoff','valid_bet','counts']]=wager_platform[['payoff','valid_bet','counts']].astype(float)
wager_platform=wager_platform.groupby(['kind']).agg({'payoff':'sum','valid_bet':'sum','counts':'sum'})

#投注人數
wager_dataall= pd.DataFrame(columns=['kind','user_count'])

ttt_count = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&vendor=bbin&vendor=sp&vendor=boe&vendor=crown&vendor=nbb_sport&vendor=ae&vendor=im&kind=1&kind=1&kind=1&kind=1&kind=1&kind=1&kind=1&parentOption=all&first_result=0&max_results=30" , headers=headers )
wager_data=ttt_count.json()['total']
wager_data=pd.DataFrame([wager_data])[['user_count']]
wager_data['kind']=1
wager_dataall=wager_dataall.append(wager_data)

ttt_count = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&vendor=bbin&vendor=ag&vendor=ab&vendor=bg&vendor=evo&vendor=ebet&vendor=lg_live&vendor=mg_live&vendor=sexy&kind=2&kind=2&kind=2&kind=2&kind=2&kind=2&kind=2&kind=2&kind=2&parentOption=all&first_result=0&max_results=30" , headers=headers )
wager_data=ttt_count.json()['total']
wager_data=pd.DataFrame([wager_data])[['user_count']]
wager_data['kind']=2
wager_dataall=wager_dataall.append(wager_data)

ttt_count = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&vendor=bbin&vendor=pt&vendor=jdb&vendor=ag_casino&vendor=mw&vendor=cq9&vendor=pg&vendor=lg_casino&vendor=aw&vendor=mg2&vendor=bng2&vendor=lg_yb_casino&vendor=fc&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&kind=3&parentOption=all&first_result=0&max_results=30" , headers=headers )
wager_data=ttt_count.json()['total']
wager_data=pd.DataFrame([wager_data])[['user_count']]
wager_data['kind']=3
wager_dataall=wager_dataall.append(wager_data)

ttt_count = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&vendor=bbin&vendor=vr&vendor=lg_ly&vendor=allwin&vendor=sigua_ly&kind=4&kind=4&kind=4&kind=4&kind=4&parentOption=all&first_result=0&max_results=30" , headers=headers )
wager_data=ttt_count.json()['total']
wager_data=pd.DataFrame([wager_data])[['user_count']]
wager_data['kind']=4
wager_dataall=wager_dataall.append(wager_data)

ttt_count = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&vendor=ky&vendor=fg&vendor=jdb_card&vendor=mt&vendor=lg_card&vendor=th&vendor=leg&vendor=lg_yb_card&kind=5&kind=5&kind=5&kind=5&kind=5&kind=5&kind=5&kind=5&parentOption=all&first_result=0&max_results=30" , headers=headers )
wager_data=ttt_count.json()['total']
wager_data=pd.DataFrame([wager_data])[['user_count']]
wager_data['kind']=5
wager_dataall=wager_dataall.append(wager_data)

ttt_count = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+ddd+"T00%3A00%3A00-04%3A00&end_at="+ddd+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&vendor=xbb_mj&kind=6&parentOption=all&first_result=0&max_results=30" , headers=headers )
wager_data=ttt_count.json()['total']
wager_data=pd.DataFrame([wager_data])[['user_count']]
wager_data['kind']=6
wager_dataall=wager_dataall.append(wager_data)

####註冊會員數
ttt_count = session_requests.get("https://yb01.88lard.com/api/v1/player/daily_register?created_day="+ddd+"&first_result=0&max_results=20" , headers=headers )
countnewuser=int(ttt_count.json()['pagination']['total'])
new_register_user=[]
for i in range(0, countnewuser, 1000) :   
    ttt_new = session_requests.get("https://yb01.88lard.com/api/v1/player/daily_register?created_day="+ddd+"&first_result="+str(i)+"&max_results=1000" , headers=headers )
    output_data=ttt_new.json()['ret']
    new_register_user=new_register_user+output_data
new_register_user_df=pd.DataFrame(new_register_user)[['username','level']]


# In[438]:


#獲取cookies id
payid=log_in_web('https://yb01.88lard.com/')


# In[439]:


########### 訊付資料
headerss = {
'cookie': 'lang=zh-cn; payid='+payid,
#'referer': weblink,
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
} 
####成功  審核時間
c_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt111_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+today_day+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_s=ttt111_1.json()['ret']
    c_data_all_s=c_data_all_s+output_data_s
three_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt222_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+today_day+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_s=ttt222_1.json()['ret']
    three_data_all_s=three_data_all_s+output_data_s
e_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt333_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+today_day+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_s=ttt333_1.json()['ret']
    e_data_all_s=e_data_all_s+output_data_s
m_data_all_s=[]
for i in range(0, 10000, 1000) :   
    ttt444_1 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/crypto/entry/list?display_merge_data=true&state_at_start="+ddd+"T12%3A00%3A00%2B0800&state_at_end="+today_day+"T11%3A59%3A59%2B0800&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_s=ttt444_1.json()['ret']
    m_data_all_s=m_data_all_s+output_data_s

####失敗  申請時間
c_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt111_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/remit/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+today_day+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt111_2.json()['ret']
    c_data_all_f=c_data_all_f+output_data_f
three_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt222_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/deposit/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+today_day+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt222_2.json()['ret']
    three_data_all_f=three_data_all_f+output_data_f
e_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt333_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/wallet/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+today_day+"T11%3A59%3A59%2B0800&sort=id&order=desc&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt333_2.json()['ret']
    e_data_all_f=e_data_all_f+output_data_f
m_data_all_f=[]
for i in range(0, 10000, 1000) :   
    ttt444_2 = session_requests.get("https://a.inpay-pro.com/api/trade/v1/crypto/entry/list?created_at_start="+ddd+"T12%3A00%3A00%2B0800&created_at_end="+today_day+"T11%3A59%3A59%2B0800&display_merge_data=true&first_result="+str(i)+"&max_results=1000" , headers=headerss )
    output_data_f=ttt444_2.json()['ret']
    m_data_all_f=m_data_all_f+output_data_f

#轉換成dataframe 
def changetodataframe(df,currency=1):
    if len(df)==0 :
        output=pd.DataFrame(columns=['会员帐号','会员层级','支付类型','存入状态','存入情況','申请金额','首存','操作端'])
    elif currency==0 :
        output=pd.DataFrame(df)[['username','level_name','bank_name','confirm','complete','amount','first','browser']]
        output.columns = ['会员帐号','会员层级','支付类型','存入状态','存入情況','申请金额','首存','操作端']
        output['申请金额']=output['申请金额'].astype('float')
    elif currency==2 :
        output=pd.DataFrame(df)[['username','level_name','type_name','gateway_name','merchant_alias','confirm','complete','amount','first','browser']]
        output.columns = ['会员帐号','会员层级','支付类型','第三方平台','后台代称','存入状态','存入情況','申请金额','首存','操作端']
        output['申请金额']=output['申请金额'].astype('float')
    else:
        output=pd.DataFrame(df)[['username','level_name','type_name','confirm','complete','amount','first','browser']]
        output.columns = ['会员帐号','会员层级','支付类型','存入状态','存入情況','申请金额','首存','操作端']
        output['申请金额']=output['申请金额'].astype('float')
    return(output)

register_deposite_c=changetodataframe(c_data_all_s)
register_deposite_3=changetodataframe(three_data_all_s,2)
register_deposite_e=changetodataframe(e_data_all_s)
register_deposite_m=changetodataframe(m_data_all_s,0)
register_deposite_3d=changetodataframe(three_data_all_f,2)
register_deposite_ed=changetodataframe(e_data_all_f)
register_deposite_md=changetodataframe(m_data_all_f,0)

# ((register_deposite_3["存入状态"] == False) & (register_deposite_3["存入情況"] == False))


# # 各支付方式統計

# In[440]:


list_item = ['手机支付-成功笔数','手机支付-失败笔数','手机支付-总比数','手机支付-成功金额','手机支付-成功率',
            '在线支付-成功笔数','在线支付-失败笔数','在线支付-总比数','在线支付-成功金额','在线支付-成功率',
            '扫码支付-成功笔数','扫码支付-失败笔数','扫码支付-总比数','扫码支付-成功金额','扫码支付-成功率',
            '公司入款-成功笔数','公司入款-失败笔数','公司入款-总比数','公司入款-成功金额','公司入款-成功率',
            '代客充值-成功笔数','代客充值-总比数','代客充值-成功金额','代客充值-成功率',
            '电子钱包入款-成功笔数','电子钱包入款-失败笔数','电子钱包入款-总比数','电子钱包入款-成功金额','电子钱包入款-成功率',
            '加密货币入款-成功笔数','加密货币入款-失败笔数','加密货币入款-总比数','加密货币入款-成功金额','加密货币入款-成功率']
list_time = [delay_oneday]
all_dataframe_data= pd.DataFrame(columns=list_time,index=list_item)


# In[441]:


#'------------------------手机支付' 手機支付 
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True) & ((register_deposite_3["支付类型"] == "手机支付") | (register_deposite_3["支付类型"] == "手機支付")) ]
cdata22_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('測試')) & ((register_deposite_3d["存入状态"] == False) & (register_deposite_3d["存入情況"] == False)) & ((register_deposite_3d["支付类型"] == "手机支付") | (register_deposite_3d["支付类型"] == "手機支付")) ]
unique_user_s=cdata22_s['会员帐号']
unique_user_f=cdata22_f['会员帐号']
unique_amount_s=cdata22_s['申请金额']
unique_amount_f=cdata22_f['申请金额']
all_dataframe_data.iloc[0]=len(unique_user_s)
all_dataframe_data.iloc[1]=len(unique_user_f)
all_dataframe_data.iloc[2]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[3]=round(sum(unique_amount_s))
all_dataframe_data.iloc[4]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[442]:


#'------------------------在线支付' 在線支付
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True) & ((register_deposite_3["支付类型"] == "在线支付")|(register_deposite_3["支付类型"] == "在線支付")) & (register_deposite_3["第三方平台"] != "JJ代客充值")]
cdata22_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('測試')) & ((register_deposite_3d["存入状态"] == False) & (register_deposite_3d["存入情況"] == False)) & ((register_deposite_3d["支付类型"] == "在线支付")|(register_deposite_3d["支付类型"] == "在線支付")) & (register_deposite_3d["第三方平台"] != "JJ代客充值")]
unique_user_s=cdata22_s['会员帐号'] 
unique_user_f=cdata22_f['会员帐号']
unique_amount_s=cdata22_s['申请金额']
unique_amount_f=cdata22_f['申请金额']
all_dataframe_data.iloc[5]=len(unique_user_s)
all_dataframe_data.iloc[6]=len(unique_user_f)
all_dataframe_data.iloc[7]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[8]=round(sum(unique_amount_s))
all_dataframe_data.iloc[9]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[443]:


#'------------------------扫码支付' 掃碼支付
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True) & ((register_deposite_3["支付类型"] == "扫码支付")|(register_deposite_3["支付类型"] == "掃碼支付"))]
cdata22_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('測試')) & ((register_deposite_3d["存入状态"] == False) & (register_deposite_3d["存入情況"] == False)) & ((register_deposite_3d["支付类型"] == "扫码支付")|(register_deposite_3d["支付类型"] == "掃碼支付"))]
unique_user_s=cdata22_s['会员帐号']
unique_user_f=cdata22_f['会员帐号']
unique_amount_s=cdata22_s['申请金额']
unique_amount_f=cdata22_f['申请金额']
all_dataframe_data.iloc[10]=len(unique_user_s)
all_dataframe_data.iloc[11]=len(unique_user_f)
all_dataframe_data.iloc[12]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[13]=round(sum(unique_amount_s))
all_dataframe_data.iloc[14]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[444]:


#'------------------------公司入款'
cdata11_s=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & (register_deposite_c["存入状态"] == True)]
cdata11_f=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & ((register_deposite_c["存入状态"] == False) & (register_deposite_c["存入情況"] == True))]
unique_user_s=cdata11_s['会员帐号']
unique_user_f=cdata11_f['会员帐号']
unique_amount_s=cdata11_s['申请金额']
unique_amount_f=cdata11_f['申请金额']
all_dataframe_data.iloc[15]=len(unique_user_s)
all_dataframe_data.iloc[16]=len(unique_user_f)
all_dataframe_data.iloc[17]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[18]=round(sum(unique_amount_s))
all_dataframe_data.iloc[19]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[445]:


#'------------------------代客充值'
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True) & ((register_deposite_3["支付类型"] == "在线支付")|(register_deposite_3["支付类型"] == "在線支付")) & (register_deposite_3["第三方平台"] == "JJ代客充值")]
unique_user_s=cdata22_s['会员帐号']
unique_amount_s=cdata22_s['申请金额']
all_dataframe_data.iloc[20]=len(unique_user_s)
all_dataframe_data.iloc[21]=len(unique_user_s)
all_dataframe_data.iloc[22]=round(sum(unique_amount_s))
all_dataframe_data.iloc[23]= 0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)) * 100 ,2)


# In[446]:


#'------------------------电子钱包入款'
cdata33_s=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('測試')) & (register_deposite_e["存入状态"] == True)]
cdata33_f=register_deposite_ed[(~register_deposite_ed['会员层级'].str.contains('測試')) & ((register_deposite_ed["存入状态"] == False) & (register_deposite_ed["存入情況"] == False))]
unique_user_s=cdata33_s['会员帐号']
unique_user_f=cdata33_f['会员帐号']
unique_amount_s=cdata33_s['申请金额']
unique_amount_f=cdata33_f['申请金额']
all_dataframe_data.iloc[24]=len(unique_user_s)
all_dataframe_data.iloc[25]=len(unique_user_f)
all_dataframe_data.iloc[26]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[27]=round(sum(unique_amount_s))
all_dataframe_data.iloc[28]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[447]:


#'------------------------加密货币入款'
cdata44_s=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('測試')) & (register_deposite_m["存入状态"] == True)]
cdata44_f=register_deposite_md[(~register_deposite_md['会员层级'].str.contains('測試')) & ((register_deposite_md["存入状态"] == False) & (register_deposite_md["存入情況"] == False))]
unique_user_s=cdata44_s['会员帐号']
unique_user_f=cdata44_f['会员帐号']
unique_amount_s=cdata44_s['申请金额']
unique_amount_f=cdata44_f['申请金额']
all_dataframe_data.iloc[29]=len(unique_user_s)
all_dataframe_data.iloc[30]=len(unique_user_f)
all_dataframe_data.iloc[31]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[32]=round(sum(unique_amount_s))
all_dataframe_data.iloc[33]=0 if (len(unique_user_s)+len(unique_user_f)) == 0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# # 金額區間/支付方式

# In[448]:


#創建dataframe
list_item_3 = ['三方-失敗','三方-成功','公司-失敗','公司-成功','電子-失敗','電子-成功','加密-失敗','加密-成功']
list_time_3 = ['50-199','200-999','1000-2999','3000-4999','5000up']
pay_dataframe_data= pd.DataFrame(columns=list_time_3,index=list_item_3)


# In[449]:


#公司 # 
cdata222_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True )]
cdata222_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('測試')) & ((register_deposite_3d["存入状态"] == False) & (register_deposite_3d["存入情況"] == False)) & (register_deposite_3d["第三方平台"] != "JJ代客充值")]
cdata111_s=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & (register_deposite_c["存入状态"] == True)]
cdata111_f=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & ((register_deposite_c["存入状态"] == False) & (register_deposite_c["存入情況"] == True))]
cdata333_s=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('測試')) & (register_deposite_e["存入状态"] == True)]
cdata333_f=register_deposite_ed[(~register_deposite_ed['会员层级'].str.contains('測試')) & ((register_deposite_ed["存入状态"] == False) & (register_deposite_ed["存入情況"] == False))]
cdata444_s=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('測試')) & (register_deposite_m["存入状态"] == True)]
cdata444_f=register_deposite_md[(~register_deposite_md['会员层级'].str.contains('測試')) & ((register_deposite_md["存入状态"] == False) & (register_deposite_md["存入情況"] == False))]

all_data_test=[cdata222_f,cdata222_s,cdata111_f,cdata111_s,cdata333_f,cdata333_s,cdata444_f,cdata444_s]

j=0
for all_data in all_data_test:
    count_frq_50 = 0 ; count_frq_200 = 0 ; count_frq_1000 = 0 ; count_frq_3000 = 0 ; count_frq_5000 = 0 
    for i in range(all_data.shape[0]):
        if all_data['申请金额'].iloc[i]>=50 and all_data['申请金额'].iloc[i]<200 :
            count_frq_50 += 1
        elif all_data['申请金额'].iloc[i]>=200 and all_data['申请金额'].iloc[i]<1000 :
            count_frq_200 += 1
        elif all_data['申请金额'].iloc[i]>=1000 and all_data['申请金额'].iloc[i]<3000 :
            count_frq_1000 += 1
        elif all_data['申请金额'].iloc[i]>=3000 and all_data['申请金额'].iloc[i]<5000 :
            count_frq_3000 += 1
        else :
            count_frq_5000 += 1
    
    pay_dataframe_data.iloc[j]=[count_frq_50,count_frq_200,count_frq_1000,count_frq_3000,count_frq_5000]
    j+=1


# # 數據1資料表

# In[450]:


#登入
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
#反水
ttt = session_requests.get("https://yb01.88lard.com/api/v1/rebate/event/list?first_result=0&max_results=20&frequency=2&start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00" , headers=headers )
output_data=ttt.json()['ret']
try :
    df_rebet =pd.DataFrame(output_data)[['name','total']]
except :
    df_rebet = pd.DataFrame({'name':['rebet'],'total':[0]})
#有效投注損益  #today_day
ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/daily_report?start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00" , headers=headers )
output_data=ttt.json()['ret']
df_total_data=pd.DataFrame(output_data).T[['valid_bet','payoff']]

#總餘額
ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/daily_report?start_at="+str(today_day)+"T00%3A00%3A00-04%3A00&end_at="+str(today_day)+"T23%3A59%3A59-04%3A00" , headers=headers )
output_data=ttt.json()['ret']
df_total_balance=pd.DataFrame(output_data).T[['total_balance']]

#測試帳號撈取
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
list_data_all=[]
for k in range(0,15000,1000): 
    ttt = session_requests.get("https://yb01.88lard.com/api/v1/player/list?level=581&first_result="+str(k)+"&max_results=1000&fields=enable&fields=username" , headers=headers )
    output_data=ttt.json()['ret']
    list_data_all=list_data_all+output_data
test_user=pd.DataFrame(list_data_all)[['username','enable']]

#計算有效投注人數
ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=20" , headers=headers )
output_data=ttt.json()['ret']
parent_id=pd.DataFrame(output_data)[['parent_id','user_count']]

total_list=[]
list_data_all=[]
for i in range(parent_id.shape[0]) : 
    p_id=parent_id.iloc[i,0]
    u_count=parent_id.iloc[i,1]
    list_data_all=[]
    for j in range(0,int(u_count),1000): 
        ttt = session_requests.get("https://yb01.88lard.com/api/v1/stats/agent/"+str(p_id)+"/children/wager_report?start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00&canceled=0&first_result="+str(j)+"&max_results=1000&currency=&to_CNY=true" , headers=headers )
        output_data=ttt.json()['ret']
        list_data_all=list_data_all+output_data
    total_list=total_list+list_data_all
all_bet_user=pd.DataFrame(total_list)[['username','counts']]

formal_user_bet=pd.merge(all_bet_user,test_user,on = 'username',how = 'left')
user_bet_total=formal_user_bet[~(formal_user_bet['enable']==True)]


# In[451]:


######################################################  數據1  ###############################################
list_item_123 = ['註冊會員數','首次充值人数','首次充值总金额','代客充值系統首次充值人數','安卓系统首次充值人数(数据群)',
            'IOS系统首次充值人数(数据群)','平均首次充值金额','注册转化率','当日充值总人数','有效投注总人数',
            '当日洗码量(投注额)','当日返水金额','当日派彩(损益)','累计派彩','所有会员总余额',
            '充值成功率% (数据组)','安卓系统充值成功率(数据群)','IOS系统充值成功率(数据群)','当日有效充值通道几个(CT组)','成功充值共几笔(数据组)',
            '失败充值共几笔(数据组)','成功最大一笔多少钱(数据组)','成功充值金额 ','失败充值金额 ',
            '当日提款金额 (结算组)','充提差金额 (结算组)','入款手续费 (结算组)','代付手续费 (结算组)','银行互转手续费',
            '当日盈利','当日新增有效代理数 (代理部)','代理商总数 (代理部)','存款订单总共几笔']
list_time_123 = [delay_oneday]
dataframe_count= pd.DataFrame(columns=list_time_123,index=list_item_123)

#註冊會員數
count_register_user=new_register_user_df.shape[0]
dataframe_count.iloc[0]=count_register_user

#首次充值人数
#公司
new_user_c=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & (register_deposite_c["首存"] == True)]
count_user1=new_user_c.shape[0]
sum_price1=sum(new_user_c['申请金额'])
#第三方
new_user_3=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["首存"] == True) ]
count_user2=new_user_3.shape[0]
sum_price2=sum(new_user_3['申请金额'])
#電子錢包
new_user_e=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('測試')) & (register_deposite_e["首存"] == True)]
count_user3=new_user_e.shape[0]
sum_price3=sum(new_user_e['申请金额'])
#加密貨幣
new_user_m=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('測試')) & (register_deposite_m["首存"] == True)]
count_user4=new_user_m.shape[0]
sum_price4=sum(new_user_m['申请金额'])


dataframe_count.iloc[1]=count_user2+count_user3
dataframe_count.iloc[2]=sum_price2+sum_price3

#代客充值系統首次充值人數
new_user_help=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["首存"] == True) & (register_deposite_3["第三方平台"] == "JJ代客充值")] 
count_user_help=new_user_help.shape[0]
dataframe_count.iloc[3]=count_user_help


# In[452]:


#安卓人 #| and_user[i] in 'Windows' | and_user[i] in '马甲'
new_user_33=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["首存"] == True) & (register_deposite_3["第三方平台"] != "JJ代客充值")]
and_user=new_user_c['操作端'].append(new_user_33['操作端']).append(new_user_e['操作端'])
count_frq_and = 0 ; count_frq_ios = 0 
for ai in and_user:
    if  'Android' in ai :  
        count_frq_and += 1
    else:
        count_frq_ios += 1

#安卓系统首次充值人数
dataframe_count.iloc[4]=count_frq_and
#IOS系统首次充值人数
dataframe_count.iloc[5]=count_frq_ios

#平均首次充值金额
dataframe_count.iloc[6]= round((sum_price2+sum_price3)/(count_user2+count_user3) ,2)
#注册转化率
dataframe_count.iloc[7]= round((count_user2+count_user3) / count_register_user  *100 ,2)
#当日充值总人数
now_deposite1=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & (register_deposite_c["存入状态"] == True)]
now_deposite2=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True)]
now_deposite3=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('測試')) & (register_deposite_e["存入状态"] == True)]
now_deposite4=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('測試')) & (register_deposite_m["存入状态"] == True)]
unique_user=now_deposite1['会员帐号'].append(now_deposite2['会员帐号']).append(now_deposite3['会员帐号']).append(now_deposite4['会员帐号'])
unique_user_now=len(np.unique(unique_user))
dataframe_count.iloc[8]= unique_user_now
#有效投注总人数
#count_p_b=len(np.unique(betamount_count_p[(betamount_count_p['会员层级'] != '測試帳號')]['会员帐号']))  
dataframe_count.iloc[9]=user_bet_total.shape[0]


# In[453]:


#当日洗码量
dataframe_count.iloc[10]=round(float(df_total_data.iloc[0,0]),2)
#当日返水金额
dataframe_count.iloc[11]=round(float(df_rebet.iloc[0,1]),2)
#当日派彩(损益)
dataframe_count.iloc[12]=round(float(df_total_data.iloc[0,1]),2)*-1
#当日派彩(损益)
dataframe_count.iloc[13]='加上昨天'
#所有会员总余额
dataframe_count.iloc[14]=round(float(df_total_balance.iloc[0,0]),2)


# In[454]:


#'充值成功率% (数据组)',   扣除加密貨幣 !!!  +all_dataframe_data.iloc[31,0]
sss=(all_dataframe_data.iloc[0,0]+all_dataframe_data.iloc[5,0]+all_dataframe_data.iloc[10,0]+all_dataframe_data.iloc[15,0]+all_dataframe_data.iloc[24,0] )
sss_total=(all_dataframe_data.iloc[2,0]+all_dataframe_data.iloc[7,0]+all_dataframe_data.iloc[12,0]+all_dataframe_data.iloc[17,0]+all_dataframe_data.iloc[26,0])
dataframe_count.iloc[15]=round(sss / sss_total * 100 ,2)

#'安卓系统充值成功率(数据群)',
cdata11_s_platform=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & (register_deposite_c["存入状态"] == True)] 
cdata11_f_platform=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('測試')) & ((register_deposite_c["存入状态"] == False) & (register_deposite_c["存入情況"] == True))]

cdata22_s_platform=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True) & (register_deposite_3["第三方平台"] != 'JJ代客充值')]
cdata22_f_platform=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('測試')) & ((register_deposite_3d["存入状态"] == False) & (register_deposite_3d["存入情況"] == False)) & (register_deposite_3d["第三方平台"] != "JJ代客充值")]

cdata33_s_platform=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('測試')) & (register_deposite_e["存入状态"] == True)]
cdata33_f_platform=register_deposite_ed[(~register_deposite_ed['会员层级'].str.contains('測試')) & ((register_deposite_ed["存入状态"] == False) & (register_deposite_ed["存入情況"] == False))]

cdata44_s_platform=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('測試')) & (register_deposite_m["存入状态"] == True)]
cdata44_f_platform=register_deposite_md[(~register_deposite_md['会员层级'].str.contains('測試')) & ((register_deposite_md["存入状态"] == False) & (register_deposite_md["存入情況"] == False))]

#成功
and_user_s=cdata11_s_platform['操作端'].append(cdata22_s_platform['操作端']).append(cdata33_s_platform['操作端'])
count_frq_and_s = 0 ; count_frq_ios_s = 0 
for ai in and_user_s:
    if  'Android' in ai :  
        count_frq_and_s += 1
    else:

        count_frq_ios_s += 1
#失敗
and_user_f=cdata11_f_platform['操作端'].append(cdata22_f_platform['操作端']).append(cdata33_f_platform['操作端'])
count_frq_and_f = 0 ; count_frq_ios_f = 0 
for ai in and_user_f:
    if  'Android' in ai :  
        count_frq_and_f += 1
    else:

        count_frq_ios_f += 1

dataframe_count.iloc[16]=round(count_frq_and_s/(count_frq_and_s+count_frq_and_f) *100 , 2)

#'IOS系统充值成功率(数据群)',
dataframe_count.iloc[17]=round(count_frq_ios_s/(count_frq_ios_s+count_frq_ios_f) *100 , 2)

#'当日有效充值通道几个(CT组)',
dataframe_count.iloc[18]='請查詢'

#'成功充值共几笔(数据组)'
dataframe_count.iloc[19]=len(and_user_s)

#'失败充值共几笔(数据组)',
dataframe_count.iloc[20]=len(and_user_f)

#'成功最大一笔多少钱(数据组
cdata22_s_platform_max=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('測試')) & (register_deposite_3["存入状态"] == True)]
cdata22_f_platform_max=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('測試')) & ((register_deposite_3d["存入状态"] == False) & (register_deposite_3d["存入情況"] == False))]

dataframe_count.iloc[21]=max(cdata11_s_platform['申请金额'].append(cdata22_s_platform_max['申请金额']).append(cdata33_s_platform['申请金额']))

#'成功充值金额 '
dataframe_count.iloc[22]=sum(cdata11_s_platform['申请金额'].append(cdata22_s_platform['申请金额']).append(cdata33_s_platform['申请金额'])) + all_dataframe_data.iloc[22]

#'失败充值金额 '
dataframe_count.iloc[23]=sum(cdata11_f_platform['申请金额'].append(cdata22_f_platform['申请金额']).append(cdata33_f_platform['申请金额']))

#未給值欄位
dataframe_count.iloc[24]='請查詢'
dataframe_count.iloc[25]='請查詢'
dataframe_count.iloc[26]='請查詢'
dataframe_count.iloc[27]='請查詢'
dataframe_count.iloc[28]='請查詢'
dataframe_count.iloc[29]='請查詢'
dataframe_count.iloc[30]='請查詢'
dataframe_count.iloc[31]='請查詢'

#'存款订单总共几笔'
dataframe_count.iloc[32]=dataframe_count.iloc[19]+dataframe_count.iloc[20]


# # 各平台占比

# In[455]:


wager_dataall=pd.merge(wager_dataall,wager_platform,on = 'kind',how = 'left')
wager_dataall['payoff']=round(wager_dataall['payoff'].astype(float),2)*-1
wager_dataall['valid_bet']=round(wager_dataall['valid_bet'].astype(float),2)
wager_dataall['user_count']=round(wager_dataall['user_count'].astype(float),2)
wager_dataall['counts']=round(wager_dataall['counts'].astype(float),2)
wager_dataall=wager_dataall[['payoff','valid_bet','user_count','counts']]
#wager_dataall=wager_dataall.groupby(['kind']).agg({'payoff':'sum','valid_bet':'sum','user_count':'sum','count':'sum'})


# # 填寫到 google sheet

# In[456]:


import datetime
import string

#google sheet 專用
from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


# In[457]:


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly',
      'https://www.googleapis.com/auth/drive',
      'https://www.googleapis.com/auth/spreadsheets']

SAMPLE_SPREADSHEET_ID = '1jaVBKWc44aoS_6tJgMJ6AJRP0JM7fz5DrnbyVGcV5sA'
"""Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
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

def google_sheet_api_date(datetime_eastern,sheetname):
    #找出全部日期對應
    #SAMPLE_SPREADSHEET_ID = '1WvchqW0qPnHcS1Kexo1uCIJtfE9MCsbwuLL9gm2kFGY'
    SAMPLE_RANGE_NAME = sheetname+'!A1:AJ1'
    result = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    datetime123=result.get('values')[0]
    
    #找出日期欄位
    datetimeindex=datetime123.index(datetime_eastern)
    abclist=list(string.ascii_uppercase)
    abclist=abclist+['AA','AB','AC','AD','AE','AF','AG','AH','AI','AJ']
    sheetname=abclist[datetimeindex]
    
    return( sheetname )


# # 數據一

# In[458]:


#寫入 data 進入 google sheet #美東時間
datetime_eastern = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%m/%d")  
sheetname=google_sheet_api_date(datetime_eastern,'数据-1')
def insert_data(value_range_body,sheetname,col1,col2) :
    SAMPLE_RANGE_NAME = '数据-1!'+sheetname+str(col1)+':'+sheetname+str(col2)
    request= sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption='USER_ENTERED',range=SAMPLE_RANGE_NAME , body=value_range_body).execute()


# In[459]:


#分段寫入
value_range_body = {"majorDimension":"COLUMNS","values":[[dataframe_count.iloc[0,0]]]}
insert_data(value_range_body,sheetname,3,3)

value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ dataframe_count.iloc[2,0],dataframe_count.iloc[3,0],dataframe_count.iloc[4,0],dataframe_count.iloc[5,0]]]}
insert_data(value_range_body,sheetname,5,8)

value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ dataframe_count.iloc[8,0],dataframe_count.iloc[9,0],dataframe_count.iloc[10,0]
                               ,dataframe_count.iloc[11,0],dataframe_count.iloc[12,0] ]]}
insert_data(value_range_body,sheetname,11,15)

value_range_body = {"majorDimension":"COLUMNS","values":[[ dataframe_count.iloc[14,0] ]]}
insert_data(value_range_body,sheetname,17,17)

value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ str(dataframe_count.iloc[16,0])+'%',str(dataframe_count.iloc[17,0])+'%' ]]}
insert_data(value_range_body,sheetname,19,20)

value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ dataframe_count.iloc[19,0],dataframe_count.iloc[20,0],dataframe_count.iloc[21,0]
                               ,dataframe_count.iloc[22,0],dataframe_count.iloc[23,0] ]]}
insert_data(value_range_body,sheetname,22,26)


# # 各平台占比

# In[460]:


#寫入 data 進入 google sheet #美東時間
datetime_eastern = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%#m/%#d")  
sheetname=google_sheet_api_date(datetime_eastern,'各平台占比')
def insert_data(value_range_body,sheetname,col1,col2) :
    SAMPLE_RANGE_NAME = '各平台占比!'+sheetname+str(col1)+':'+sheetname+str(col2)
    request= sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption='USER_ENTERED',range=SAMPLE_RANGE_NAME , body=value_range_body).execute()


# In[461]:


#分段寫入  #1 體育 2 視訊 3電子 4 彩票 5棋牌  6麻將
value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ wager_dataall.iloc[0,0],wager_dataall.iloc[1,0],wager_dataall.iloc[2,0]
                               ,wager_dataall.iloc[3,0],wager_dataall.iloc[4,0],wager_dataall.iloc[5,0] ]]}
insert_data(value_range_body,sheetname,4,9)

value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ wager_dataall.iloc[0,1],wager_dataall.iloc[1,1],wager_dataall.iloc[2,1]
                               ,wager_dataall.iloc[3,1],wager_dataall.iloc[4,1],wager_dataall.iloc[5,1] ]]}
insert_data(value_range_body,sheetname,11,16)

value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ wager_dataall.iloc[0,2],wager_dataall.iloc[1,2],wager_dataall.iloc[2,2]
                               ,wager_dataall.iloc[3,2],wager_dataall.iloc[4,2],wager_dataall.iloc[5,2] ]]}
insert_data(value_range_body,sheetname,18,23)

value_range_body = {"majorDimension":"COLUMNS",
                    "values":[[ wager_dataall.iloc[0,3],wager_dataall.iloc[1,3],wager_dataall.iloc[2,3]
                               ,wager_dataall.iloc[3,3],wager_dataall.iloc[4,3],wager_dataall.iloc[5,3] ]]}
insert_data(value_range_body,sheetname,25,30)


# # 金額區間/支付方式

# In[462]:


def google_sheet_api_date(datetime_eastern,sheetname):
    #找出全部日期對應
    #SAMPLE_SPREADSHEET_ID = '1WvchqW0qPnHcS1Kexo1uCIJtfE9MCsbwuLL9gm2kFGY'
    SAMPLE_RANGE_NAME = sheetname+'!A1:A40'
    result = sheet.values().get(
        spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    datetime123=result.get('values')  
    datetime123=datetime123.index([datetime_eastern])+1
    return( datetime123 )


# In[463]:


#寫入 data 進入 google sheet #美東時間
datetime_eastern = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%#m/%#d")  
sheetnumber=google_sheet_api_date(datetime_eastern,'金額區間/支付方式')
def insert_data(value_range_body,sheetnumber,col1,col2) :
    SAMPLE_RANGE_NAME = '金額區間/支付方式!'+col1+str(sheetnumber)+':'+col2+str(sheetnumber)
    request= sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption='USER_ENTERED',range=SAMPLE_RANGE_NAME , body=value_range_body).execute()


# In[464]:


value_range_body = {"majorDimension":"ROWS",
                    "values":[[ pay_dataframe_data.iloc[0,0],pay_dataframe_data.iloc[0,1],pay_dataframe_data.iloc[0,2]
                               ,pay_dataframe_data.iloc[0,3],pay_dataframe_data.iloc[0,4]
                               ,pay_dataframe_data.iloc[1,0],pay_dataframe_data.iloc[1,1],pay_dataframe_data.iloc[1,2]
                               ,pay_dataframe_data.iloc[1,3],pay_dataframe_data.iloc[1,4]
                              ]]}
insert_data(value_range_body,sheetnumber,'B','K')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ pay_dataframe_data.iloc[2,0],pay_dataframe_data.iloc[2,1],pay_dataframe_data.iloc[2,2]
                               ,pay_dataframe_data.iloc[2,3],pay_dataframe_data.iloc[2,4]
                               ,pay_dataframe_data.iloc[3,0],pay_dataframe_data.iloc[3,1],pay_dataframe_data.iloc[3,2]
                               ,pay_dataframe_data.iloc[3,3],pay_dataframe_data.iloc[3,4]
                              ]]}
insert_data(value_range_body,sheetnumber,'N','W')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ pay_dataframe_data.iloc[4,0],pay_dataframe_data.iloc[4,1],pay_dataframe_data.iloc[4,2]
                               ,pay_dataframe_data.iloc[4,3],pay_dataframe_data.iloc[4,4]
                               ,pay_dataframe_data.iloc[5,0],pay_dataframe_data.iloc[5,1],pay_dataframe_data.iloc[5,2]
                               ,pay_dataframe_data.iloc[5,3],pay_dataframe_data.iloc[5,4]
                              ]]}
insert_data(value_range_body,sheetnumber,'Z','AI')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ pay_dataframe_data.iloc[6,0],pay_dataframe_data.iloc[6,1],pay_dataframe_data.iloc[6,2]
                               ,pay_dataframe_data.iloc[6,3],pay_dataframe_data.iloc[6,4]
                               ,pay_dataframe_data.iloc[7,0],pay_dataframe_data.iloc[7,1],pay_dataframe_data.iloc[7,2]
                               ,pay_dataframe_data.iloc[7,3],pay_dataframe_data.iloc[7,4]
                              ]]}
insert_data(value_range_body,sheetnumber,'AL','AU')


# # 各支付方式统计

# In[465]:


#寫入 data 進入 google sheet #美東時間
datetime_eastern = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y/%#m/%#d")  
sheetnumber=google_sheet_api_date(datetime_eastern,'各支付方式统计')
def insert_data(value_range_body,sheetnumber,col1,col2) :
    SAMPLE_RANGE_NAME = '各支付方式统计!'+col1+str(sheetnumber)+':'+col2+str(sheetnumber)
    request= sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,valueInputOption='USER_ENTERED',range=SAMPLE_RANGE_NAME , body=value_range_body).execute()


# In[466]:


#手機
value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[0,0],all_dataframe_data.iloc[1,0] ]]}
insert_data(value_range_body,sheetnumber,'B','C')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[3,0]]]}
insert_data(value_range_body,sheetnumber,'E','E')

#在線支付
value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[5,0],all_dataframe_data.iloc[6,0] ]]}
insert_data(value_range_body,sheetnumber,'G','H')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[8,0]]]}
insert_data(value_range_body,sheetnumber,'J','J')

#掃碼支付
value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[10,0],all_dataframe_data.iloc[11,0] ]]}
insert_data(value_range_body,sheetnumber,'L','M')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[13,0]]]}
insert_data(value_range_body,sheetnumber,'O','O')

#公司入款
value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[15,0],all_dataframe_data.iloc[16,0] ]]}
insert_data(value_range_body,sheetnumber,'Q','R')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[18,0]]]}
insert_data(value_range_body,sheetnumber,'T','T')

#代客充值
value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[20,0] ]]}
insert_data(value_range_body,sheetnumber,'V','V')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[22,0]]]}
insert_data(value_range_body,sheetnumber,'X','X')

#電子錢包
value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[24,0],all_dataframe_data.iloc[25,0] ]]}
insert_data(value_range_body,sheetnumber,'Z','AA')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[27,0]]]}
insert_data(value_range_body,sheetnumber,'AC','AC')

#加密貨幣
value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[29,0],all_dataframe_data.iloc[30,0] ]]}
insert_data(value_range_body,sheetnumber,'AE','AF')

value_range_body = {"majorDimension":"ROWS",
                    "values":[[ all_dataframe_data.iloc[32,0]]]}
insert_data(value_range_body,sheetnumber,'AH','AH')


# In[467]:


os.system("taskkill /im firefox.exe")


# In[ ]:




