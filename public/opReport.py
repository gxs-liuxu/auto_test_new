#Author:chen
#!/usr/bin/env python
#-*- coding: utf-8 -*-
import xlsxwriter
import time
from public.common.sql_exc import sql_exc
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

class opExcel(object):
    def __init__(self):
        self.time1 = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        try:
            self.workbook = xlsxwriter.Workbook('./public/report/testReport%s.xlsx'%time.strftime('%Y-%m-%d %H-%M-%S'))  # 新建Excel
            self.worksheet = self.workbook.add_worksheet("测试总况")  # 传入sheet名称
            #self.worksheet2 = self.workbook.add_worksheet("响应时间分布")
        except Ellipsis as e:
            print("新建excel遇到错误：",e)
        #self.worksheet2 = self.workbook.add_worksheet("测试详情")

    def get_format(self,wd,option={}):
        '''表格样式设置'''
        return wd.add_format(option)

    def get_format_center(self,wd, num=1):
        '''设置居中'''
        return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})

    def get_color(self,wd,color):
        return wd.set_font_color()

    def set_border_(self,wd, num=1):
        return wd.add_format({}).set_border(num)

    def _write_center(self,worksheet, cl, data, wd):
        '''写入Excel数据'''
        return worksheet.write(cl, data, self.get_format_center(wd))

    def GenCondition(self,worksheet,project_name=None,version=None,env=None):
        '''设置测试总况'''

        #设置行列宽高
        worksheet.set_column("A:A", 15)
        worksheet.set_column("B:B", 20)
        worksheet.set_column("C:C", 20)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 20)
        worksheet.set_column("F:F", 20)

        worksheet.set_row(1, 30)
        worksheet.set_row(2, 30)
        worksheet.set_row(3, 30)
        worksheet.set_row(4, 30)
        worksheet.set_row(5, 30)

        define_format_H1 = self.get_format(self.workbook, {'bold': True, 'font_size': 18})  # 设置字体加粗，字体大小
        define_format_H2 = self.get_format(self.workbook, {'bold': True, 'font_size': 14})
        define_format_H1.set_border(1) #设置表格边框
        define_format_H2.set_border(1)

        # 设置居中和颜色
        define_format_H1.set_align("center")
        define_format_H2.set_align("center")
        define_format_H2.set_bg_color("green")
        define_format_H2.set_color("#ffffff")

        worksheet.merge_range('A1:F1', '测试报告总概况', define_format_H1)
        worksheet.merge_range('A2:F2', '测试概括', define_format_H2)
        worksheet.merge_range('A3:A6', '详情',self.get_format_center(self.workbook))

        self._write_center(worksheet, "B3", '项目名称', self.workbook)
        self._write_center(worksheet, "B4", '接口版本', self.workbook)
        self._write_center(worksheet, "B5", '脚本语言', self.workbook)
        self._write_center(worksheet, "B6", '测试网络', self.workbook)

        data = {"test_name": project_name, "test_version": version, "test_pl": "Python", "test_env": env}
        self._write_center(worksheet, "C3", data['test_name'], self.workbook)
        self._write_center(worksheet, "C4", data['test_version'], self.workbook)
        self._write_center(worksheet, "C5", data['test_pl'], self.workbook)
        self._write_center(worksheet, "C6", data['test_env'], self.workbook)
        self._write_center(worksheet, "D3", "接口总数", self.workbook)
        self._write_center(worksheet, "D4", "通过总数", self.workbook)
        self._write_center(worksheet, "D5", "失败总数", self.workbook)
        self._write_center(worksheet, "D6", "测试日期", self.workbook)

        num = sql_exc("SELECT COUNT(*) FROM process_record")
        #print(num['data'][0][0])
        success = sql_exc("SELECT check_result FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d"%num['data'][0][0])
        #iss = sql_exc("SELECT exc_time FROM interface_exc_log ORDER BY id DESC LIMIT 0,22") #调试时间
        #print(iss)
        test_success = []
        test_failed = []
        for res in success['data']:
            i = '%s'%res[0]
            if 'No' in i:
                test_failed.append('fail')
            else:
                test_success.append('pass')
        #print(test_failed,test_success)
        #数量统计
        data1 = {"test_sum": num['data'][0][0],
                 "test_success": test_success.count('pass'),
                 "test_failed": test_failed.count('fail'),
                 "test_date": self.time1}
        self._write_center(worksheet, "E3", data1['test_sum'], self.workbook)
        self._write_center(worksheet, "E4", data1['test_success'], self.workbook)

        #失败数标红显示
        if data1['test_failed'] != 0:
            cell_format = self.workbook.add_format()
            cell_format.set_font_color('red')
            worksheet.write(4,4,data1['test_failed'],cell_format)
        else:
            self._write_center(worksheet, "E5", data1['test_failed'], self.workbook)

        self._write_center(worksheet, "E6", data1['test_date'], self.workbook)

        resTime = sql_exc("SELECT response_time FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d"%num['data'][0][0])
        rt = []
        for resT in resTime['data']:
            #print(resT[0])
            rt.append(float(resT[0]))#存进列表并转类型

        self._write_center(worksheet, "F3", "平均响应时间", self.workbook)
        worksheet.merge_range('F4:F6', sum(rt)/num['data'][0][0], self.get_format_center(self.workbook))#平均响应时间
        self.pie(self.workbook, worksheet)
        self.rtPic()  #绘图

    def pie(self, workbook, worksheet):
        '''生成饼状图'''
        chart1 = workbook.add_chart({'type': 'pie'})
        chart1.add_series({
            'name': '接口测试统计',
            'categories': '=测试总况!$D$4:$D$5',
            'values': '=测试总况!$E$4:$E$5',
        })
        chart1.set_title({'name': '接口测试统计'})
        chart1.set_style(10)
        worksheet.insert_chart('A9', chart1, {'x_offset': 25, 'y_offset': 10})

    def rtPic(self):
        '''绘制响应时间柱状图'''
        num = sql_exc("SELECT COUNT(*) FROM process_record")
        resTime = sql_exc("SELECT response_time FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d" % num['data'][0][0])
        y = []
        for resT in resTime['data']:
            y.append(float(resT[0]))  # 存进列表并转类型

        module_name = sql_exc("SELECT id FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d" % num['data'][0][0])
        x = []
        for name in module_name['data']:
            #print(name[0])
            x.append(name[0])

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        #plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.bar(range(len(y)),y,color='rgb',tick_label = x)
        plt.savefig('./public/report/rtime/%srTime.jpg'%time.strftime('%Y-%m-%d %H-%M-%S'))
        #plt.show()



if __name__=="__main__":
    op = opExcel()
    # 设置列行的宽高
    op.GenCondition(op.worksheet,project_name="股先生",version="3.0.0",env="内网",)
    op.workbook.close()
    op.rtPic()
