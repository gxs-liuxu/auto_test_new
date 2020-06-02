from public.interface.interface_class import interface_test
from public.common.date import get_date_time_str
from public.common.sql_exc import sql_exc
from public.common.date import *

class process_class():

    def __init__(self):
        interface_test.__init__(self)
        self.global_dict = {}       #流程全局数据字典，控制出参、入参
        self.global_Preset = 1      #前置设置全局数据字典状态，默认为1
        self.process_list = []      #测试整体流程list
        self.project = ''      #测试项目名
        self.task = ''          #测试任务名
        self.process_data = {}      #单个流程数据
        self.sql_result = False
        self.process_log_data = {}  #流程执行日志
        self.process_base_log = {}  #流程基础日志


    def set_begin_time(self):
        '''获取整个流程开始执行时间'''
        self.process_log_data['report_record'] = 'report_' + get_date_time_str()
        self.log_data['report_record'] = self.process_log_data['report_record']
        self.process_base_log['report_record'] = self.process_log_data['report_record']


    def set_test_process(self,process_list):
        '''
        根据测试流程列表process_list，设置测试内容
        :param process_list: 待测流程list
        '''
        self.process_list = process_list

    def set_test_project(self, project):
        '''
        设置待测项目名称
        :param project: 待测项目
        '''
        self.project = project

    def set_test_task(self, task):
        '''
        设置待测项目名称
        :param project: 待测项目
        '''
        self.task = task

    def set_global_dict(self, global_dict):
        '''
        设置待测流程前置全局数据字典
        :param global_dict: 待设置全局字典
        '''
        if type(global_dict) == dict:
            self.global_dict.update(global_dict)
        else:
            self.process_base_log['message'] = 'Error! 设置待测流程前置全局字典失败：' + str(global_dict)
            self.global_Preset = 0

    def process_take_apart(self, scene_name = ''):
        '''
        根据流程名，获取全部子流程的起始流程
        :param process_name: 待测项目名
        :param task_name: 待测任务名
        :param scene_name: 待测场景名,子场景中间用'=>'隔开，如：登录=>注册
        :return: 可执行流程起始流程list
        '''

        sql = "SELECT process_tag FROM process_record WHERE process_status = 0"
        if self.project != '':
            sql += " AND project = \'" + str(self.project) + "\'"
        if self.task != '':
            sql += " AND task = \'" + str(self.task) + "\'"

        process_scene_list = scene_name.split('=>')
        scene_num = len(process_scene_list)
        if scene_name != '' and '=>' not in scene_name:
            main_scene = scene_name
            sql += " And main_scene = \'" + str(main_scene) + "\'"
        if scene_num >= 2:
            main_scene = process_scene_list[0]
            second_scene = process_scene_list[1]
            sql += " And main_scene = \'" + str(main_scene) + "\' And second_scene = \'" + str(second_scene) + "\'"
        if scene_num == 3:
            third_scene = process_scene_list[2]
            sql += " And third_scene = \'" + str(third_scene) + "\'"
        return sql_exc(sql)



    def set_process_base_log(self):
        self.process_base_log['project'] = self.project
        self.process_base_log['task'] = self.task
        self.process_base_log['process_list'] = str(self.process_list)
        self.process_base_log['process_begin_time'] = get_time_stamp()
        self.process_base_log['process_end_time'] = ''


    def row_to_process_data(self, sql_row_result):
        '''
        单行流程数据转字典
        :param sql_row_result: 数据库process_record查询结果中单行数据
        :return: 单行数据处理为数据字典
        '''
        self.process_data['project'] = sql_row_result[0]
        self.process_data['process_tag'] = sql_row_result[1]
        self.process_data['main_scene'] = sql_row_result[2]
        self.process_data['second_scene'] = sql_row_result[3]
        self.process_data['third_scene'] = sql_row_result[4]
        self.process_data['process_status'] = sql_row_result[5]
        self.process_data['interface_tag'] = sql_row_result[6]
        self.process_data['input_parameter'] = sql_row_result[7]
        self.process_data['output_parameter'] = sql_row_result[8]
        self.process_data['new_checkpoint'] = sql_row_result[9]
        self.process_data['check_status'] = sql_row_result[10]
        self.process_data['max_exc_num'] = sql_row_result[11]
        self.process_data['max_fail_exc_num'] = sql_row_result[12]
        self.process_data['success_jump'] = sql_row_result[13]
        self.process_data['fail_jump'] = sql_row_result[14]
        self.process_data['is_exc'] = sql_row_result[15]
        self.process_data['task'] = sql_row_result[16]


    def inputparameter_to_dict(self):
        '''
        根据需求的入参和全局可使用的参数，构建可替换的入参，dict
        :return: 已替换完成的需要入参，dict
        '''

        return_inputparameter_dict = {}
        temp_list = self.process_data['input_parameter'].split(";")
        for i in temp_list:
            single_parameter = i.split("=")
            if len(single_parameter) == 1:
                if single_parameter[0] in self.global_dict.keys():
                    return_inputparameter_dict[single_parameter[0]] = self.global_dict[single_parameter[0]]
                else:
                    self.process_log_data['remark'] += "Error! 参数替换格式错误，全局可替换参数不存在：" + str(single_parameter[0]) + ' ! '
            elif len(single_parameter) == 2:
                #参数名与全局使用的参数名不一致处理时，需替换的全局参数名添加前后加上|来转换; 否则将等式做赋值处理
                if len(str(single_parameter[1])) > 2 and str(single_parameter[1])[0] == '|' and str(single_parameter[1])[-1] == '|':
                    if str(single_parameter[1])[1:-1] in self.global_dict.keys():
                        return_inputparameter_dict[single_parameter[0]] = self.global_dict[str(single_parameter[1])[1:-1]]
                    else:
                        self.process_log_data['remark'] += "Error! 参数替换格式错误，全局可替换参数不存在：" + str(single_parameter[1])[1:-1] + ' ! '
                else:
                    return_inputparameter_dict[single_parameter[0]] = single_parameter[1]
            else:
                self.process_log_data['remark'] += "Error! 参数替换格式错误，期望替换内容为：" + str(i)

        return return_inputparameter_dict


    def outputparameter_to_dict(self):
        '''
        将出参数据存入流程全局参数中，global_dict
        '''


        temp_list = self.process_data['output_parameter'].split(";")
        for i in temp_list:
            if '=' in i:
                temp_output_parameter = i.split('=')[0]
                replace_parameter_temp = i.split('=')[1]
                if len(replace_parameter_temp) > 2 and replace_parameter_temp[0] == '|' and replace_parameter_temp[-1] == '|':
                    replace_parameter = replace_parameter_temp[1:-1]
            else:
                temp_output_parameter = i
                replace_parameter = False

            #存在多层数据结构处理
            if ":" in temp_output_parameter and temp_output_parameter[0] != ':' and temp_output_parameter[-1] != ':':
                output_parameter = temp_output_parameter.split(':')[-1]
                try:
                    output_value = eval(interface_test.format_variable_str(temp_output_parameter, "self.response_data_json"))
                except:
                    self.process_log_data['remark'] += 'Error! 未获取出参为 ' + str(output_parameter) + ' 的数据'
                    output_value = ''
            else:
                output_parameter = temp_output_parameter
                try:
                    output_value = eval("self.response_data_json[\'" + str(output_parameter) + "\']")
                except:
                    self.process_log_data['remark'] += 'Error! 未获取出参为 ' + str(output_parameter) + ' 的数据'
                    output_value = ''

            if replace_parameter:
                self.global_dict[replace_parameter] = output_value
            else:
                self.global_dict[output_parameter] = output_value



    def get_process_record_row_data(self, process_tag):
        '''
        查询process_record中指定process_tag的数据，并返回
        :param process_tag: process_tag，数据库中需唯一
        :return: 查询数据
        '''
        sql = "SELECT project,process_tag,main_scene,second_scene,third_scene,process_status,interface_tag,input_parameter,output_parameter,new_checkpoint,check_status,max_exc_num,max_fail_exc_num,success_jump,fail_jump,is_exc,task from process_record WHERE process_tag = \'" + str(process_tag) + "\'"
        return sql_exc(sql)


    def change_checkpoint(self):
        '''
        流程中接口有新设置检查点，则修改接口基础数据表中获取的对应检查点为新检查点
        '''
        if self.process_data['new_checkpoint'] != '':
            interface_test.set_checkpoint(self, self.process_data['new_checkpoint'])


    def replace_get_url(self, replace_dict):
        '''
        :param replace_dict 需替换的参数dict:
        :return: 已构建好，可执行请求的url
        '''
        temp_url = self.interface_data['url'].split('?')

        if (len(temp_url)) == 2:
            url_base = temp_url[0]
            url_replace = temp_url[1]

            # url内容转换为dict数据
            url_replace_kv = {}
            for k in url_replace.split('&'):
                temp_k_v = k.split('=')
                #print(temp_k_v)
                if len(temp_k_v) == 2:
                    url_replace_kv[temp_k_v[0]] = temp_k_v[1]


            # 替换url
            url_replace_kv.update(replace_dict)

            url_replace_list = []
            for k, v in url_replace_kv.items():
                url_replace_list.append(str(k) + "=" + str(v))

            url_replace = url_base + '?' + '&'.join(url_replace_list)

            self.interface_data['url'] = url_replace


    def replace_post_body(self, replace_dict):
        '''

        :param replace_dict 需替换的参数dict:
        :return: 已构建好，可执行请求的body
        '''

        # body内容转换为dict数据
        body_replace_kv = {}
        for k in self.interface_data['body'].split('&'):
            temp_k_v = k.split('=')
            if len(temp_k_v) == 2:
                body_replace_kv[temp_k_v[0]] = temp_k_v[1]


        # 替换body
        body_replace_kv.update(replace_dict)

        body_replace_list = []
        for k, v in body_replace_kv.items():
            body_replace_list.append(str(k) + "=" + str(v))

        body_replace = '&'.join(body_replace_list)

        self.interface_data['body'] = body_replace

    def write_process_exc_log_database(self):
        '''
        写接口执行日志入数据库
        :param net_name: 网络环境名
        :param database: 指定数据库
        :return: 数据库写入结果
        '''

        sql = "INSERT INTO process_exc_log (project,task,process_tag,scene,process_status,is_exc,interface_tag,interface_exc_success_num,interface_exc_fail_num,interface_exc_time,exc_status,jump_process_tag,report_record,remark) VALUES (\'" + \
              self.process_log_data['project'] + "\',\'"+ self.process_log_data['task'] + "\',\'"+ self.process_log_data['process_tag'] + "\',\'"+ self.process_log_data['scene'] + "\',\'"+ str(self.process_log_data['process_status']) + "\',\'" \
               + str(self.process_log_data['is_exc']) + "\',\'"+ str(self.process_log_data['interface_tag']) + "\',\'"+ str(self.process_log_data['interface_exc_success_num']) + "\',\'"+ str(self.process_log_data['interface_exc_fail_num']) + "\',\'"+ str(self.process_log_data['interface_exc_time']) + "\',\'"+ str(self.process_log_data['exc_status']) + "\',\'"+ str(self.process_log_data['jump_process_tag']) + "\',\'"\
              + str(self.process_log_data['report_record']) + "\',\"" + str(interface_test.set_escape_character(self.process_log_data['remark'])) + "\")"

        sql_exc(sql)


    def write_process_base_log_database(self):
        '''
        写接口执行日志入数据库
        :param net_name: 网络环境名
        :param database: 指定数据库
        :return: 数据库写入结果
        '''

        sql = "INSERT INTO process_base_log (report_record,project,task,process_list,create_time,process_begin_time,process_end_time,message) VALUES (\'" + \
              self.process_base_log['report_record'] + "\',\'"+ self.process_base_log['project'] + "\',\'"+ self.process_base_log['task'] + "\',\""+ str(interface_test.set_escape_character(self.process_base_log['process_list'])) + "\",\'"+ str(self.process_base_log['create_time']) + "\',\'" \
               + str(self.process_base_log['process_begin_time']) + "\',\'"+ str(self.process_base_log['process_end_time']) + "\',\""+ str(interface_test.set_escape_character(self.process_base_log['message'])) + "\")"

        sql_exc(sql)


    def get_begin_process_list(self):
        '''
        根据配置的process_list，获取按顺序执行的所有流程的起始process_tag
        :return:  流程的起始process_tag， list
        '''
        begin_process_list = []
        if self.process_list != []:
            for p in self.process_list:
                temp_sql_result = self.process_take_apart(p)
                if temp_sql_result is not False:
                    for i in range(temp_sql_result['row_num']):
                        begin_process_list.append(temp_sql_result['data'][i][0])
        else:
            temp_sql_result = self.process_take_apart()
            if temp_sql_result is not False:
                for i in range(temp_sql_result['row_num']):
                    begin_process_list.append(temp_sql_result['data'][i][0])
        return begin_process_list

    def create_process_exc_log(self):
        '''
        构建流程执行日志
        '''
        self.process_log_data['project'] = self.process_data['project']
        self.process_log_data['task'] = self.process_data['task']
        self.process_log_data['process_tag'] = self.process_data['process_tag']
        self.process_log_data['scene'] = self.process_data['main_scene']
        if self.process_data['second_scene'] != '':
            self.process_log_data['scene'] += " => " + self.process_data['second_scene']
        if self.process_data['third_scene'] != '':
            self.process_log_data['scene'] += " => " + self.process_data['third_scene']
        self.process_log_data['process_status'] = self.process_data['process_status']
        self.process_log_data['is_exc'] = self.process_data['is_exc']
        self.process_log_data['interface_tag'] = self.process_data['interface_tag']
        self.process_log_data['interface_exc_success_num'] = ''
        self.process_log_data['interface_exc_fail_num'] = ''
        self.process_log_data['interface_exc_time'] = ''
        self.process_log_data['exc_status'] = ''
        self.process_log_data['jump_process_tag'] = ''
        self.process_log_data['remark'] = ''


    def run(self):
        '''执行'''

        #设置report_record
        self.set_begin_time()

        #预处理process_base_log日志
        self.set_process_base_log()

        #判断流程列表格式，必须是list,tuple
        if type(self.process_list) not in (list,tuple):
            self.process_base_log['process_end_time'] = get_time_stamp()
            self.process_base_log['create_time'] = get_time_stamp()
            self.process_base_log['message'] = 'Error! 流程设置的数据类型应为list, 流程为： ' + str(self.process_list) + '; 数据类型为： ' +'\\\''.join(str(type(self.process_list)).split('\''))
            self.write_process_base_log_database()
            return False

        #判断前置设置全局数据字典状态,设置为0时，流程整体异常退出
        if self.global_Preset == 0:
            self.process_base_log['process_end_time'] = get_time_stamp()
            self.process_base_log['create_time'] = get_time_stamp()
            self.write_process_base_log_database()
            return False

        #获取按顺序执行的所有流程的起始process_tag
        begin_process_list = self.get_begin_process_list()


        if begin_process_list == []:
            self.process_base_log['process_end_time'] = get_time_stamp()
            self.process_base_log['create_time'] = get_time_stamp()
            self.process_base_log['message'] = 'Warning! 未能获取流程执行起始process_tag,  获取的begin_process_list为: ' + interface_test.set_escape_character(str(self.process_list))
            self.write_process_base_log_database()
            return False

        for n in begin_process_list:
            process_tag = n
            while(process_tag != 'end'):
                #获取单个流程数据
                process_record_row = self.get_process_record_row_data(process_tag)
                #流程数据转为dict格式, 若获取流程数据失败则退出当前流程
                if process_record_row['data'] == ():
                    self.process_base_log['create_time'] = get_time_stamp()
                    self.process_base_log['message'] = 'Error! 获取流程数据失败，退出当前流程: ' + str(process_tag) + ', 起始流程为： ' + str(n)
                    self.write_process_base_log_database()
                    break
                self.row_to_process_data(process_record_row['data'][0])

                #构建流程日志
                self.create_process_exc_log()

                #判断当前流程是否可执行,不可执行退出当前流程
                if self.process_data['is_exc'] == 0:
                    self.process_log_data['remark'] += 'Error！ 当前流程已设置为不可执行'
                    self.write_process_exc_log_database()
                    break

                #获取流程接口数据
                interface_sql_row = interface_test.get_interface_row_data(self.process_data['interface_tag'])
                if interface_sql_row is False:
                    self.process_log_data['remark'] += 'Error! 获取接口数据失败：' + str(self.process_data['interface_tag'])
                    self.write_process_exc_log_database()
                    break
                else:
                    if interface_sql_row['row_num'] == 0:
                        self.process_log_data['remark'] += 'Error! 未查询到指定接口数据：' + str(self.process_data['interface_tag'])
                        self.write_process_exc_log_database()
                        break
                    #接口数据转为dict格式
                    self.sql_row_result = interface_test.row_to_interface_data(self, interface_sql_row['data'][0])
                    #检查点替换
                    self.change_checkpoint()
                    #入参替换
                    if self.process_data['input_parameter'] != '':
                        inputparameter_dict = self.inputparameter_to_dict()
                        if self.interface_data['method'].lower() == 'get':
                            self.replace_get_url(inputparameter_dict)
                        elif self.interface_data['method'].lower() == 'post':
                            self.replace_post_body(inputparameter_dict)

                    #判断连续执行次数，最大失败次数。当接口连续多次执行时，当达到设置执行次数或达到最大执行次数时退出
                    max_exc_num = self.process_data['max_exc_num']
                    max_fail_exc_num = self.process_data['max_fail_exc_num']
                    success_num = 0
                    fail_num = 0
                    while(max_exc_num):
                        #接口请求执行
                        interface_test.interface_exc(self)
                        # 写接口执行日志入数据库
                        interface_test.write_interface_exc_log_database(self)
                        if self.log_data['status_code'] == 200 and self.log_data['check_status'] == 1:
                            success_num += 1
                            max_exc_num -= 1
                            if success_num + fail_num == self.process_data['max_exc_num']:
                                break
                        else:
                            fail_num += 1
                            if fail_num == max_fail_exc_num:
                                break

                    self.process_log_data['interface_exc_success_num'] = success_num
                    self.process_log_data['interface_exc_fail_num'] = fail_num
                    self.process_log_data['interface_exc_time'] = self.log_data['exc_time']

                    # 判断接口执行状态码和检查状态，提取出参，流程跳转判断
                    if self.log_data['status_code'] == 200 and self.log_data['check_status'] == 1:
                        if self.process_data['output_parameter'] != '':
                            self.outputparameter_to_dict()
                        process_tag = self.process_data['success_jump']
                        self.process_log_data['exc_status'] = 1
                        self.process_log_data['jump_process_tag'] = self.process_data['success_jump']
                    else:
                        process_tag = self.process_data['fail_jump']
                        self.process_log_data['exc_status'] = 0
                        self.process_log_data['jump_process_tag'] = self.process_data['fail_jump']
                        self.process_log_data['remark'] += 'Error! 流程执行失败' + str(self.process_data['process_tag'])

                    self.write_process_exc_log_database()


        self.process_base_log['process_end_time'] = get_time_stamp()
        self.process_base_log['create_time'] = get_time_stamp()
        self.process_base_log['message'] = 'Finish! 流程执行完成！'
        self.write_process_base_log_database()






