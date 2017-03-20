# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 10:05:42 2017

@author: Administrator
"""

import pandas as pd
import time

user_pay=pd.read_csv('./user_pay.txt',header=None,names=['user_id','shop_id','time_stamp'])

user_pay.time_stamp=user_pay.time_stamp.apply(lambda x:x[3:4]+x[5:7]+x[8:10])
new_data=user_pay.groupby(['shop_id','time_stamp'],as_index=False).count()
del user_pay

day=list(set(list(new_data.time_stamp)))
day.sort()
week=1
daily=4
day_dict={}
for i in day:
    if i=='51211':
        daily+=1
    if daily==7:
        daily=1
        week+=1
    else:
        daily+=1
    day_dict[i]={}
    day_dict[i]['week']=week
    day_dict[i]['daily']=daily

new_data['week']=new_data.time_stamp.apply(lambda x:day_dict[x]['week'])
new_data['daily']=new_data.time_stamp.apply(lambda x:day_dict[x]['daily'])
new_data=new_data[new_data.user_id>2]
new_data['week'][new_data.daily==1]=new_data.week-1
data=new_data.groupby(['shop_id','week'],as_index=False)['user_id'].mean()
data.columns=['shop_id','week','count_mean']
new_data=pd.merge(new_data,data,how='left',on=['shop_id','week'])
new_data['distribute']=new_data.user_id/new_data.count_mean