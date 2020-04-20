#coding:utf-8
import os
from public.common.date import *

#返回文件信息list,文件大小，创建时间，访问时间，修改时间
def get_file_info(filePath):
    file_info = []
    #filePath = unicode(filePath,'utf8')
    #文件大小，byte
    file_info.append(os.path.getsize(filePath))
    #文件创建时间
    file_info.append(TimestampToTime(os.path.getctime(filePath)))
    #文件访问时间
    file_info.append(TimestampToTime(os.path.getatime(filePath)))
    #文件修改时间
    file_info.append(TimestampToTime(os.path.getmtime(filePath)))
    return file_info