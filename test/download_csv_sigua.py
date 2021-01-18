#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
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
delay_oneday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")


# In[4]:


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
fp.set_preference("browser.download.dir", "F:\Desktop\download_csv_sigua") 
options = Options()
options.add_argument('--headless')
options.binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
browser = webdriver.Firefox(executable_path=r'F:\Desktop\python_code\geckodriver.exe', options=options,firefox_profile = fp)
browser.maximize_window()
browser.get('https://sg.88lard.com/')
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


# In[5]:


#下載今日註冊會員
browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div[3]/div[2]/a/div').click()
browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[1]/div[3]/div[3]/div/div[2]/a').click()
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/form/div/div[1]/div/div/input').click()
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[3]/span/a[1]').click()
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/form/div/div[4]/button').click()
time.sleep(3)
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[3]/div/button').click()

#VIP
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[1]/div[3]/div[3]/div/div[4]/a').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[1]/div[1]/a[2]').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div[1]/button[2]').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div').click()

browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/div[2]/div[2]/span').click()

time.sleep(2)
browser.find_element_by_xpath('//*[@id="app"]/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[2]/div/i').click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/form/div/div[4]/button').click()
time.sleep(2)
browser.find_element_by_xpath('/html/body/div/div[1]/div[2]/div[2]/div/div[3]/div[2]/div/div[1]/div[2]/button[2]').click()

#下載今日存款  #載入時間為昨天時間  要過中午12點後再操作
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[3]/div[4]/a/div').click()
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[3]/div[5]/div/div[1]/a').click()
browser.find_element_by_xpath('//*[@id="date"]').click()
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]').click()
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[2]/div/a[2]').click()
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[1]/form/div/div[4]/button').click()
time.sleep(3)
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div[2]/button').click()

#下載今日出款  #載入時間為昨天時間  要過中午12點後再操作
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[1]/div[3]/div[5]/div/div[3]/a').click()
browser.find_element_by_xpath('//*[@id="date"]').click()
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div[2]').click()
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div[2]/div/a[2]').click()
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div/div[1]/form/div/div[4]/button').click()
time.sleep(3)
browser.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div[2]/div/div/div/div[4]/button').click()


# In[6]:


#點選進入迅付
browser.find_element_by_class_name('item.sidebar-tab.extension-menu').click()
time.sleep(1)
browser.find_element_by_xpath('//div[@class="sidebar-text"][text()="迅付"]').click() 
time.sleep(1) 


# In[7]:


#換分頁
browser1=browser.window_handles[1]
browser.switch_to_window(browser1) 


# In[8]:


#抵達會員入款訊息 
time.sleep(5)
browser.find_element_by_link_text('会员入款').click()


# # 成功 使用審核時間

# In[9]:


#分頁 '公司入款' 只有審核時間  
time.sleep(2)
list_deposite=['/html/body/div/div[2]/div/div/div/ul/li[2]','/html/body/div/div[2]/div/div/div/ul/li[4]','/html/body/div/div[2]/div/div/div/ul/li[6]']


# In[10]:


#### 公司入款 第三方入款 電子錢包入款  ####
for c_deposite in list_deposite:
    #更換頁簽
    browser.find_element_by_xpath(c_deposite).click()
    #打開下拉霸
    time.sleep(2)
    browser.find_element_by_class_name('sc-fznNTe.fnbSrb').click()
    time.sleep(2)
    #清除現有時間   
    menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[0]
    ActionChains(browser).move_to_element(menu).click().perform()
    time.sleep(2)
    if len(browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")) != 0 :
        menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[1]
        ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
    try :
        #審核時間(起)  
        browser.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div/div[1]/form/div[3]/span/div/input').click()
        time.sleep(1) 
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[1]/div/input').send_keys(delay_oneday)
        time.sleep(1) 
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
        time.sleep(1) 
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[13]').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
        time.sleep(1)
        #審核時間((迄)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/form/div[4]/span/div/input').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[1]').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/form/div[4]/span/div/input').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[12]').click()
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[60]').click()
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]/ul/li[60]').click()
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="queryBtn"]').click()
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/button[3]').click()
        time.sleep(6)
    except : 
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[1]/div/input').send_keys(delay_oneday)
        time.sleep(1) 
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
        time.sleep(1) 
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[13]').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
        time.sleep(1)
        #審核時間((迄) 
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/form/div[4]/span/div/input').click()
        time.sleep(1) 
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[3]/span/a[1]').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/form/div[4]/span/div/input').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
        time.sleep(1)
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[12]').click()
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[60]').click()
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]/ul/li[60]').click()
        browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
        time.sleep(3)
        browser.find_element_by_xpath('//*[@id="queryBtn"]').click()
        time.sleep(3)
        browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/button[3]').click()
        time.sleep(6)


# In[11]:


##########   加密貨幣   #############
#更換頁簽
browser.find_element_by_xpath('/html/body/div/div[2]/div/div/div/ul/li[8]').click()
#打開下拉霸
time.sleep(2)
browser.find_element_by_class_name('sc-fznNTe.fnbSrb').click()
time.sleep(2)
#清除現有時間   
menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[0]
ActionChains(browser).move_to_element(menu).click().perform()
time.sleep(2)
if len(browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")) != 0 :
    menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[1]
    ActionChains(browser).move_to_element(menu).click().perform()
    time.sleep(2)
try :
    #審核時間(起)   
    browser.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div/div[1]/div[1]/div[3]/span/div/input').click()
    time.sleep(1)   
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[1]/div/input').send_keys(delay_oneday)
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[13]').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
    time.sleep(1)
    #審核時間((迄)
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[4]/span/div/input').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[1]').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[4]/span/div/input').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[12]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[60]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]/ul/li[60]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="queryBtn"]').click()
    time.sleep(3)
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/button[2]').click()
    time.sleep(6)
except : 
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[1]/div/input').send_keys(delay_oneday)
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[13]').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
    time.sleep(1)
    #審核時間((迄) 
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[4]/span/div/input').click()
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[3]/span/a[1]').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[4]/span/div/input').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
    time.sleep(1)
    browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[12]').click()
    browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[60]').click()
    browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]/ul/li[60]').click()
    browser.find_element_by_xpath('/html/body/div[4]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="queryBtn"]').click()
    time.sleep(3)
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/button[2]').click()
    time.sleep(6) 


# # 失敗  使用申請時間 

# In[12]:


#############   失敗  ################
time.sleep(2)
list_deposite_f=['/html/body/div/div[2]/div/div/div/ul/li[4]','/html/body/div/div[2]/div/div/div/ul/li[6]']

for c_deposite in list_deposite_f:
    #更換頁簽
    browser.find_element_by_xpath(c_deposite).click()
    #打開下拉霸
    time.sleep(2)
    browser.find_element_by_class_name('sc-fznNTe.fnbSrb').click()
    time.sleep(2)
    #清除現有時間   
    menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[0]
    ActionChains(browser).move_to_element(menu).click().perform()
    time.sleep(2)
    if len(browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")) != 0 :
        menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[1]
        ActionChains(browser).move_to_element(menu).click().perform()
        time.sleep(2)
    #申請時間(起)   
    browser.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div/div[1]/form/div[1]/span/div/input').click()
    time.sleep(1)    
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[1]/div/input').send_keys(delay_oneday)
    time.sleep(1)  
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
    time.sleep(1)  
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[13]').click()
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
    time.sleep(1)
    #申請時間(迄) 
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/form/div[2]/span/div/input').click()
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[1]').click()
    time.sleep(1)  
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/form/div[2]/span/div/input').click()
    time.sleep(1)  
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
    time.sleep(1) 
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[12]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[60]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]/ul/li[60]').click()
    browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
    time.sleep(3)
    browser.find_element_by_xpath('//*[@id="queryBtn"]').click()
    time.sleep(3)
    browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/button[3]').click()
    time.sleep(6)  


# In[13]:


########## 失敗 加密貨幣   #################
browser.find_element_by_xpath('/html/body/div/div[2]/div/div/div/ul/li[8]').click()
#打開下拉霸
time.sleep(2)
browser.find_element_by_class_name('sc-fznNTe.fnbSrb').click()
time.sleep(2)
#清除現有時間   
menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[0]
ActionChains(browser).move_to_element(menu).click().perform()
time.sleep(2)
if len(browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")) != 0 :
    menu = browser.find_elements_by_css_selector("[aria-label='icon: close-circle']")[1]
    ActionChains(browser).move_to_element(menu).click().perform()
    time.sleep(2)

browser.find_element_by_xpath('/html/body/div/div[2]/div/div/div/div/div[1]/div[1]/div[1]/span/div/input').click()
time.sleep(1)  
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[1]/div/input').send_keys(delay_oneday)
time.sleep(1) 
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
time.sleep(1) 
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[13]').click()
time.sleep(1)
browser.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
time.sleep(1)
#審核時間((迄) 
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/span/div/input').click()
time.sleep(1)
browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[1]').click()
time.sleep(1) 
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[1]/div[1]/div[2]/span/div/input').click()
time.sleep(1)
browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[3]/span/a[2]').click()
time.sleep(1)
browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[1]/ul/li[12]').click()
browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/ul/li[60]').click()
browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[3]/ul/li[60]').click()
browser.find_element_by_xpath('/html/body/div[3]/div/div/div/div/div[2]/div[4]/span/a[3]').click()
time.sleep(3)
browser.find_element_by_xpath('//*[@id="queryBtn"]').click()
time.sleep(3)
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/button[2]').click()
time.sleep(6)


# In[14]:


browser.close()
browser.switch_to_window(browser.window_handles[0]) 
browser.close()


# In[15]:


import os 
os.system("taskkill /im firefox.exe")


# In[ ]:




