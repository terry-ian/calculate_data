#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import telepot
import time


# In[2]:


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


#畫圖 YABO
run_python_file("F:\\Desktop\\pythontest\\python F:\\Desktop\\excuter\\request_data-plot-eastern.py " ,'美東畫圖','plot' )
time.sleep(1)

#畫圖 SIGUA
run_python_file("F:\\Desktop\\pythontest\\python F:\\Desktop\\excuter\\request_data-plot-eastern_sigua.py " ,'美東畫圖','plot' )
time.sleep(1)

#載檔案 YABO
run_python_file("F:\\Desktop\\pythontest\\python F:\\Desktop\\excuter\\download_csv.py " ,'下載檔案','download' )
time.sleep(1)

#計算輸出 YABO
run_python_file("F:\\Desktop\\pythontest\\python F:\\Desktop\\excuter\\pay_count.py " ,'計算檔案','calculate')
time.sleep(1)

#載檔案 SIGUA
run_python_file("F:\\Desktop\\pythontest\\python F:\\Desktop\\excuter\\download_csv_sigua.py " ,'下載檔案','download' )
time.sleep(1)

#計算輸出 SIGUA
run_python_file("F:\\Desktop\\pythontest\\python F:\\Desktop\\excuter\\pay_count_sigua.py " ,'計算檔案','calculate')
time.sleep(1)


# In[3]:


telebot_finish()


# In[ ]:


'''
#各排程执行
def telebot_send_error(bank_name,bank_code):
    bot = telepot.Bot(token=tele_warning_token)
    bot.sendMessage(chat_id=tele_warning_chatid ,text= bank_name+'-程序执行有误log档案如下:')
    bot.sendDocument(chat_id=tele_warning_chatid , document= open("F:\\Desktop\\download_csv\\"+bank_code+".log", "r",encoding = 'utf-8'))


run_python_file("F:\\Desktop\\pythontest\\python F:\\Desktop\\excuter\\pay_count.py > F:\\Desktop\\download_csv\\calculate.log 2>&1" ,'計算檔案','calculate')
time.sleep(1)


'''

