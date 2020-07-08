import time
import random
from config.config import *

class parameter_change():

    def __init__(self):
        pass

    @staticmethod
    def get_millisecond_timestamp():
        '''获取毫秒级时间戳'''
        return str(round(time.time() * 1000))

    @staticmethod
    def get_time_stamp():
        '''获取时间戳'''
        return str(round(time.time()))

    @staticmethod
    def get_zdjl_member_id(zdjl_member_id_list):
        '''获取后台我的股池=>指导交流=>群发消息所需入参uids，由member_id构成的字符串'''
        member_id_list = eval(zdjl_member_id_list)
        n = len(member_id_list)
        member_id_str = ''
        for i in range(n):
            member_id_str += member_id_list[i]['member_id']
            if i != n - 1:
                member_id_str += ','
        return member_id_str

    @staticmethod
    def ybwzxq_date_replace(ybwz_date):
        '''研报文章详情字符串拼接'''
        date_list = ybwz_date.split(' ')
        temp_date = date_list[0].split('-')
        return '/' + temp_date[0] + '/' + temp_date[1] + temp_date[2] + '/'

    @staticmethod
    def get_chance_list_len(chance_list_str):
        '''获取机会list的len'''
        if type(chance_list_str) == list:
            return len(chance_list_str)
        else:
            return 0

    @staticmethod
    def str_to_float(temp_str):
        '''字符串转float'''
        return float(temp_str)

    @staticmethod
    def str_to_int(temp_str):
        '''字符串转int'''
        return int(temp_str)

    @staticmethod
    def crm_cookies_set(cookies):
        try:
            cookies = eval(cookies)
            kv_str = ''
            for key in cookies.keys():
                kv_str += key + '=' + cookies[key] + ';'

            return kv_str[:-1]
        except:
            print('error!')
