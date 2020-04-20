#coding:utf-8
import hashlib
import json
from public.common.log import *
    
#字符串md5加密
def get_md5(need_str):
    return hashlib.md5(need_str.encode('utf-8')).hexdigest()

#处理字符串为json格式
def str_to_json(result_str):

    RST = ''
    try:
        RST = json.loads(result_str)
    except:
        try:
            #处理可能包含在()内的json字符串
            temp_str = result_str.split('(')[1].split(')')[0]
            RST = json.loads(temp_str)
        except:
            logging.error("字符串处理Json失败: " + str(result_str))
            return False
        
    return RST


#获取dict指定的字段数据
def dict_filter_columns(dict_data, array_need = ['*']):

    if type(dict_data) != dict:
        logging.error("Dict数据格式不正确.\n\t当前Dict数据:\t"  + str(dict_data) + '\n\t当前数据类型为:\t' + str(type(dict_data)))
        return False
    else:
        if type(array_need) == list:            
            temp = len(array_need)
            if temp == 0:
                logging.error("处理Dict数据，未提供需求字段")
                return False
            #array_need为['*']时返回整个json
            elif temp == 1 and array_need[0] == '*':
                return dict_data
            else:
                return_json = {}
                for i in range(0, temp):
                    if array_need[i] in dict_data.keys():
                        return_json[array_need[i]] = dict_data[array_need[i]]
                    else:
                        logging.warning("处理Dict数据警告，Keys不包含" + str(array_need[i]) + '字段.\n\t提供的Dict数据为\t' + str(dict_data))
                return return_json
        else:
            logging.error("提供需求字段错误,需list格式数据.\n\t当前Dict数据:\t"  + str(array_need) + "\n\t当前数据格式为:\t" + str(type(array_need)))
            return False

#二位数组排序,二维数组中第column_num列的值排序， row_num表示从第几行开始排序
def array_sec_sort(array_b, column_num, row_num = 0):
    array_temp = array_b
    array_len = len(array_temp)
    if array_len == 1:
        return array_temp
    else:
        if column_num < len(array_b[0]):
            for i in range(0, array_len - 1):
                for j in range(row_num, array_len - 1 - i):
                    if array_temp[j][column_num] < array_temp[j+1][column_num]:
                        temp_num = array_temp[j]
                        array_temp[j] = array_temp[j+1]
                        array_temp[j+1] = temp_num
            #return array_temp
        else:
            print("比较的数出错啦")

#数组+字典排序,二维数组中第column_num列的值排序， row_num表示从第几行开始排序
def array_dict_sort(array_dict, dict_key, row_num=0):
    array_temp = array_dict
    array_len = len(array_dict)
    if array_len == 1:
        return array_dict
    else:
        for i in range(0, array_len - 1):
            for j in range(row_num, array_len - 1 - i):
                if array_temp[j][dict_key] < array_temp[j + 1][dict_key]:
                    temp_num = array_temp[j]
                    array_temp[j] = array_temp[j + 1]
                    array_temp[j + 1] = temp_num

        return array_temp

#返回dict中的三层内的key
def get_keys(need_dict):
    if type(need_dict) != dict:
        print('非字典格式数据，无法处理!')
        return None
    else:
        return_keys = []
        for i in need_dict:
            return_keys.append(i)
            if type(need_dict[i]) == dict:
                for j in need_dict[i]:
                    return_keys.append(j)
                    if type(need_dict[i][j]) == dict:
                        for k in need_dict[i][j]:
                            return_keys.append(k)
        return return_keys

#设置hosts
def modify_hosts(need_host):
    fp = open(r"C:\Windows\System32\drivers\etc\hosts", 'w')
    fp.write(need_host)
    fp.close()
    print('Hosts设置成功')