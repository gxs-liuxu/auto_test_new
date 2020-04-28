#Author:chen
#!/usr/bin/env python
#-*- coding: utf-8 -*-
import os
import time

now = time.strftime('%Y-%m-%d %H-%M-%S')
# 获取项目路径
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 定义测报告的路径
REPORT_PATH =  os.path.join(BASE_PATH,'public\\report\\report%s.xlsx'%now)
# 定义日志文件的路径
INFO_LOG_PATH = os.path.join(BASE_PATH,'log\\info.log')
ERROR_LOG_PATH = os.path.join(BASE_PATH,'log\\error.log')
#定义响应时间图路径
RES_TIME = os.path.join(BASE_PATH,'public\\report\\rtime\\%srTime.jpg'%now)
#定义十次异常统计路径
TEN_TIMES = os.path.join(BASE_PATH,'public\\report\\tenTimes\\%srTime.jpg'%now)