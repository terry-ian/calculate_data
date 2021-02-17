#!/usr/bin/env python
# coding: utf-8

# In[73]:


import pandas as pd
import numpy as np
import datetime
import os
import telepot
import requests


# In[74]:


#time now 
day = datetime.datetime.now()
today_day=datetime.datetime.now().strftime("%Y-%m-%d")   
delay_oneday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")   
#open csv file  
#註冊會員數
register_user = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/daily_register.csv", encoding = "utf-8") # header=None skiprows = 1

#成功  審核時間
register_deposite_c = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/公司入款纪录.csv" , encoding = "utf-8")
register_deposite_3 = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/第三方入款纪录.csv", encoding = "utf-8")
register_deposite_e = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/电子钱包入款纪录.csv" , encoding = "utf-8")
register_deposite_m = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/加密货币入款纪录.csv" , encoding = "utf-8")

#失敗  申請時間
register_deposite_3d = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/第三方入款纪录(1).csv", encoding = "utf-8")
register_deposite_ed = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/电子钱包入款纪录(1).csv" , encoding = "utf-8")
register_deposite_md = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/加密货币入款纪录(1).csv" , encoding = "utf-8")

#檢查存款細項
deposite_user = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/deposit_invoice_entries.csv", encoding = "utf-8")
withdraw_user = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/withdraw_entries.csv", encoding = "utf-8")

#VIP客源
vipList = pd.read_csv("C:/Users/btorin/Desktop/download_csv_sigua/vipList.csv", encoding = "utf-8")

#有效投注總人數
#betamount_count_p = pd.read_csv("F:/Downloads/2020_12_03_02_11_55.csv", encoding = "utf-8")


# In[75]:


LOGIN_URL = 'https://sg.88lard.com/api/v1/manager/login'
headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
            'accept-language': 'zh-TW'
}
payload = {
    'username': 'bbtorin',
    'password': 'qwe123',
}


# # 各支付方式統計

# In[76]:


list_item = ['手机支付-成功笔数','手机支付-失败笔数','手机支付-总比数','手机支付-成功金额','手机支付-成功率',
            '在线支付-成功笔数','在线支付-失败笔数','在线支付-总比数','在线支付-成功金额','在线支付-成功率',
            '扫码支付-成功笔数','扫码支付-失败笔数','扫码支付-总比数','扫码支付-成功金额','扫码支付-成功率',
            '公司入款-成功笔数','公司入款-失败笔数','公司入款-总比数','公司入款-成功金额','公司入款-成功率',
            '代客充值-成功笔数','代客充值-总比数','代客充值-成功金额','代客充值-成功率',
            '电子钱包入款-成功笔数','电子钱包入款-失败笔数','电子钱包入款-总比数','电子钱包入款-成功金额','电子钱包入款-成功率',
            '加密货币入款-成功笔数','加密货币入款-失败笔数','加密货币入款-总比数','加密货币入款-成功金额','加密货币入款-成功率']
list_time = [delay_oneday]
all_dataframe_data= pd.DataFrame(columns=list_time,index=list_item)


# In[77]:


#'------------------------手机支付' 手機支付
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"') & ((register_deposite_3["支付类型"] == '="手机支付"') | (register_deposite_3["支付类型"] == '="手機支付"')) ]
cdata22_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('测试')) & (register_deposite_3d["存入状态"] == '="未送单"') & ((register_deposite_3d["支付类型"] == '="手机支付"') | (register_deposite_3d["支付类型"] == '="手機支付"')) ]
unique_user_s=cdata22_s['会员帐号']
unique_user_f=cdata22_f['会员帐号']
unique_amount_s=cdata22_s['申请金额']
unique_amount_f=cdata22_f['申请金额']
all_dataframe_data.iloc[0]=len(unique_user_s)
all_dataframe_data.iloc[1]=len(unique_user_f)
all_dataframe_data.iloc[2]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[3]=round(sum(unique_amount_s))
all_dataframe_data.iloc[4]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[78]:


#'------------------------在线支付' 在線支付
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"') & ((register_deposite_3["支付类型"] == '="在线支付"')|(register_deposite_3["支付类型"] == '="在線支付"')) & (register_deposite_3["第三方平台"] != '="JJ代客充值"')]
cdata22_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('测试')) & (register_deposite_3d["存入状态"] == '="未送单"') & ((register_deposite_3d["支付类型"] == '="在线支付"')|(register_deposite_3d["支付类型"] == '="在線支付"')) & (register_deposite_3d["第三方平台"] != '="JJ代客充值"')]
unique_user_s=cdata22_s['会员帐号']
unique_user_f=cdata22_f['会员帐号']
unique_amount_s=cdata22_s['申请金额']
unique_amount_f=cdata22_f['申请金额']
all_dataframe_data.iloc[5]=len(unique_user_s)
all_dataframe_data.iloc[6]=len(unique_user_f)
all_dataframe_data.iloc[7]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[8]=round(sum(unique_amount_s))
all_dataframe_data.iloc[9]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[79]:


#'------------------------扫码支付' 掃碼支付
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"') & ((register_deposite_3["支付类型"] == '="扫码支付"')|(register_deposite_3["支付类型"] == '="掃碼支付"'))]
cdata22_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('测试')) & (register_deposite_3d["存入状态"] == '="未送单"') & ((register_deposite_3d["支付类型"] == '="扫码支付"')|(register_deposite_3d["支付类型"] == '="掃碼支付"'))]
unique_user_s=cdata22_s['会员帐号']
unique_user_f=cdata22_f['会员帐号']
unique_amount_s=cdata22_s['申请金额']
unique_amount_f=cdata22_f['申请金额']
all_dataframe_data.iloc[10]=len(unique_user_s)
all_dataframe_data.iloc[11]=len(unique_user_f)
all_dataframe_data.iloc[12]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[13]=round(sum(unique_amount_s))
all_dataframe_data.iloc[14]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[80]:


#'------------------------公司入款'
cdata11_s=register_deposite_c[(register_deposite_c['会员层级'] != '="测试账号"') & (register_deposite_c["存入状态"] == '="已入帐"')]
cdata11_f=register_deposite_c[(register_deposite_c['会员层级'] != '="测试账号"') & (register_deposite_c["存入状态"] != '="已入帐"')]
unique_user_s=cdata11_s['会员帐号']
unique_user_f=cdata11_f['会员帐号']
unique_amount_s=cdata11_s['申请金额']
unique_amount_f=cdata11_f['申请金额']
all_dataframe_data.iloc[15]=len(unique_user_s)
all_dataframe_data.iloc[16]=len(unique_user_f)
all_dataframe_data.iloc[17]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[18]=round(sum(unique_amount_s))
all_dataframe_data.iloc[19]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[81]:


#'------------------------代客充值'
cdata22_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"') & ((register_deposite_3["支付类型"] == '="在线支付"')|(register_deposite_3["支付类型"] == '="在線支付"')) & (register_deposite_3["第三方平台"] == '="JJ代客充值"')]
unique_user_s=cdata22_s['会员帐号']
unique_amount_s=cdata22_s['申请金额']
all_dataframe_data.iloc[20]=len(unique_user_s)
all_dataframe_data.iloc[21]=len(unique_user_s)
all_dataframe_data.iloc[22]=round(sum(unique_amount_s))
all_dataframe_data.iloc[23]= 0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)) * 100 ,2)


# In[82]:


#'------------------------电子钱包入款'
cdata33_s=register_deposite_e[(register_deposite_e['会员层级'] != '="测试账号"') & (register_deposite_e["存入状态"] == '="已入帐"')]
cdata33_f=register_deposite_ed[(register_deposite_ed['会员层级'] != '="测试账号"') & (register_deposite_ed["存入状态"] != '="已入帐"')]
unique_user_s=cdata33_s['会员帐号']
unique_user_f=cdata33_f['会员帐号']
unique_amount_s=cdata33_s['申请金额']
unique_amount_f=cdata33_f['申请金额']
all_dataframe_data.iloc[24]=len(unique_user_s)
all_dataframe_data.iloc[25]=len(unique_user_f)
all_dataframe_data.iloc[26]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[27]=round(sum(unique_amount_s))
all_dataframe_data.iloc[28]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# In[83]:


#'------------------------加密货币入款'
cdata44_s=register_deposite_m[(register_deposite_m['会员层级'] != '="测试账号"') & (register_deposite_m["存入状态"] == '="已入帐"')]
cdata44_f=register_deposite_md[(register_deposite_md['会员层级'] != '="测试账号"') & (register_deposite_md["存入状态"] != '="已入帐"')]
unique_user_s=cdata44_s['会员帐号']
unique_user_f=cdata44_f['会员帐号']
unique_amount_s=cdata44_s['申请金额']
unique_amount_f=cdata44_f['申请金额']
all_dataframe_data.iloc[29]=len(unique_user_s)
all_dataframe_data.iloc[30]=len(unique_user_f)
all_dataframe_data.iloc[31]=len(unique_user_s)+len(unique_user_f)
all_dataframe_data.iloc[32]=round(sum(unique_amount_s))
all_dataframe_data.iloc[33]=0 if len(unique_user_s)==0 else round(len(unique_user_s)/(len(unique_user_s)+len(unique_user_f)) * 100 ,2)


# # 金額區間/支付方式

# In[84]:


#創建dataframe
list_item_3 = ['三方-失敗','三方-成功','公司-失敗','公司-成功','電子-失敗','電子-成功','加密-失敗','加密-成功']
list_time_3 = ['50-199','200-999','1000-2999','3000-4999','5000up']
pay_dataframe_data= pd.DataFrame(columns=list_time_3,index=list_item_3)


# In[85]:


#公司 #
cdata222_s=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"' )]
cdata222_f=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('测试')) & (register_deposite_3d["存入状态"] == '="未送单"') & (register_deposite_3d["第三方平台"] != '="JJ代客充值"')]
cdata111_s=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('测试')) & (register_deposite_c["存入状态"] == '="已入帐"')]
cdata111_f=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('测试')) & (register_deposite_c["存入状态"] != '="已入帐"')]
cdata333_s=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('测试')) & (register_deposite_e["存入状态"] == '="已入帐"')]
cdata333_f=register_deposite_ed[(~register_deposite_ed['会员层级'].str.contains('测试')) & (register_deposite_ed["存入状态"] != '="已入帐"')]
cdata444_s=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('测试')) & (register_deposite_m["存入状态"] == '="已入帐"')]
cdata444_f=register_deposite_md[(~register_deposite_md['会员层级'].str.contains('测试')) & (register_deposite_md["存入状态"] != '="已入帐"')]

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

# In[86]:


#登入
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
#反水
ttt = session_requests.get("https://sg.88lard.com/api/v1/rebate/event/list?first_result=0&max_results=20&frequency=2&start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00" , headers=headers )
output_data=ttt.json()['ret']
try :
    df_rebet =pd.DataFrame(output_data)[['name','total']]
except :
    df_rebet = pd.DataFrame({'name':['rebet'],'total':[0]})

#有效投注損益  #today_day
ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/daily_report?start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00" , headers=headers )
output_data=ttt.json()['ret']
df_total_data=pd.DataFrame(output_data).T[['valid_bet','payoff']]

#總餘額
ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/daily_report?start_at="+str(today_day)+"T00%3A00%3A00-04%3A00&end_at="+str(today_day)+"T23%3A59%3A59-04%3A00" , headers=headers )
output_data=ttt.json()['ret']
df_total_balance=pd.DataFrame(output_data).T[['total_balance']]

#测试账号撈取
session_requests = requests.session()
response = session_requests.request('PUT',url=LOGIN_URL, data=payload, headers=headers)
ttt = session_requests.get("https://sg.88lard.com/api/v1/player/list?level=797&enable=1&first_deposit=3&country_code=0&search=user&first_result=0&max_results=20&sort=id&order=desc&use_cache=true&fields=bankrupt&fields=blacklist&fields=cash&fields=enable&fields=id&fields=last_city_id&fields=last_country&fields=last_ip&fields=last_login&fields=last_online&fields=level&fields=locked&fields=parent&fields=tied&fields=username&fields=upper" , headers=headers )
output_data=ttt.json()['ret']
test_user=pd.DataFrame(output_data)[['username','enable']]

#計算有效投注人數
ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/agents/wager_report?canceled=0&start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00&timeOption=at&currency=&to_CNY=true&specify=0&=&=&=&parentOption=all&first_result=0&max_results=20" , headers=headers )
output_data=ttt.json()['ret']
parent_id=pd.DataFrame(output_data)[['parent_id','user_count']]

total_list=[]
list_data_all=[]
for i in range(parent_id.shape[0]) : 
    p_id=parent_id.iloc[i,0]
    u_count=parent_id.iloc[i,1]
    list_data_all=[]
    for j in range(0,int(u_count),1000): 
        ttt = session_requests.get("https://sg.88lard.com/api/v1/stats/agent/"+str(p_id)+"/children/wager_report?start_at="+str(delay_oneday)+"T00%3A00%3A00-04%3A00&end_at="+str(delay_oneday)+"T23%3A59%3A59-04%3A00&canceled=0&first_result="+str(j)+"&max_results=1000&currency=&to_CNY=true" , headers=headers )
        output_data=ttt.json()['ret']
        list_data_all=list_data_all+output_data
    total_list=total_list+list_data_all
all_bet_user=pd.DataFrame(total_list)[['username','counts']]

formal_user_bet=pd.merge(all_bet_user,test_user,on = 'username',how = 'left')
user_bet_total=formal_user_bet[~(formal_user_bet['enable']==True)]


# In[87]:


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
count_register_user=register_user.shape[0]
dataframe_count.iloc[0]=count_register_user

#首次充值人数
#公司
new_user_c=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('测试')) & (register_deposite_c["首存"] == '="Y"')]
count_user1=new_user_c.shape[0]
sum_price1=sum(new_user_c['申请金额'])
#第三方
new_user_3=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["首存"] == '="Y"')]
count_user2=new_user_3.shape[0]
sum_price2=sum(new_user_3['申请金额'])
#電子錢包
new_user_e=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('测试')) & (register_deposite_e["首存"] == '="Y"')]
count_user3=new_user_e.shape[0]
sum_price3=sum(new_user_e['申请金额'])
#加密貨幣
new_user_m=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('测试')) & (register_deposite_m["首存"] == '="Y"')]
count_user4=new_user_m.shape[0]
sum_price4=sum(new_user_m['申请金额'])


dataframe_count.iloc[1]=count_user2+count_user3
dataframe_count.iloc[2]=sum_price2+sum_price3

#代客充值系統首次充值人數
new_user_help=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["首存"] == '="Y"') & (register_deposite_3["第三方平台"] == '="JJ代客充值"')] #
count_user_help=new_user_help.shape[0]
dataframe_count.iloc[3]=count_user_help


# In[88]:


#安卓人 #| and_user[i] in 'Windows' | and_user[i] in '马甲'
new_user_33=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["首存"] == '="Y"') & (register_deposite_3["第三方平台"] != '="JJ代客充值"')]
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
now_deposite1=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('测试')) & (register_deposite_c["存入状态"] == '="已入帐"')]
now_deposite2=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"')]
now_deposite3=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('测试')) & (register_deposite_e["存入状态"] == '="已入帐"')]
now_deposite4=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('测试')) & (register_deposite_m["存入状态"] == '="已入帐"')]
unique_user=now_deposite1['会员帐号'].append(now_deposite2['会员帐号']).append(now_deposite3['会员帐号']).append(now_deposite4['会员帐号'])
unique_user_now=len(np.unique(unique_user))
dataframe_count.iloc[8]= unique_user_now
#有效投注总人数
#count_p_b=len(np.unique(betamount_count_p[(betamount_count_p['会员层级'] != '测试账号')]['会员帐号']))  
dataframe_count.iloc[9]=user_bet_total.shape[0]


# In[89]:


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


# In[90]:


#'安卓系统充值成功率(数据群)',
cdata11_s_platform=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('测试')) & (register_deposite_c["存入状态"] == '="已入帐"')]
cdata11_f_platform=register_deposite_c[(~register_deposite_c['会员层级'].str.contains('测试')) & (register_deposite_c["存入状态"] == '="已取消"')]

cdata22_s_platform=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"') & (register_deposite_3["第三方平台"] != '="JJ代客充值"')]
cdata22_f_platform=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('测试')) & (register_deposite_3d["存入状态"] == '="未送单"') & (register_deposite_3d["第三方平台"] != '="JJ代客充值"')]

cdata33_s_platform=register_deposite_e[(~register_deposite_e['会员层级'].str.contains('测试')) & (register_deposite_e["存入状态"] == '="已入帐"')]
cdata33_f_platform=register_deposite_ed[(~register_deposite_ed['会员层级'].str.contains('测试')) & (register_deposite_ed["存入状态"] == '="未送单"')]

cdata44_s_platform=register_deposite_m[(~register_deposite_m['会员层级'].str.contains('测试')) & (register_deposite_m["存入状态"] == '="已入帐"')]
cdata44_f_platform=register_deposite_md[(~register_deposite_md['会员层级'].str.contains('测试')) & (register_deposite_md["存入状态"] == '="未送单"')]

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
cdata22_s_platform_max=register_deposite_3[(~register_deposite_3['会员层级'].str.contains('测试')) & (register_deposite_3["存入状态"] == '="已入帐"')]
cdata22_f_platform_max=register_deposite_3d[(~register_deposite_3d['会员层级'].str.contains('测试')) & (register_deposite_3d["存入状态"] == '="未送单"')]

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

#'充值成功率% (数据组)',   扣除加密貨幣 !!!  +all_dataframe_data.iloc[31,0]
sss=dataframe_count.iloc[19].astype(float)
sss_total=dataframe_count.iloc[19].astype(float)+dataframe_count.iloc[20].astype(float)
dataframe_count.iloc[15]=round(sss / sss_total * 100 ,2)

#'存款订单总共几笔'
dataframe_count.iloc[32]=dataframe_count.iloc[19]+dataframe_count.iloc[20]


# # 異常數據

# In[91]:


#除錯用   公司入款  第三方入款 電子錢包  加密貨幣  代客充值
list_item_321 = ['總成功次數','總失敗次數','總成功金額','總失敗金額']
list_time_321 = ['公司入款' , '第三方入款','電子錢包','加密貨幣','代客充值']
test_different_seposite = pd.DataFrame(columns=list_item_321,index=list_time_321)
test_different_seposite.iloc[0,0]=cdata11_s_platform.shape[0]
test_different_seposite.iloc[0,2]=sum(cdata11_s_platform['申请金额'])
test_different_seposite.iloc[0,1]=cdata11_f_platform.shape[0]
test_different_seposite.iloc[0,3]=sum(cdata11_f_platform['申请金额'])
test_different_seposite.iloc[1,0]=cdata22_s_platform.shape[0]
test_different_seposite.iloc[1,2]=sum(cdata22_s_platform['申请金额'])
test_different_seposite.iloc[1,1]=cdata22_f_platform.shape[0]
test_different_seposite.iloc[1,3]=sum(cdata22_f_platform['申请金额'])
test_different_seposite.iloc[2,0]=cdata33_s_platform.shape[0]
test_different_seposite.iloc[2,2]=sum(cdata33_s_platform['申请金额'])
test_different_seposite.iloc[2,1]=cdata33_f_platform.shape[0]
test_different_seposite.iloc[2,3]=sum(cdata33_f_platform['申请金额'])
test_different_seposite.iloc[3,0]=cdata44_s_platform.shape[0]
test_different_seposite.iloc[3,2]=sum(cdata44_s_platform['申请金额'])
test_different_seposite.iloc[3,1]=cdata44_f_platform.shape[0]
test_different_seposite.iloc[3,3]=sum(cdata44_f_platform['申请金额'])
test_different_seposite.iloc[4,0]=all_dataframe_data.iloc[21].values[0]
test_different_seposite.iloc[4,2]=all_dataframe_data.iloc[22].values[0]
test_different_seposite.iloc[4,1]=0
test_different_seposite.iloc[4,3]=0


# In[104]:


#########  今日註冊存提差   ########   今日註冊账号今日出入款
deposite_user=deposite_user[ (deposite_user['状态']=='通过')]
deposite_cg=pd.DataFrame(deposite_user[deposite_user['存款方式']=='CGPay'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "CGPay"})
deposite_usdt=pd.DataFrame(deposite_user[deposite_user['存款方式']=='USDT(ERC20)'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "USDT"})
deposite_company=pd.DataFrame(deposite_user[deposite_user['存款方式']=='公司入款'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "公司入款"})
deposite_go=pd.DataFrame(deposite_user[deposite_user['存款方式']=='购宝钱包'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "购宝钱包"})
deposite_give=pd.DataFrame(deposite_user[deposite_user['存款方式']=='转让充值(A)'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "转让充值"})
deposite_3=pd.DataFrame(deposite_user[deposite_user['存款方式']=='第三方入款'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "第三方入款"})

deposite_user_data=pd.merge(pd.DataFrame(np.unique(register_user['会员帐号'].astype(str)), columns=["会员帐号"] ) ,deposite_cg,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_usdt,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_company,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_go,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_give,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_3,on = '会员帐号',how = 'left')

deposite_user_data=deposite_user_data.fillna(0)
deposite_user_data=pd.DataFrame(deposite_user_data.groupby(by=['会员帐号']).sum()).reset_index()
deposite_user_data['入款加總']=deposite_user_data.iloc[:,1]+deposite_user_data.iloc[:,2]+deposite_user_data.iloc[:,3]+deposite_user_data.iloc[:,4]+deposite_user_data.iloc[:,5]+deposite_user_data.iloc[:,6]

# 檢查取款細項

withdraw_user_first=withdraw_user[ (withdraw_user['出款状态']=='成功')]  #(withdraw_user['首次出款']=='首次出款') &
today_withdraw=pd.DataFrame(withdraw_user_first.groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "出款加總"})

user_n_d_w=pd.merge(deposite_user_data,today_withdraw,on = '会员帐号',how = 'left').fillna(0)
user_n_d_w['存提差']=user_n_d_w.iloc[:,7]-user_n_d_w.iloc[:,8]

final_user_n_d_w=user_n_d_w[user_n_d_w["存提差"]< 0].sort_values(by=['存提差'])
#final_user_n_d_w.to_csv('F:/Downloads/problem_user_new.csv' ,encoding="utf_8_sig" )


# # 會員存提差

# In[105]:


#########  今日所有會員存提差   ########   今日創建账号今日出入款 入款扣除轉讓充值
deposite_user=deposite_user[ (deposite_user['状态']=='通过')]
deposite_cg=pd.DataFrame(deposite_user[deposite_user['存款方式']=='CGPay'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "CGPay"})
deposite_usdt=pd.DataFrame(deposite_user[deposite_user['存款方式']=='USDT(ERC20)'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "USDT"})
deposite_company=pd.DataFrame(deposite_user[deposite_user['存款方式']=='公司入款'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "公司入款"})
deposite_go=pd.DataFrame(deposite_user[deposite_user['存款方式']=='购宝钱包'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "购宝钱包"})
deposite_give=pd.DataFrame(deposite_user[deposite_user['存款方式']=='转让充值(A)'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "转让充值"})
deposite_3=pd.DataFrame(deposite_user[deposite_user['存款方式']=='第三方入款'].groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "第三方入款"})

deposite_user_data=pd.merge(pd.DataFrame(np.unique(deposite_user['会员帐号']), columns=["会员帐号"] ) ,deposite_cg,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_usdt,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_company,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_go,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_give,on = '会员帐号',how = 'left')
deposite_user_data=pd.merge(deposite_user_data,deposite_3,on = '会员帐号',how = 'left')

deposite_user_data=deposite_user_data.fillna(0)
deposite_user_data=pd.DataFrame(deposite_user_data.groupby(by=['会员帐号']).sum()).reset_index()
deposite_user_data['入款加總']=deposite_user_data.iloc[:,1]+deposite_user_data.iloc[:,2]+deposite_user_data.iloc[:,3]+deposite_user_data.iloc[:,4]+deposite_user_data.iloc[:,5]+deposite_user_data.iloc[:,6]

# 檢查取款細項

withdraw_user_first=withdraw_user[ (withdraw_user['出款状态']=='成功')]  #(withdraw_user['首次出款']=='首次出款') &
today_withdraw=pd.DataFrame(withdraw_user_first.groupby(by=['会员帐号'])['申请金额'].sum()).reset_index().rename(columns={ "申请金额": "出款加總"})

user_n_d_w=pd.merge(deposite_user_data,today_withdraw,on = '会员帐号',how = 'left').fillna(0)
user_n_d_w['存提差(扣轉讓充值)']=user_n_d_w.iloc[:,7]-user_n_d_w.iloc[:,8]-user_n_d_w.iloc[:,5]  #扣除代客充值

final_user_all_d_w=user_n_d_w.sort_values(by=['存提差(扣轉讓充值)'])  #[user_n_d_w["存提差(扣轉讓充值)"]< 0]

#final_user_all_d_w.to_csv('F:/Downloads/problem_user_all.csv' ,encoding="utf_8_sig" )


# In[107]:


vipList=vipList[['会员帐号','VIP特权','累积流水金额(开站日起算)','累积输赢']]
vipList['累积流水金额(开站日起算)']=vipList['累积流水金额(开站日起算)'].astype(str).str.replace("=","").str.replace('"',"")
vipList['累积输赢']=vipList['累积输赢'].astype(str).str.replace("=","").str.replace('"',"")
today_alluser_dw=pd.merge(final_user_all_d_w,vipList,on = '会员帐号',how = 'left')
today_alluser_dw['VIP特权'] = today_alluser_dw['VIP特权'].fillna("VIP 0") 
today_alluser_dw = today_alluser_dw.fillna("無資料")
#today_alluser_dw.to_csv('F:/Desktop/download_csv/test.csv' ,encoding="utf_8_sig" )


# # 每小時統計入款方式

# In[108]:


# 時間段存入金額   (每小時統計)
hour_deposite_user=deposite_user[['会员帐号','存款方式','申请时间','申请金额']]
hour_deposite_user['申请时间']=hour_deposite_user['申请时间'].str[13:15]
all_hour_deposite_user=pd.DataFrame(hour_deposite_user.groupby(by=['会员帐号','申请时间']).agg({'申请金额': ['sum','count']})).reset_index().rename(columns={ "申请金额": "出款加總"})
all_hour_deposite_user.columns = ['会员帐号','申请时间','出款加總','出款次數']

method_hour_deposite_user=pd.DataFrame(hour_deposite_user.groupby(by=['会员帐号','存款方式','申请时间']).agg({'申请金额': ['sum','count']})).reset_index().rename(columns={ "申请金额": "出款加總"})
method_hour_deposite_user.columns = ['会员帐号', '存款方式', '申请时间','出款加總','出款次數']

#group by 各種入款
cgpay_hour_deposite_user=method_hour_deposite_user[method_hour_deposite_user['存款方式']=='CGPay'][['会员帐号','申请时间','出款加總','出款次數']]
usdt_hour_deposite_user=method_hour_deposite_user[method_hour_deposite_user['存款方式']=='USDT(ERC20)'][['会员帐号','申请时间','出款加總','出款次數']]
conpany_hour_deposite_user=method_hour_deposite_user[method_hour_deposite_user['存款方式']=='公司入款'][['会员帐号','申请时间','出款加總','出款次數']]
go_hour_deposite_user=method_hour_deposite_user[method_hour_deposite_user['存款方式']=='购宝钱包'][['会员帐号','申请时间','出款加總','出款次數']]
change_hour_deposite_user=method_hour_deposite_user[method_hour_deposite_user['存款方式']=='转让充值(A)'][['会员帐号','申请时间','出款加總','出款次數']]
three_hour_deposite_user=method_hour_deposite_user[method_hour_deposite_user['存款方式']=='第三方入款'][['会员帐号','申请时间','出款加總','出款次數']]

#創建table表
list_item_123 = ['全部統計','CGPay','USDT','公司入款','购宝钱包','转让充值','第三方入款',]
list_time_123 = ['00-次數','00-金額','01-次數','01-金額','02-次數','02-金額','03-次數','03-金額',
                 '04-次數','04-金額','05-次數','05-金額','06-次數','06-金額','07-次數','07-金額',
                 '08-次數','08-金額','09-次數','09-金額','10-次數','010-金額','11-次數','11-金額',
                 '12-次數','12-金額','13-次數','13-金額','14-次數','14-金額','15-次數','15-金額',
                 '16-次數','16-金額','17-次數','17-金額','18-次數','18-金額','19-次數','19-金額',
                 '20-次數','20-金額','21-次數','21-金額','22-次數','22-金額','23-次數','23-金額']
hour_table_count_all= pd.DataFrame(columns=list_time_123,index=list_item_123)


# In[109]:


def count_sum_user_fuc(data):
    list_item_123 = ['統計值']
    list_time_123 = ['00-次數','00-金額','01-次數','01-金額','02-次數','02-金額','03-次數','03-金額',
                        '04-次數','04-金額','05-次數','05-金額','06-次數','06-金額','07-次數','07-金額',
                        '08-次數','08-金額','09-次數','09-金額','10-次數','010-金額','11-次數','11-金額',
                        '12-次數','12-金額','13-次數','13-金額','14-次數','14-金額','15-次數','15-金額',
                        '16-次數','16-金額','17-次數','17-金額','18-次數','18-金額','19-次數','19-金額',
                        '20-次數','20-金額','21-次數','21-金額','22-次數','22-金額','23-次數','23-金額']
    hour_table_count= pd.DataFrame(0,columns=list_time_123,index=list_item_123)
    
    for i in range(data.shape[0]):
        if data['申请时间'].iloc[i] == '00':
            hour_table_count.iloc[0,0]=hour_table_count.iloc[0,0]+data.iloc[i,3] ; hour_table_count.iloc[0,1]=hour_table_count.iloc[0,1]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '01':
            hour_table_count.iloc[0,2]=hour_table_count.iloc[0,2]+data.iloc[i,3] ; hour_table_count.iloc[0,3]=hour_table_count.iloc[0,3]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '02':
            hour_table_count.iloc[0,4]=hour_table_count.iloc[0,4]+data.iloc[i,3] ; hour_table_count.iloc[0,5]=hour_table_count.iloc[0,5]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '03':
            hour_table_count.iloc[0,6]=hour_table_count.iloc[0,6]+data.iloc[i,3] ; hour_table_count.iloc[0,7]=hour_table_count.iloc[0,7]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '04':
            hour_table_count.iloc[0,8]=hour_table_count.iloc[0,8]+data.iloc[i,3] ; hour_table_count.iloc[0,9]=hour_table_count.iloc[0,9]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '05':
            hour_table_count.iloc[0,10]=hour_table_count.iloc[0,10]+data.iloc[i,3] ; hour_table_count.iloc[0,11]=hour_table_count.iloc[0,11]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '06':
            hour_table_count.iloc[0,12]=hour_table_count.iloc[0,12]+data.iloc[i,3] ; hour_table_count.iloc[0,13]=hour_table_count.iloc[0,13]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '07':
            hour_table_count.iloc[0,14]=hour_table_count.iloc[0,14]+data.iloc[i,3] ; hour_table_count.iloc[0,15]=hour_table_count.iloc[0,15]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '08':
            hour_table_count.iloc[0,16]=hour_table_count.iloc[0,16]+data.iloc[i,3] ; hour_table_count.iloc[0,17]=hour_table_count.iloc[0,17]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '09':
            hour_table_count.iloc[0,18]=hour_table_count.iloc[0,18]+data.iloc[i,3] ; hour_table_count.iloc[0,19]=hour_table_count.iloc[0,19]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '10':
            hour_table_count.iloc[0,20]=hour_table_count.iloc[0,20]+data.iloc[i,3] ; hour_table_count.iloc[0,21]=hour_table_count.iloc[0,21]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '11':
            hour_table_count.iloc[0,22]=hour_table_count.iloc[0,22]+data.iloc[i,3] ; hour_table_count.iloc[0,23]=hour_table_count.iloc[0,23]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '12':
            hour_table_count.iloc[0,24]=hour_table_count.iloc[0,24]+data.iloc[i,3] ; hour_table_count.iloc[0,25]=hour_table_count.iloc[0,25]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '13':
            hour_table_count.iloc[0,26]=hour_table_count.iloc[0,26]+data.iloc[i,3] ; hour_table_count.iloc[0,27]=hour_table_count.iloc[0,27]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '14':
            hour_table_count.iloc[0,28]=hour_table_count.iloc[0,28]+data.iloc[i,3] ; hour_table_count.iloc[0,29]=hour_table_count.iloc[0,29]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '15':
            hour_table_count.iloc[0,30]=hour_table_count.iloc[0,30]+data.iloc[i,3] ; hour_table_count.iloc[0,31]=hour_table_count.iloc[0,31]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '16':
            hour_table_count.iloc[0,32]=hour_table_count.iloc[0,32]+data.iloc[i,3] ; hour_table_count.iloc[0,33]=hour_table_count.iloc[0,33]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '17':
            hour_table_count.iloc[0,34]=hour_table_count.iloc[0,34]+data.iloc[i,3] ; hour_table_count.iloc[0,35]=hour_table_count.iloc[0,35]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '18':
            hour_table_count.iloc[0,36]=hour_table_count.iloc[0,36]+data.iloc[i,3] ; hour_table_count.iloc[0,37]=hour_table_count.iloc[0,37]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '19':
            hour_table_count.iloc[0,38]=hour_table_count.iloc[0,38]+data.iloc[i,3] ; hour_table_count.iloc[0,39]=hour_table_count.iloc[0,39]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '20':
            hour_table_count.iloc[0,40]=hour_table_count.iloc[0,40]+data.iloc[i,3] ; hour_table_count.iloc[0,41]=hour_table_count.iloc[0,41]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '21':
            hour_table_count.iloc[0,42]=hour_table_count.iloc[0,42]+data.iloc[i,3] ; hour_table_count.iloc[0,43]=hour_table_count.iloc[0,43]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '22':
            hour_table_count.iloc[0,44]=hour_table_count.iloc[0,44]+data.iloc[i,3] ; hour_table_count.iloc[0,45]=hour_table_count.iloc[0,45]+data.iloc[i,2]
        elif data['申请时间'].iloc[i] == '23':
            hour_table_count.iloc[0,46]=hour_table_count.iloc[0,46]+data.iloc[i,3] ; hour_table_count.iloc[0,47]=hour_table_count.iloc[0,47]+data.iloc[i,2]

    
    return(hour_table_count)


# In[110]:


hour_table_count_all.iloc[0]=count_sum_user_fuc(all_hour_deposite_user).iloc[0]
hour_table_count_all.iloc[1]=count_sum_user_fuc(cgpay_hour_deposite_user).iloc[0]
hour_table_count_all.iloc[2]=count_sum_user_fuc(usdt_hour_deposite_user).iloc[0]
hour_table_count_all.iloc[3]=count_sum_user_fuc(conpany_hour_deposite_user).iloc[0]
hour_table_count_all.iloc[4]=count_sum_user_fuc(go_hour_deposite_user).iloc[0]
hour_table_count_all.iloc[5]=count_sum_user_fuc(change_hour_deposite_user).iloc[0]
hour_table_count_all.iloc[6]=count_sum_user_fuc(three_hour_deposite_user).iloc[0]
#hour_table_count_all.to_csv('F:/Downloads/deposite_by_hour.csv' ,encoding="utf_8_sig" )


# # 統計小額充值

# In[111]:


################## 小額充值問題 #############
#50小額
deposite_50_s=register_deposite_3[(register_deposite_3['会员层级'] != '="测试账号"') & (register_deposite_3["存入状态"] == '="已入帐"') & (register_deposite_3["申请金额"] == 50)][['会员帐号','后台代称','申请金额']]
deposite_50_f=register_deposite_3d[(register_deposite_3d['会员层级'] != '="测试账号"') & (register_deposite_3d["存入状态"] == '="未送单"') & (register_deposite_3d["申请金额"] == 50) ][['会员帐号','后台代称','申请金额']]
deposite_50_s['会员帐号']=deposite_50_s['会员帐号'].astype(str).str.replace("=","").str.replace('"',"")
deposite_50_s['后台代称']=deposite_50_s['后台代称'].astype(str).str.replace("=","").str.replace('"',"")
deposite_50_f['会员帐号']=deposite_50_f['会员帐号'].astype(str).str.replace("=","").str.replace('"',"")
deposite_50_f['后台代称']=deposite_50_f['后台代称'].astype(str).str.replace("=","").str.replace('"',"")

deposite_50_s=pd.DataFrame(deposite_50_s.groupby(by=['会员帐号','后台代称']).agg({'申请金额': ['sum','count']})).reset_index().rename(columns={ "申请金额": "出款加總"})
deposite_50_s.columns = ['会员帐号', '后台代称','出款加總','出款次數']
deposite_50_f=pd.DataFrame(deposite_50_f.groupby(by=['会员帐号','后台代称']).agg({'申请金额': ['sum','count']})).reset_index().rename(columns={ "申请金额": "出款加總"})
deposite_50_f.columns = ['会员帐号', '后台代称','出款加總','出款次數']


#100大額
deposite_100_s=register_deposite_3[(register_deposite_3['会员层级'] != '="测试账号"') & (register_deposite_3["存入状态"] == '="已入帐"') & (register_deposite_3["申请金额"] == 100)][['会员帐号','后台代称','申请金额']]
deposite_100_f=register_deposite_3d[(register_deposite_3d['会员层级'] != '="测试账号"') & (register_deposite_3d["存入状态"] == '="未送单"') & (register_deposite_3d["申请金额"] == 100) ][['会员帐号','后台代称','申请金额']]
deposite_100_s['会员帐号']=deposite_100_s['会员帐号'].astype(str).str.replace("=","").str.replace('"',"")
deposite_100_s['后台代称']=deposite_100_s['后台代称'].astype(str).str.replace("=","").str.replace('"',"")
deposite_100_f['会员帐号']=deposite_100_f['会员帐号'].astype(str).str.replace("=","").str.replace('"',"")
deposite_100_f['后台代称']=deposite_100_f['后台代称'].astype(str).str.replace("=","").str.replace('"',"")

deposite_100_s=pd.DataFrame(deposite_100_s.groupby(by=['会员帐号','后台代称']).agg({'申请金额': ['sum','count']})).reset_index().rename(columns={ "申请金额": "出款加總"})
deposite_100_s.columns = ['会员帐号', '后台代称','出款加總','出款次數']
deposite_100_f=pd.DataFrame(deposite_100_f.groupby(by=['会员帐号','后台代称']).agg({'申请金额': ['sum','count']})).reset_index().rename(columns={ "申请金额": "出款加總"})
deposite_100_f.columns = ['会员帐号', '后台代称','出款加總','出款次數']


designate_code = np.unique(deposite_50_s['后台代称'])

def count_sum_pay_fuc(data1,data2,data3,data4,bcode):
    list_item_123 = bcode
    list_time_123 = ['50-成功-次數','50-失敗-次數','50-成功-金額','50-失敗-金額','100-成功-次數','100-失敗-次數','100-成功-金額','100-失敗-金額']
    hour_table_count_small= pd.DataFrame(0,columns=list_time_123,index=list_item_123)
    
    #50成功
    for i in range(data1.shape[0]):
        for j in range(len(designate_code)):
            if data1['后台代称'].iloc[i] == designate_code[j]:
                hour_table_count_small.iloc[j,0]=hour_table_count_small.iloc[j,0]+data1.iloc[i,3] ; hour_table_count_small.iloc[j,2]=hour_table_count_small.iloc[j,2]+data1.iloc[i,2]
    #50失敗
    for i in range(data2.shape[0]):
        for j in range(len(designate_code)):
            if data2['后台代称'].iloc[i] == designate_code[j]:
                hour_table_count_small.iloc[j,1]=hour_table_count_small.iloc[j,1]+data2.iloc[i,3] ; hour_table_count_small.iloc[j,3]=hour_table_count_small.iloc[j,3]+data2.iloc[i,2]
    #100成功
    for i in range(data3.shape[0]):
        for j in range(len(designate_code)):
            if data3['后台代称'].iloc[i] == designate_code[j]:
                hour_table_count_small.iloc[j,4]=hour_table_count_small.iloc[j,4]+data3.iloc[i,3] ; hour_table_count_small.iloc[j,6]=hour_table_count_small.iloc[j,6]+data3.iloc[i,2]
    #100失敗
    for i in range(data4.shape[0]):
        for j in range(len(designate_code)):
            if data4['后台代称'].iloc[i] == designate_code[j]:
                hour_table_count_small.iloc[j,5]=hour_table_count_small.iloc[j,5]+data4.iloc[i,3] ; hour_table_count_small.iloc[j,7]=hour_table_count_small.iloc[j,7]+data4.iloc[i,2]
  
    return(hour_table_count_small)


# In[112]:


data_small_pay=count_sum_pay_fuc(deposite_50_s,deposite_50_f,deposite_100_s,deposite_100_f,designate_code)
data_small_pay['50-成功率'] = round(data_small_pay['50-成功-次數'] / (data_small_pay['50-成功-次數']+data_small_pay['50-失敗-次數']) *100 ,2)
data_small_pay['100-成功率'] = round(data_small_pay['100-成功-次數'] / (data_small_pay['100-成功-次數']+data_small_pay['100-失敗-次數']) *100 ,2)
data_small_pay=data_small_pay[['50-成功-次數','50-失敗-次數','50-成功率','50-成功-金額','50-失敗-金額','100-成功-次數','100-失敗-次數','100-成功率','100-成功-金額','100-失敗-金額']]
data_small_pay.loc['整行加總'] = data_small_pay.apply(lambda x: x.sum())
#data_small_pay.to_csv('F:/Downloads/deposite_small.csv' ,encoding="utf_8_sig" )


# In[72]:


# all_dataframe_data
# pay_dataframe_data
# dataframe_count


# # 輸出至 TG

# In[118]:


#傳送文件
def send_telegrame_file(text,title):
    tele_chatid=['-451149494 ','-123456789']         #测试 -451149494   #正式 -空 
    tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
    bot = telepot.Bot(tele_token)
    bot.sendMessage(chat_id=tele_chatid[0],text= title) 
    bot.sendDocument(chat_id=tele_chatid[0] , document= open(text,'rb')) #,encoding = 'utf-8'


# In[117]:


with pd.ExcelWriter("C:/Users/btorin/Desktop/download_csv_sigua/auto_data_sigua.xlsx") as auto_data_sigua:
    #美日數據
    dataframe_count.to_excel(auto_data_sigua, sheet_name="數據-1")
    pay_dataframe_data.to_excel(auto_data_sigua, sheet_name="金額區間-支付方式")
    all_dataframe_data.to_excel(auto_data_sigua, sheet_name="各支付方式統計")
    #異常
    test_different_seposite.to_excel(auto_data_sigua, sheet_name="各支付成功失敗")
    final_user_n_d_w.to_excel(auto_data_sigua, sheet_name="今日註冊會員存提差")
    today_alluser_dw.to_excel(auto_data_sigua, sheet_name="會員存提差")
    hour_table_count_all.to_excel(auto_data_sigua, sheet_name="每小時存款細項")
    data_small_pay.to_excel(auto_data_sigua, sheet_name="小額充值管道成功失敗")
    auto_data_sigua.save()


# In[119]:


#傳送資料
send_telegrame_file("C:/Users/btorin/Desktop/download_csv_sigua/auto_data_sigua.xlsx",'SIGUA-'+str(delay_oneday)+'-數據總攬(每日數據、異常數據)')


# In[6]:


import shutil 
import os
import time

shutil.rmtree('C:\\Users\\btorin\\Desktop\\download_csv_sigua_copy')  
time.sleep(3)
shutil.copytree('C:\\Users\\btorin\\Desktop\\download_csv_sigua', 'C:\\Users\\btorin\\Desktop\\download_csv_sigua_copy')  #, symlinks=False, ignore=None
time.sleep(3)
shutil.rmtree('C:\\Users\\btorin\\Desktop\\download_csv_sigua')  
time.sleep(3)
os.mkdir('C:\\Users\\btorin\\Desktop\\download_csv_sigua')     

# In[27]:


'''
def send_telegrame(text,title):
    tele_chatid=['-451149494 ','-123456789']         #测试 -451149494   #正式 -空 
    tele_token='1020859504:AAEb-tLbaBjJvJqBsLCzCsStrgTlZNqXRR8'
    bot = telepot.Bot(tele_token)
    bot.sendMessage(chat_id=tele_chatid[0],text= delay_oneday+'資料'+ title + "\n"  
                + str(text.to_dict) ) 
pd.options.display.float_format = "{:.2f}".format
send_telegrame(dataframe_count,'-數據-1')
send_telegrame(pay_dataframe_data,'-金額區間/支付方式')
send_telegrame(all_dataframe_data,'-各支付方式統計')
'''

