#coding:utf-8
import requests
import warnings
from public.common.log import *

#过滤掉警告
warnings.filterwarnings('ignore')

class requests_handle():
    #初始化
    def __init__(self, method = '', url = '', body = '', headers = '', verify = False):
        self.method = method
        self.url = url
        self.body = body
        self.headers = headers
        self.verify = verify
        self.result = None
        self.return_data = {
            "status" : '',
            "exception" : '',
            "response_data" : '',
            "status_code" : ''
        }

        #设置requests参数
    def set_requests_para(self, method, url, body = '', headers = '', verify = False):
        self.method = method
        self.url = url
        self.body = body
        self.headers = headers
        self.verify = verify

    #执行request请求，支持get和post方法
    def exc_requests(self):
        #method不区分大小写
        if self.method.lower() not in ('get', 'post'):
            logging.error('暂未配置get以及post外的方法!\n\t请求方法为\t' + str(self.method))
            self.return_data['status'] = False
            self.return_data['exception'] = 'Error! 错误的请求Method : ' + str(self.method)
            return self.return_data
        elif str(self.url)[:7].lower() != 'http://' and str(self.url)[0:8].lower() != 'https://':
            logging.error('URL配置错误，请正确配置URL后使用\n\t请求URL为:\t' + str(self.url))
            self.return_data['status'] = False
            self.return_data['exception'] = 'Error! 错误的请求Url : ' + str(self.url)
            return self.return_data
        elif self.method.lower() == 'get':
            try:
                logging.info('request请求\n\t请求方法为:\t' + str(self.method) + '\n\t请求URL为:\t' + str(self.url))
                self.result = requests.get(self.url, self.verify)
                self.return_data['status'] = True
                self.return_data['response_data'] = self.result.text
                self.return_data['status_code'] = self.result.status_code
                return self.return_data
            except requests.RequestException as e:
                logging.error('request请求接口失败\n\t请求方法为:\t' + str(self.method) + '\n\t请求URL为:\t' + str(self.url) + '\n\t异常信息为:\t' + str(e))
                self.return_data['status'] = False
                self.return_data['exception'] = 'Error! 异常信息 : ' + str(e)
                return self.return_data
        elif self.method.lower() == 'post':
            try:
                logging.error('request请求接口\n\t请求方法为:\t' + str(self.method) + '\n\t请求URL为:\t' + str(self.url) + '\n\t请求Body为:\t' + str(self.body) + '\n\t请求Headers为:\t' + str(self.headers))
                self.result = requests.post(self.url, data = self.body, headers = self.headers, verify = self.verify)
                self.return_data['status'] = True
                self.return_data['response_data'] = self.result.text
                self.return_data['status_code'] = self.result.status_code
                self.return_data['elapsed_time'] = self.result.elapsed.total_seconds()
                return self.return_data
            except requests.RequestException as e:
                logging.error('request请求接口失败\n\t请求方法为:\t' + str(self.method) + '\n\t请求URL为:\t' + str(self.url) + '\n\t请求Body为:\t' + str(self.body) + '\n\t请求Headers为:\t' + str(self.headers) + '\n\t异常信息为:\t' + str(e))
                self.return_data['status'] = False
                self.return_data['exception'] = 'Error! 异常信息 : ' + str(e)
                return self.return_data
            

