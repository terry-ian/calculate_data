#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import telepot
import time


# In[ ]:


#參數
#warning message 
tele_warning_chatid='-418327801'
tele_warning_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'

#執行cmd指令
def run_python_file(cmdtext,bankname,bankcode):
    ret=os.system(cmdtext)
    #if ret!=0 : telebot_send_error(bankname,bankcode)
#完成今日爬虫作业
def telebot_finish():
    timenow=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    bot = telepot.Bot(token=tele_warning_token)
    bot.sendMessage(chat_id=tele_warning_chatid ,text= timenow+' - 美東時間計算完成')


# In[ ]:


#計算輸出 YABO
run_python_file("C:\\Users\\btorin\\AppData\\Local\\Programs\\Python\\Python38\\python C:\\Users\\btorin\\Desktop\\excuter\\googleapisheet_upgrade_yabo.py " ,'計算檔案','calculate')
time.sleep(1)
#

#計算輸出 SIGUA
run_python_file("C:\\Users\\btorin\\AppData\\Local\\Programs\\Python\\Python38\\python C:\\Users\\btorin\\Desktop\\excuter\\googleapisheet_upgrade_sigua.py " ,'計算檔案','calculate')
time.sleep(1)

# In[ ]:
telebot_finish()

import sys
sys.exit()

