# -*-coding:utf-8 -*-
import pandas as pd

def high_temp_code(high_temp):
    if(int(high_temp) >= 20):
        return 0
    elif (int(high_temp) >= 15)&(int(high_temp) <= 19):
        return 1
    elif (int(high_temp) >= 10) & (int(high_temp) <= 14):
        return 2
    elif (int(high_temp) >= 5)&(int(high_temp) <= 9):
        return 3
    elif (int(high_temp) >= 0) & (int(high_temp) <= 4):
        return 4
    else :
        return 5

def low_temp_code(low_temp):
    if(int(low_temp) >= 20):
        return 0
    elif (int(low_temp) >= 15)&(int(low_temp) <= 19):
        return 1
    elif (int(low_temp) >= 10) & (int(low_temp) <= 14):
        return 2
    elif (int(low_temp) >= 5)&(int(low_temp) <= 9):
        return 3
    elif (int(low_temp) >= 0) & (int(low_temp) <= 4):
        return 4
    elif (int(low_temp) >= -5) & (int(low_temp) <= -1):
        return 5
    else:
        return 6

def mWeather_code(mWeather):
    if (("暴雨" in mWeather) | ("暴雪" in mWeather)):
        return -1
    elif(("中雨" in mWeather)|("大雨" in mWeather)):
        return 0
    elif (("雨"in mWeather)|("雪"in mWeather)):
        return 1
    elif (("多云"in mWeather)|("阴"in mWeather)):
        return 2
    elif (("晴"in mWeather)):
        return 3
    else:
        return 4

def wind_level_code(wind_level):
    wind_level = str(wind_level)
    if(("6" in wind_level)):
        return 0
    elif (("5"in wind_level)):
        return 1
    elif (("4"in wind_level)):
        return 2
    elif (("3"in wind_level)):
        return 3
    elif (("2"in wind_level)):
        return 4
    elif (("1"in wind_level)):
        return 5
    else:
        return 6



shop_info = pd.read_table('./shop_info.txt', sep=',', header=-1)
shop_info.columns = ['shop_id', 'city_name', 'location_id', 'per_pay', 'score', 'comment_cnt', 'shop_level',
                     'cate_1_name', 'cate_2_name', 'cate_3_name']

shop_info = shop_info[['shop_id', 'city_name']]

weather_all = pd.read_table('./weather_all.csv',sep=',')
weather_all.columns=['city_name','date','high_temp','low_temp','mWeather','wind_direction','wind_level']

result = pd.merge(shop_info, weather_all, on=['city_name'], how='left')

result = result[['shop_id','date', 'high_temp', 'low_temp', 'mWeather', 'wind_level']]

result.high_temp = result.high_temp.apply(high_temp_code)
result.mWeather = result.mWeather.apply(mWeather_code)
result.wind_level = result.wind_level.apply(wind_level_code)

result['time_stamp']=result.date.apply(lambda x:x[3:4]+x[5:7]+x[8:10])
# for i in range(0,7,1):
#     if i==0:
#         shop_weather_simple0 = result[(result.date == '2016-10-30')]
#     elif i==1:
#         shop_weather_simple0 = result[(result.date == '2016-10-31')]
#     elif i==2:
#         shop_weather_simple0 = result[(result.date == '2016-10-25')]
#     elif i==3:
#         shop_weather_simple0 = result[(result.date == '2016-10-26')]
#     elif i==4:
#         shop_weather_simple0 = result[(result.date == '2016-10-27')]
#     elif i==5:
#         shop_weather_simple0 = result[(result.date == '2016-10-28')]
#     elif i==6:
#         shop_weather_simple0 = result[(result.date == '2016-10-29')]
#
#     shop_weather_simple0 = shop_weather_simple0[['shop_id', 'high_temp','low_temp','mWeather','wind_level']]
#
#     shop_weather_simple0.high_temp = shop_weather_simple0.high_temp.apply(high_temp_code)
#     shop_weather_simple0.low_temp = shop_weather_simple0.low_temp.apply(low_temp_code)
#     shop_weather_simple0.mWeather = shop_weather_simple0.mWeather.apply(mWeather_code)
#     shop_weather_simple0.wind_level = shop_weather_simple0.wind_level.apply(wind_level_code)
#
#     shop_weather_simple0.to_csv("../data/shop_weather_simple0_" + str(i) + ".csv", index=False)
#
#
# for i in range(0,7,1):
#     if i==0:
#         shop_weather_simple0 = result[(result.date == '2016-10-23')]
#     elif i==1:
#         shop_weather_simple0 = result[(result.date == '2016-10-24')]
#     elif i==2:
#         shop_weather_simple0 = result[(result.date == '2016-10-18')]
#     elif i==3:
#         shop_weather_simple0 = result[(result.date == '2016-10-19')]
#     elif i==4:
#         shop_weather_simple0 = result[(result.date == '2016-10-20')]
#     elif i==5:
#         shop_weather_simple0 = result[(result.date == '2016-10-21')]
#     elif i==6:
#         shop_weather_simple0 = result[(result.date == '2016-10-22')]
#
#     shop_weather_simple0 = shop_weather_simple0[['shop_id', 'high_temp','low_temp','mWeather','wind_level']]
#
#     shop_weather_simple0.high_temp = shop_weather_simple0.high_temp.apply(high_temp_code)
#     shop_weather_simple0.low_temp = shop_weather_simple0.low_temp.apply(low_temp_code)
#     shop_weather_simple0.mWeather = shop_weather_simple0.mWeather.apply(mWeather_code)
#     shop_weather_simple0.wind_level = shop_weather_simple0.wind_level.apply(wind_level_code)
#
#     shop_weather_simple0.to_csv("../data/shop_weather_simple1_" + str(i) + ".csv", index=False)
#
#
# for i in range(0,7,1):
#     if i==0:
#         shop_weather_simple0 = result[(result.date == '2016-10-16')]
#     elif i==1:
#         shop_weather_simple0 = result[(result.date == '2016-10-17')]
#     elif i==2:
#         shop_weather_simple0 = result[(result.date == '2016-10-11')]
#     elif i==3:
#         shop_weather_simple0 = result[(result.date == '2016-10-12')]
#     elif i==4:
#         shop_weather_simple0 = result[(result.date == '2016-10-13')]
#     elif i==5:
#         shop_weather_simple0 = result[(result.date == '2016-10-14')]
#     elif i==6:
#         shop_weather_simple0 = result[(result.date == '2016-10-15')]
#
#     shop_weather_simple0 = shop_weather_simple0[['shop_id', 'high_temp','low_temp','mWeather','wind_level']]
#
#     shop_weather_simple0.high_temp = shop_weather_simple0.high_temp.apply(high_temp_code)
#     shop_weather_simple0.low_temp = shop_weather_simple0.low_temp.apply(low_temp_code)
#     shop_weather_simple0.mWeather = shop_weather_simple0.mWeather.apply(mWeather_code)
#     shop_weather_simple0.wind_level = shop_weather_simple0.wind_level.apply(wind_level_code)
#
#     shop_weather_simple0.to_csv("../data/shop_weather_simple2_" + str(i) + ".csv", index=False)
#
#
# for i in range(0,7,1):
#     if i==0:
#         shop_weather_simple0 = result[(result.date == '2016-11-06')]
#     elif i==1:
#         shop_weather_simple0 = result[(result.date == '2016-11-07')]
#     elif i==2:
#         shop_weather_simple0 = result[(result.date == '2016-11-01')]
#     elif i==3:
#         shop_weather_simple0 = result[(result.date == '2016-11-02')]
#     elif i==4:
#         shop_weather_simple0 = result[(result.date == '2016-11-03')]
#     elif i==5:
#         shop_weather_simple0 = result[(result.date == '2016-11-04')]
#     elif i==6:
#         shop_weather_simple0 = result[(result.date == '2016-11-05')]
#
#     shop_weather_simple0 = shop_weather_simple0[['shop_id', 'high_temp','low_temp','mWeather','wind_level']]
#
#     shop_weather_simple0.high_temp = shop_weather_simple0.high_temp.apply(high_temp_code)
#     shop_weather_simple0.low_temp = shop_weather_simple0.low_temp.apply(low_temp_code)
#     shop_weather_simple0.mWeather = shop_weather_simple0.mWeather.apply(mWeather_code)
#     shop_weather_simple0.wind_level = shop_weather_simple0.wind_level.apply(wind_level_code)
#
#     shop_weather_simple0.to_csv("../data/shop_weather_test_part1_" + str(i) + ".csv", index=False)
#
#
# for i in range(0,7,1):
#     if i==0:
#         shop_weather_simple0 = result[(result.date == '2016-11-13')]
#     elif i==1:
#         shop_weather_simple0 = result[(result.date == '2016-11-14')]
#     elif i==2:
#         shop_weather_simple0 = result[(result.date == '2016-11-08')]
#     elif i==3:
#         shop_weather_simple0 = result[(result.date == '2016-11-09')]
#     elif i==4:
#         shop_weather_simple0 = result[(result.date == '2016-11-10')]
#     elif i==5:
#         shop_weather_simple0 = result[(result.date == '2016-11-11')]
#     elif i==6:
#         shop_weather_simple0 = result[(result.date == '2016-11-12')]
#
#     shop_weather_simple0 = shop_weather_simple0[['shop_id', 'high_temp','low_temp','mWeather','wind_level']]
#
#     shop_weather_simple0.high_temp = shop_weather_simple0.high_temp.apply(high_temp_code)
#     shop_weather_simple0.low_temp = shop_weather_simple0.low_temp.apply(low_temp_code)
#     shop_weather_simple0.mWeather = shop_weather_simple0.mWeather.apply(mWeather_code)
#     shop_weather_simple0.wind_level = shop_weather_simple0.wind_level.apply(wind_level_code)
#
#     shop_weather_simple0.to_csv("../data/shop_weather_test_part2_" + str(i) + ".csv", index=False)