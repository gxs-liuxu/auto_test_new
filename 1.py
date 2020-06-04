def add(a):
    return a + 1
print(add(5))
bb = "def add(a):\n    return a + 1\nprint(add(5))"
exec(bb)

global_dict = {}
process_data = {
    "output_parameter":1111111111
}

def format_variable_str(variable_position_str, need_format_str="response_data_dict"):
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

def outputparameter_to_dict():
    '''
    将出参数据存入流程全局参数中，global_dict
    '''

    temp_list = process_data['output_parameter'].split(";")
    for i in temp_list:
        if '=' in i:
            temp_output_parameter = i.split('=')[0]
            replace_parameter_temp = i.split('=')[1]
            if len(replace_parameter_temp) > 2 and replace_parameter_temp[0] == '|' and replace_parameter_temp[
                -1] == '|':
                replace_parameter = replace_parameter_temp[1:-1]
            else:
                replace_parameter = False
        else:
            temp_output_parameter = i
            replace_parameter = False

        # 特殊处理出参结果需变化的情况，<<为出参结果前置增加字符串，>>为出参结果后置增加字符串
        pre_str = ''
        suf_str = ''
        if '<<' in temp_output_parameter:
            pre_str = temp_output_parameter.split('<<')[0]
            temp_output_parameter = temp_output_parameter.split('<<')[1]
        if '>>' in temp_output_parameter:
            suf_str = temp_output_parameter.split('>>')[1]
            temp_output_parameter = temp_output_parameter.split('>>')[0]

        # 存在多层数据结构处理
        if ":" in temp_output_parameter and temp_output_parameter[0] != ':' and temp_output_parameter[-1] != ':':
            output_parameter = temp_output_parameter.split(':')[-1]
            try:
                output_value = eval(
                    format_variable_str(temp_output_parameter, "self.response_data_json"))
            except:
                output_value = ''
        else:
            output_parameter = temp_output_parameter
            try:
                output_value = eval("self.response_data_json[\'" + str(output_parameter) + "\']")
            except:
                output_value = ''

        if replace_parameter:
            global_dict[replace_parameter] = pre_str + str(output_value) + suf_str
        else:
            global_dict[output_parameter] = pre_str + str(output_value) + suf_str