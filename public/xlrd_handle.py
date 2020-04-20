#coding:utf-8
import xlrd
from public.common.log import *
from xlutils.copy import copy

class xlrd_handle():
    #初始化Excel文件路径，sheet页名称
    def __init__(self, file_path = '', sheet_name = ''):
        self.file_path = file_path
        self.sheet_name = sheet_name
        self.workbook = None
        self.sheet = None
        self.list_data = None


    #打开Excel文件
    def open_workbook(self):
        try:
            self.workbook = xlrd.open_workbook(self.file_path)
        except:
            logging.error('打开Excel文件失败.\n\tExcel文件路径为：\t' + str(self.file_path))
            self.workbook = None
            return False
            
    #选择sheet页
    def open_sheet(self):
        try:
            self.sheet = self.workbook.sheet_by_name(self.sheet_name)
        except:
            logging.error('选取Sheet页失败.\n\tExcel文件路径为：\t' + str(self.file_path) + '\n\t尝试打开的Sheet页名称为:\t' + str(self.sheet_name))
            self.sheet = None
            return False

    #设置Excel文件路径
    def set_file_path(self, file_path):
        self.file_path = file_path

    #设置sheet页名称
    def set_sheet_name(self, sheet_name):
        self.sheet_name = sheet_name


    #将指定sheet页中全部数据存入list返回
    def value_to_array(self):
        return_value = []
        try:
            if self.sheet.nrows > 0:
                for i in range (0, self.sheet.nrows):
                    return_value.append(self.sheet.row_values(i))
            else:
                logging.warning('sheet页 ' + str(self.sheet_name) + ' 的数据为空')
            return return_value
        except:
            logging.error('读取Excel数据失败.\n\tExcel文件路径为：\t' + str(self.file_path) + '\n\t尝试读取的Sheet页数据为:\t' + str(self.sheet_name))
            return False

    #将指定list或tuple数据写入sheet页中，指定行号list,tuple或range，指定列号list,tuple或range
    def write_to_sheet(self, write_list,row_list,range_list):
        if self.sheet_name == None:
            logging.error('未设置sheet页')
            return False
        if self.open_workbook() == False:
            return False
        if self.open_sheet() == False:
            return False
        if isinstance(write_list, list) == False and isinstance(write_list, tuple) == False and isinstance(write_list, range) == False:
            logging.error('写入数据类型非list或tuple类型：\n\t' + str(write_list)+ '\n\t' + str(type(write_list)) + '\n\t请重新录入')
            return False
        if len(write_list) == 0:
            logging.error('写入数据list为空：\n\t' + str(write_list) + '\n\t请重新录入')
            return False
        if isinstance(row_list, list) == False and isinstance(row_list, tuple) == False and isinstance(row_list, range) == False:
            logging.error('写入数据类型非list或tuple类型：\n\t' + str(row_list) + '\n\t' + str(type(row_list)) + '\n\t请重新录入')
            return False
        if len(row_list) == 0:
            logging.error('行号list为空：\n\t' + str(row_list) + '\n\t请重新录入')
            return False
        if isinstance(range_list, list) == False and isinstance(range_list, tuple) == False and isinstance(range_list, range) == False:
            logging.error('写入数据类型非list或非tuple或非range类型：\n\t' + str(range_list) + '\n\t' + str(type(range_list)) + '\n\t请重新录入')
            return False
        if len(range_list) == 0:
            logging.error('列号list为空：\n\t' + str(range_list) + '\n\t请重新录入')
            return False
        temp_excel = copy(self.workbook)
        sheet = temp_excel.get_sheet(0)
        for i in range(len(write_list)):
            if isinstance(write_list[i], list) == False and isinstance(write_list[i], tuple) == False and isinstance(write_list[i], range) == False:
                logging.error('写入单行数据类型非list或tuple类型：\n\t' + str(write_list[i]) + '\n\t' + str(type(write_list[i])) + '\n\t请重新录入')
                return False
            if len(write_list[i]) == 0:
                logging.error('写入单行数据为空')
                return False
            if len(write_list) != len(row_list):
                logging.error('写入行数与指定行数不一致：\n\t写入行数为：\t' + str(len(write_list)) + '\n\t指定行数为：\t' + str(len(row_list)) + '\n\t请重新录入')
                return False
            if len(write_list[i]) != len(range_list):
                logging.error('写入列数与指定列数不一致：\n\t 第\t' + str(i) + '行\n\t写入列数为：\t' + str(len(write_list[i])) + '\n\t指定列数为：\t' + str(len(range_list)) + '\n\t请重新录入')
                return False
            for j in range(len(range_list)):
                try:
                    sheet.write(row_list[i], range_list[j], str(write_list[i][j]))
                except Exception as e:
                    logging.error('写入数据失败：\n\t 第\t' + str(row_list[i]) + '\t行\n\t第\t' + str(range_list[j]) + '\t列\n\t录入数据为：\t' + str(write_list[i][j]) + '\n\t请重新录入\nException:\t' + str(e))
                    return False
                finally:
                    #copy_file_path = self.file_path.split('.')[0] + '_copy.' + self.file_path.split('.')[1]
                    copy_file_path = self.file_path.split('.')[0] + '.' + self.file_path.split('.')[1]
                    temp_excel.save(copy_file_path)
