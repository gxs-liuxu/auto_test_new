from public.xlrd_handle import xlrd_handle
from public.common.sql_exc import sql_exc

def interface_excel_to_database(file_path, sheet_name = '接口基础数据'):
    '''将excel里sheet页为interface_base_data的内容写入数据库interface_base_data表中'''
    xh = xlrd_handle()
    xh.set_file_path(file_path)
    xh.set_sheet_name(sheet_name)
    xh.open_workbook()
    xh.open_sheet()
    interface_data = xh.value_to_array()
    if interface_data:
        for i in range(1, len(interface_data)):
            sql = "INSERT INTO interface_base_data (interface_tag,project,main_module,second_module,third_module,method,url,headers,body,is_check,checkpoint,interface_status,remark,author,create_time,modify_time) VALUES (\'" +\
                  str(interface_data[i][0]) + "\',\'" + str(interface_data[i][1]) + "\',\'" + str(interface_data[i][2]) + "\',\'" + str(interface_data[i][3]) + "\',\'" + str(interface_data[i][4]) + "\',\'" + \
                  str(interface_data[i][5]) + "\',\'" + str(interface_data[i][6]) + "\',\'" + str(interface_data[i][7]) + "\',\'" + str(interface_data[i][8]) + "\',\'" + str(interface_data[i][9]) + "\',\'" + \
                  str(interface_data[i][10]) + "\',\'" + str(interface_data[i][11]) + "\',\'" + str(interface_data[i][12]) + "\',\'" + str(interface_data[i][13]) + "\', now(),now())"
            sql_exc(sql)


def process_excel_to_database(file_path, sheet_name = '流程记录'):
    '''将excel里sheet页为process_record的内容写入数据库process_record表中'''
    xh = xlrd_handle()
    xh.set_file_path(file_path)
    xh.set_sheet_name(sheet_name)
    xh.open_workbook()
    xh.open_sheet()
    interface_data = xh.value_to_array()
    if interface_data:
        for i in range(1, len(interface_data)):
            sql = "INSERT INTO process_record (project,task,process_tag,main_scene,second_scene,third_scene,process_status,is_exc,interface_tag,input_parameter,output_parameter,new_checkpoint,check_status,max_exc_num,max_fail_exc_num,success_jump,fail_jump,remark,author,create_time) VALUES (\'" +\
                  str(interface_data[i][0]) + "\',\'" + str(interface_data[i][1]) + "\',\'" + str(interface_data[i][2]) + "\',\'" + str(interface_data[i][3]) + "\',\'" + str(interface_data[i][4]) + "\',\'" + \
                  str(interface_data[i][5]) + "\',\'" + str(interface_data[i][6]) + "\',\'" + str(interface_data[i][7]) + "\',\'" + str(interface_data[i][8]) + "\',\'" + str(interface_data[i][9]) + "\',\'" + \
                  str(interface_data[i][10]) + "\',\'" + str(interface_data[i][11]) + "\',\'" + str(interface_data[i][12]) + "\',\'" + str(interface_data[i][13]) + "\',\'" + str(interface_data[i][14]) + "\',\'" + \
                  str(interface_data[i][15]) + "\',\'" + str(interface_data[i][16]) + "\',\'" + str(interface_data[i][17]) + "\',\'" + str(interface_data[i][18]) + "\', now())"
            sql_exc(sql)


def get_table_all_columns(table_name, table_schema = 'gxs_test'):
    '''获取指定表的全部字段名'''
    sql = "select GROUP_CONCAT(COLUMN_NAME) from information_schema.COLUMNS where table_name = \'" + str(table_name) + "\' and table_schema = \'" + str(table_schema) + "\'"
    return sql_exc(sql)


def columns_to_excel(table_name, file_path):
    '''
    数据库指定表字段名写入excel
    '''
    columns_result = get_table_all_columns(table_name)
    if columns_result:
        if columns_result['row_num'] == 1:
            write_data_temp = columns_result['data'][0][0].split(',')
            write_data = []
            write_data.append(write_data_temp)
            range_num = len(write_data_temp)
            xh = xlrd_handle()
            xh.set_file_path(file_path)
            xh.set_sheet_name(table_name)
            xh.open_workbook()
            xh.open_sheet()
            xh.write_to_sheet(write_data, [0], range(range_num))


def database_to_excel(table_name, file_path):
    '''
    数据库指定表数据写入excel
    '''
    sql_result = get_table_all_columns(table_name)
    if sql_result:
        if sql_result['row_num'] > 0:
            sql = "select " + sql_result['data'][0][0] + " from " + table_name
            write_data =  sql_exc(sql)

    if write_data:
        if write_data['row_num'] > 0:
            range_num = len(write_data['data'][0])
            xh = xlrd_handle()
            xh.set_file_path(file_path)
            xh.set_sheet_name(table_name)
            xh.open_workbook()
            xh.open_sheet()
            xh.write_to_sheet(write_data['data'],range(1,write_data['row_num'] + 1),range(range_num))



def database_table_to_excel(table_name, file_path):
    '''
    数据库指定表字段名和数据写入excel
    :param table_name:  表名
    :param file_path: excel路径
    '''
    columns_to_excel(table_name, file_path)
    database_to_excel(table_name, file_path)


#指定表接口入数据库
interface_excel_to_database(r"C:\Users\Administrator\Desktop\interface_xh.xls")
process_excel_to_database(r"C:\Users\Administrator\Desktop\interface_xh.xls")

#数据库数据写入excel
#database_table_to_excel(r"F:\test\write.xls")

