# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 15:15:17 2017

@author: Administrator
"""
import warnings
warnings.filterwarnings('ignore')

#划分训练集测试集，去掉节假日
train=new_data[new_data.week<71] #train=train[~train.week.isin(holiday_week_list)]
train=train[~train.time_stamp.isin(['50903','50904','50905','50926','50927','51001','51002','51003','51004','51005','51006','51007','60101','60102','60103','60207','60208','60209','60210','60211','60212','60213','60402','60403','60404','60430','60501','60502','60609','60610','60611','60915','60916','60917','61001','61002','61003','61004','61005','61006','61007'])]
train=train[train.user_id>3]
test=new_data[new_data.week==71]  


const=train.groupby(['shop_id','daily'],as_index=False)['distribute'].median()

d2=train[train.week.isin([70])]
d3=train[train.time_stamp.isin(['61024'])]
del d3['distribute']
d3=pd.merge(d3,const,how='left',on=['shop_id','daily'])
d3['count_mean']=d3.user_id/d3.distribute
d3['mean_space']=d3['count_mean']

d1=pd.concat([d1,d2])
d1=pd.concat([d1,d2])
d1=pd.concat([d1,d2])
d1=pd.concat([d1,d2])

del d1['distribute']
d1=pd.merge(d1,const,how='left',on=['shop_id','daily'])
d1['mean_space']=d1.user_id/d1.distribute
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])

last_week=train[train.week.isin([70])]
last2_week=train[train.week.isin([69])]
last_week=pd.DataFrame(last_week,columns=['shop_id','daily','user_id'])
last2_week=pd.DataFrame(last2_week,columns=['shop_id','daily','user_id'])
last_week.columns=['shop_id','daily','last_week']
last2_week.columns=['shop_id','daily','last2_week']

week1=last_week.groupby('shop_id',as_index=False)['last_week'].mean()
week2=last2_week.groupby('shop_id',as_index=False)['last2_week'].mean()
week_loss=pd.merge(week1,week2,how='inner',on='shop_id')
week_loss['week_loss']=week_loss.last_week-week_loss.last2_week
week_loss['week_loss']=week_loss.week_loss.apply(lambda x:abs(x))
week_loss['week_loss']=week_loss.week_loss/(week_loss.last_week+week_loss.last2_week)

d1=d1.groupby('shop_id',as_index=False).mean()
d1=pd.DataFrame(d1,columns=['shop_id','count_mean','mean_space'])
d1.columns=['shop_id','pre_mean','mean_space']


test=pd.merge(test,d1,how='inner',on='shop_id')
del test['distribute']
test=pd.merge(test,const,how='left',on=['shop_id','daily'])
test=pd.merge(test,last_week,how='left',on=['shop_id','daily'])
test=pd.merge(test,last2_week,how='left',on=['shop_id','daily'])

test['pre']=test.distribute*test.pre_mean
test['pre2']=test.distribute*test.mean_space
test['last_week'][test.last_week.isnull()]=test.last2_week
test['last2_week'][test.last2_week.isnull()]=test.last_week
test['last_week'][test.last_week.isnull()]=test.pre
test['last2_week'][test.last2_week.isnull()]=test.pre
test['pre3']=0.1*test['pre']+0.60*test['pre2']+0.15*test['last_week']+0.15*test['last2_week']


#这部分过拟合了A榜数据，B榜下降
test['pre3'][test.daily==1]=test['pre3']*0.97
test['pre3'][test.daily==2]=test['pre3']*1.02
test['pre3'][test.daily==3]=test['pre3']*0.98
test['pre3'][test.daily==6]=test['pre3']*1.03
test['pre3'][test.daily==7]=test['pre3']*1.02
shop=pd.read_csv('./shop_info.txt',header=None,names=['shop_id','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name'])
shop['cate_3_name'][shop.cate_3_name.isnull()]=shop.cate_2_name
shop['cate_3_name'][shop.cate_3_name.isnull()]=shop.cate_1_name
cate_3_list=list(set(list(shop.cate_3_name)))
cate_3_list=cate_3_list[1:]
icecream=list(shop[shop.cate_3_name==cate_3_list[29]].shop_id)
hotpot=list(shop[shop.cate_3_name.isin([cate_3_list[35],cate_3_list[42]])].shop_id)
fruit=list(shop[shop.cate_3_name==cate_3_list[38]].shop_id)
shaokao=list(shop[shop.cate_3_name.isin([cate_3_list[40],cate_3_list[4],cate_3_list[13]])].shop_id)
test['pre3'][test.shop_id.isin(hotpot)]=test['pre3']*1.09
test['pre3'][test.shop_id.isin(fruit)]=test['pre3']*0.91
test['pre3'][test.shop_id.isin(shaokao)]=test['pre3']*1.07



#天气部分处理
weather=pd.DataFrame(result,columns=['shop_id','time_stamp','mWeather'])
test=pd.merge(test,weather,how='left',on=['shop_id','time_stamp'])
test['pre3'][test.mWeather==3]=test['pre3']*1.03
test['pre3'][test.mWeather==1]=test['pre3']*0.99
test['pre3'][test.mWeather==0]=test['pre3']*0.93




#空气质量处理（这部分loss没有下降）
aqi=pd.read_csv('./alldata.csv',encoding='utf-8')






test.pre=test.pre.apply(lambda x:int(round(x)))
test.pre2=test.pre2.apply(lambda x:int(round(x)))
test.pre3=test.pre3.apply(lambda x:int(round(x*1.01)))
test['error']=test.user_id-test.pre
test['error2']=test.user_id-test.pre2
test['error3']=test.user_id-test.pre3
test.error=test.error.apply(lambda x:abs(x))
test.error2=test.error2.apply(lambda x:abs(x))
test.error3=test.error3.apply(lambda x:abs(x))
test['loss']=test.error/(test.user_id+test.pre)
test['loss2']=test.error2/(test.user_id+test.pre2)
test['loss3']=test.error3/(test.user_id+test.pre3)


print test.loss3.mean()