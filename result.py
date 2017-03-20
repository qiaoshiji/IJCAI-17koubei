# -*- coding: utf-8 -*-
"""
Created on Wed Mar 01 21:44:36 2017

@author: qiaosj
"""
import copy
train=copy.deepcopy(new_data)
train=train[~train.time_stamp.isin(['50903','50904','50905','50926','50927','51001','51002','51003','51004','51005','51006','51007','60101','60102','60103','60207','60208','60209','60210','60211','60212','60213','60402','60403','60404','60430','60501','60502','60609','60610','60611','60915','60916','60917','61001','61002','61003','61004','61005','61006','61007'])]
train=train[train.user_id>3]
 





const=train.groupby(['shop_id','daily'],as_index=False)['distribute'].median()

d0=train[train.week.isin([69,70,71])]
d1=train[train.week.isin([70,71])]
d2=train[train.week.isin([71])]
d3=train[train.time_stamp.isin(['61031'])]
del d3['distribute']
d3=pd.merge(d3,const,how='left',on=['shop_id','daily'])
d3['mean_space']=d3.user_id/d3.distribute
d3.count_mean=d3.mean_space
 
d1=pd.concat([d0,d1])
d1=pd.concat([d1,d2])




del d1['distribute']
d1=pd.merge(d1,const,how='left',on=['shop_id','daily'])
d1['mean_space']=d1.user_id/d1.distribute
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])
d1=pd.concat([d1,d3])

last_week=train[train.week.isin([71])]
last_week=pd.DataFrame(last_week,columns=['shop_id','daily','user_id'])
last_week.columns=['shop_id','daily','last_week']
last_week2=train[train.week.isin([70])]
last_week2=pd.DataFrame(last_week2,columns=['shop_id','daily','user_id'])
last_week2.columns=['shop_id','daily','last2_week']
last_week3=train[train.week.isin([69])]
last_week3=pd.DataFrame(last_week3,columns=['shop_id','daily','user_id'])
last_week3.columns=['shop_id','daily','last3_week']



d1=d1.groupby('shop_id',as_index=False).mean()
d1=pd.DataFrame(d1,columns=['shop_id','count_mean','mean_space'])
d1.columns=['shop_id','pre_mean','mean_space']


test=pd.DataFrame(columns=['shop_id'])
test.shop_id=list(range(1,2001))
test=pd.merge(test,const,how='outer',on='shop_id')
test=pd.merge(test,d1,how='left',on='shop_id')
test=test.fillna(40.0)
test=pd.merge(test,last_week,how='left',on=['shop_id','daily'])
test=pd.merge(test,last_week2,how='left',on=['shop_id','daily'])
test=pd.merge(test,last_week3,how='left',on=['shop_id','daily'])
test['last3_week'][test.last_week.isnull()]=test.last2_week
test['last3_week'][test.last_week.isnull()]=test.last_week
test['last2_week'][test.last2_week.isnull()]=test.last_week
test['last2_week'][test.last2_week.isnull()]=test.last3_week
test['last_week'][test.last3_week.isnull()]=test.last2_week
test['last_week'][test.last3_week.isnull()]=test.last3_week
test['last_week'][test.last_week.isnull()]=test.distribute*test.mean_space
test['last2_week'][test.last2_week.isnull()]=test.distribute*test.mean_space
test['last3_week'][test.last3_week.isnull()]=test.distribute*test.mean_space

test['pre']=test.distribute*test.pre_mean
test['pre2']=test.distribute*test.mean_space
test['pre3']=0.1*test['pre']+0.6*test['pre2']+0.1*test['last_week']+0.1*test['last2_week']+0.1*test['last3_week']


#shop=pd.read_csv('./shop_info.txt',header=None,names=['shop_id','city_name','location_id','per_pay','score','comment_cnt','shop_level','cate_1_name','cate_2_name','cate_3_name'],encoding='utf-8')
#shop['cate_3_name'][shop.cate_3_name.isnull()]=shop.cate_2_name
#shop['cate_3_name'][shop.cate_3_name.isnull()]=shop.cate_1_name
#cate_3_list=list(set(list(shop.cate_3_name)))
#cate_3_list=cate_3_list[1:]
##icecream=list(shop[shop.cate_3_name==cate_3_list[29]].shop_id)
#hotpot=list(shop[shop.cate_3_name.isin([cate_3_list[38],cate_3_list[7]])].shop_id)
#fruit=list(shop[shop.cate_3_name==cate_3_list[22]].shop_id)
#shaokao=list(shop[shop.cate_3_name.isin([cate_3_list[35],cate_3_list[44],cate_3_list[37]])].shop_id)
##test['pre3'][test.shop_id.isin(icecream)]=test['pre3']*0.99
#test['pre3'][test.shop_id.isin(hotpot)]=test['pre3']*1.05
#test['pre3'][test.shop_id.isin(fruit)]=test['pre3']*0.95
#test['pre3'][test.shop_id.isin(shaokao)]=test['pre3']*1.05


test.pre3=test.pre3.apply(lambda x:int(round(x*1.04)))

result=pd.DataFrame(test,columns=['shop_id','daily','pre3'])
final=pd.DataFrame(columns=['shop_id'])
final.shop_id=list(range(1,2001))
for i in [2,3,4,5,6,7,1,2,3,4,5,6,7,1]:
    one_day=result[result.daily==i]
    del one_day['daily']
    final=pd.merge(final,one_day,how='left',on='shop_id')
final.columns=['shop_id', 'pre1', 'pre2', 'pre3', 'pre4', 'pre5',
       'pre6', 'pre7', 'pre8', 'pre9', 'pre10', 'pre11',
       'pre12', 'pre13', 'pre14']
final.pre11=final.pre11.apply(lambda x:int(round(x*1.05)))
final.pre5=final.pre5.apply(lambda x:int(round(x*1.02)))
final.pre12=final.pre12.apply(lambda x:int(round(x*1.02)))
final.pre6=final.pre6.apply(lambda x:int(round(x*1.02)))
