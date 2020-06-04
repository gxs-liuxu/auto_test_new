from public.common.common import *
from public.requests_handle import requests_handle
from public.common.date import *
from public.common.sql_exc import sql_exc
from time import sleep

class interface_test():
    def __init__(self):
        self.interface_data = {}        #接口数据
        self.rq_result = ''             #请求结果
        self.log_data = {
            'report_record': ''
        }                   #日志数据
        self.response_data_json = False #json格式的响应数据

    @classmethod
    def get_interface_row_data(cls, interface_tag):
        '''
        根据inferface_tag获取指定接口基础数据
        :param interface_tag: interface_tag数据库需唯一
        :return: sql执行结果
        '''
        sql = "SELECT interface_tag,main_module,second_module,third_module,method,url,body,headers,is_check,checkpoint,interface_status,project,pre_wait_time from interface_base_data WHERE interface_tag = \'" + str(interface_tag) + "\'"
        return sql_exc(sql)


    def row_to_interface_data(self, sql_row_result):
        '''
        单行接口数据转字典
        :param sql_row_result: 数据库interface_base_data查询结果中单行数据
        :return: 单行数据处理为数据字典
        '''
        self.interface_data['interface_tag'] = sql_row_result[0]
        self.interface_data['main_module'] = sql_row_result[1]
        self.interface_data['second_module'] = sql_row_result[2]
        self.interface_data['third_module'] = sql_row_result[3]
        self.interface_data['method'] = sql_row_result[4]
        self.interface_data['url'] = sql_row_result[5]
        self.interface_data['body'] = sql_row_result[6]
        self.interface_data['headers'] = sql_row_result[7]
        self.interface_data['is_check'] = sql_row_result[8]
        self.interface_data['checkpoint'] = sql_row_result[9]
        self.interface_data['interface_status'] = sql_row_result[10]
        self.interface_data['project'] = sql_row_result[11]
        self.interface_data['pre_wait_time'] = sql_row_result[12]


    def response_data_to_json(self):
        self.response_data_json = str_to_json(self.log_data['response_data'])


    def check_checkpoint(self):
        '''
        检查点验证
        :param response_data: 接口响应数据
        :param checkpoint: 断言，支持多个断言用;隔开
        :return: 断言结果
        '''

        #响应数据转换为dict
        interface_test.response_data_to_json(self)
        #可执行字符串包含response_data_dict
        response_data_dict = self.response_data_json

        #接口响应失败判断
        if self.response_data_json is False:
            return False

        #多个检查点拆分为list
        checkpoint_list = self.interface_data['checkpoint'].split(';')

        #断言结果
        check_result_list = []

        for cps in checkpoint_list:
            #获取断言执行字符串
            try:
                check_result = interface_test.checkpointstr_to_excstr(cps.strip())
            # except:
            #     #字符串转换异常
            #     check_result = 'None'
            #     check_result_list.append('None')
            #     self.log_data['remark'] += '断言转换为可执行字符串异常,断言为：' + str(cps)
            #
            # try:
                if check_result is False:
                    check_result_list.append('False')
                elif eval(check_result):
                    check_result_list.append('Yes')
                else:
                    check_result_list.append('No')
            except:
                check_result_list.append('None')
                self.log_data['remark'] += '断言异常,断言为：' + str(cps)

        self.log_data['check_result'] = check_result_list


    @classmethod
    def format_variable_str(cls,variable_position_str, need_format_str = "response_data_dict"):
        '''
        辅助断言及出参定位提取变量位置,默认字典数据response_data_dict
        :param variable_position_str: 变量在替换字典或list中的层级字符串，分层用:隔开
        :param return_format_str: 默认响应结果的字典数据
        :return return_format_str: 响应结果中指定位置的字符串
        '''
        variable_position_list = variable_position_str.split(':')
        return_format_str = need_format_str
        for i in variable_position_list:
            try:
                int(i)
                return_format_str += "[" + i + "]"
            except:
                return_format_str += "[\'" + i + "\']"
        return return_format_str

    @classmethod
    def checkpointstr_to_excstr(cls, checkpoint_str):
        """
        断言转换为可执行字符串,默认的响应结果为字符串response_data， 字典数据response_data_dict
        :param checkpoint_str: checkpoint str，格式可为 单个字符串，判断式字符串（判断符前后需单个空格隔开，判断符支持：=,>,<,!=,>=,<=,in,notin）
        :return: 可执行字符串
        """
        cps = checkpoint_str.split(' ')
        #判断非指定格式的断言字符串，返回False
        if len(cps) not in (1,3):
            return False

        #判断为单个字符串,或字符串，并构造可执行表达式
        if len(cps) == 1:
            return "\'" + cps[0] + "\' in self.log_data[\'response_data\']"
        else:
            #构建检查点
            if (':' in cps[0]) and str(cps[0])[0] != ':' and str(cps[0])[-1] != ':':
                format_variable = interface_test.format_variable_str(cps[0])
            else:
                format_variable = "response_data_dict[\'" + str(cps[0]) + "\']"

            #判断表达式类型
            if(cps[1] == '='):
                return format_variable + " == " + str(cps[2])
            elif(cps[1] in ('>', '<', '!=', '>=', '<=')):
                return format_variable + str(cps[1]) + str(cps[2])
            elif(cps[1] == 'in'):
                return format_variable + " in " + str(cps[2])
            elif(cps[1] == 'notin'):
                return format_variable + " not in " + str(cps[2])
            else:
                return False

    def set_check_status(self):
        '''
        断言通过与否判断
        :param check_result: 断言结果
        :return: 0为不通过，1为通过
        '''
        check_status = 1
        for cr in self.log_data['check_result']:
            if cr != 'Yes':
                check_status = 0
                break
        self.log_data['check_status'] = check_status

    def set_is_check(self, is_check):
        '''
        设置是否断言判定
        :param is_check: 0或者1
        '''
        self.interface_data['is_check'] = is_check

    def set_checkpoint(self, checkpoint):
        '''
        断言设置，方便流程执行需使用的新断言覆盖接口基础数据表获取的断言
        :param checkpoint: 断言；多个断言用;隔开,判定符前后加上空格，支持比较符、包含in、不包含notin。如：code = 1;status > 2;num in (4,5,6)
        '''
        self.interface_data['checkpoint'] = checkpoint

    def pre_sleep_time(self):
        '''
        接口执行前时间等待
        :return: 无
        '''
        try:
            sleep(float(self.interface_data['pre_wait_time']))
        except:
            sleep(0)

    def interface_exc(self):
        '''
        接口执行并存日志
        :param interface_data: 接口基础数据
        :return:接口执行日志
        '''

        #构建日志
        self.log_data['interface_tag'] = self.interface_data['interface_tag']
        self.log_data['project'] = self.interface_data['project']
        self.log_data['url'] = self.interface_data['url']
        self.log_data['method'] = self.interface_data['method']
        self.log_data['body'] = self.interface_data['body']
        self.log_data['headers'] = self.interface_data['headers']
        self.log_data['module'] = self.interface_data['main_module']
        self.log_data['response_data'] = ''
        self.log_data['response_status'] = ''
        self.log_data['status_code'] = ''
        self.log_data['check_result'] = ''
        self.log_data['check_status'] = 0
        self.log_data['remark'] = ''

        if self.interface_data['second_module']:
            self.log_data['module'] += " => " + self.interface_data['second_module']
        if self.interface_data['third_module']:
            self.log_data['module'] += " => " + self.interface_data['third_module']

        self.log_data['checkpoint'] = self.interface_data['checkpoint']
        self.log_data['is_check'] = self.interface_data['is_check']

        if self.interface_data['headers']:
            headers = eval(self.interface_data['headers'])
            # headers = {
            #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            # }
        else:
            headers = self.interface_data['headers']

        if self.interface_data['interface_status'] == 0:
            self.log_data['remark'] = "Warning! 接口状态为不可使用：" + self.interface_data['interface_tag']
            return False

        #接口执行前等待
        interface_test.pre_sleep_time(self)

        rh = requests_handle(self.interface_data['method'], self.interface_data['url'], self.interface_data['body'],headers)
        begin_time = get_time_stamp()
        self.rq_result = rh.exc_requests()
        #end_time = get_time_stamp()
        #use_time = time_dif(begin_time, end_time)

        self.log_data['exc_time'] = str(begin_time)
        self.log_data['response_time'] = ''

        #接口响应结果判断
        if self.rq_result['status']:
            self.log_data['response_data'] = self.rq_result['response_data']
            self.log_data['status_code'] = self.rq_result['status_code']
            self.log_data['response_time'] = self.rq_result['elapsed_time']


            #断言判断
            #print(self.log_data)
            if self.log_data['is_check']:
                interface_test.check_checkpoint(self)
                if self.log_data['check_result']:
                    interface_test.set_check_status(self)
                else:
                    self.log_data['remark'] = 'Error! 接口响应数据转换为json失败'
        else:
            self.log_data['remark'] = self.rq_result['exception']

    @staticmethod
    def set_escape_character(sq_str):
        if "'" in sq_str:
            return "\\\'".join(sq_str.split("'"))
        if '"' in sq_str:
            return "\\\"".join(sq_str.split('"'))
        else:
            return sq_str

    def write_interface_exc_log_database(self):
        '''
        写接口执行日志入数据库
        :param log_data: 接口执行日志
        :param net_name: 网络环境名
        :param database: 指定数据库
        :return: 数据库写入结果
        '''

        sql = "INSERT INTO interface_exc_log (interface_tag,`module`,method,url,headers,body,exc_time,response_time,status_code,response_data,is_check,checkpoint,check_result,check_status,remark,project,report_record) VALUES (\'" + \
              self.log_data['interface_tag'] + "\',\'"+ self.log_data['module'] + "\',\'"+ self.log_data['method'] + "\',\'"+ self.log_data['url'] + "\',\'"+ self.log_data['headers'] + "\',\'" \
               + str(self.log_data['body']) + "\',\'"+ str(self.log_data['exc_time']) + "\',\'"+ str(self.log_data['response_time']) + "\',\'"+ str(self.log_data['status_code']) + "\',\'"+ str(interface_test.set_escape_character(self.log_data['response_data'])) + "\',\'" \
               + str(self.log_data['is_check']) + "\',\'"+ str(self.log_data['checkpoint']) + "\',\""+ str(self.log_data['check_result']) + "\",\""+ str(self.log_data['check_status']) + "\",\""+ str(interface_test.set_escape_character(self.log_data['remark'])) + "\",\'" \
              + str(self.log_data['project']) + "\',\'"+ str(self.log_data['report_record']) + "\')"

        sql_exc(sql)

