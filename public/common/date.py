#coding:utf-8
import re
import datetime
import time
from dateutil.parser import parse
from public.common.log import *

#时间戳转换为时间
def TimestampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)

#计算指定年月的最后一天的日期
def get_day(date):
    year = int(date[0:4])
    month = int(date[5:7])
    day_num = [31,28,31,30,31,30,31,31,30,31,30,31]
    if month != 2:
        return date + "-" + str(day_num[month - 1])
    elif year % 4 != 0:
        return date + "-" + str(day_num[1])
    elif year % 100 == 0 and year % 400 != 0:
        return date + "-" + str(day_num[1])
    else:
        return date + "-29"

#判断日期录入的正确性
def input_date(date, need_month = 1, need_day = 1):
    #过滤输入日期基本结构
    date_separator = '[\-]'
    year_re = '[1-9](\d){3}'
    month_re = '([0][1-9]|[1][0-2])'
    day_re = '([0][1-9]|[1-2][0-9]|[3][0-1])'
    date_re = '^' + year_re + date_separator + month_re + date_separator + day_re + '$'
    if need_month == 0:
        date_re = '^' + year_re + '$'
    if need_month == 1 and need_day == 0:
        date_re = '^' + year_re + date_separator + month_re + '$'
    pattern = re.compile(date_re)
    match = pattern.match(date)
    if match:
        date_result = match.group()
        year = int(date_result[0:4])
        if year < 1970:
            return 0
        if need_month == 1 and need_day == 1:
            month = int(date_result[5:7])
            day = int(date_result[8:])
            if month in [4,6,9,11] and day == 31:
                return 0
            elif year %4 != 0 and month == 2 and  day > 28:
                return 0
            elif year % 400 == 0 and month == 2 and day > 28:
                return 0
            elif month == 2 and day > 29:
                return 0
            else:
                return date_result
        else:
            return date_result
    else:
        return 0

#判断时间录入的正确性
def input_time(time):
    #过滤输入时间基本结构
    time_re = '^([0]?(\d){1}|[1](\d){1}|[2][0-3])[:][0-5](\d){1}[:][0-5](\d){1}|[2][4]([:][0]{2}){2}$'
    pattern = re.compile(time_re)
    match = pattern.match(time)
    if match:
        time_result = match.group()
        return  time_result
    else:
        return 0

#查询时间范围录入
def set_date_time():
    switch = 1
    result_date = []
    while (switch):
        print("请输入计算时间的范围，格式如:2016-09-01 09:00:00; 输入#为退出本次查询")
        print("开始时间:")
        begin_temp = raw_input()
        if begin_temp == '#':
            return 0
        if ' ' in begin_temp:
            date_temp = begin_temp.split(' ')
            begin_date_result = input_date(date_temp[0])
            begin_time_result = input_time(date_temp[1])
            if begin_date_result == 0 or begin_time_result == 0:
                print("时间格式不正确，请重新输入!")
                switch = 1
            else:
                switch = 0
        else:
            print("时间格式不正确，日期与时间之间请加上空格重新输入!")
    result_date.append(begin_temp)

    switch = 1
    while (switch):
        print("结束时间:")
        end_temp = raw_input()
        if end_temp == '#':
            return 0
        if ' ' in end_temp:
            date_temp = end_temp.split(' ')
            end_date_result = input_date(date_temp[0])
            end_time_result = input_time(date_temp[1])
            if end_date_result == 0 or end_time_result == 0 :
                print("时间格式不正确，请重新输入!")
                switch = 1
            else:
                switch = 0
        else:
            print("时间格式不正确，日期与时间之间请加上空格重新输入!")
    result_date.append(end_temp)
    return  result_date

def get_time_stamp():
    '''获取当前时间'''
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_secs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_secs)
    return time_stamp


def get_date_time_str():
    '''获取当前时间，精确到秒的字符串'''
    date_time = str(datetime.datetime.now()).split('.')[0].split(' ')
    return ''.join(date_time[0].split('-')) + ''.join(date_time[1].split(':'))


def time_dif(a, b):
    '''返回两个时间毫秒级差值'''
    try:
        return_time = (parse(b) - parse(a)).total_seconds()
        return return_time
    except Exception as e:
        logging.info(e)
        return False