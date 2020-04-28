#Author:chen
#!/usr/bin/env python
#-*- coding: utf-8 -*-
import xlsxwriter
from public.common.sql_exc import sql_exc
import matplotlib.pyplot as plt
import warnings
from config.setting import *
import time

warnings.filterwarnings('ignore')

class opExcel(object):
    def __init__(self):
        self.time1 = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
        self.num = sql_exc("SELECT COUNT(*) FROM interface_exc_log WHERE report_record = (SELECT report_record FROM interface_exc_log ORDER BY id DESC LIMIT 1)")

        try:
            self.workbook = xlsxwriter.Workbook(REPORT_PATH)  # 新建Excel
            self.worksheet = self.workbook.add_worksheet("测试总况")  # 传入sheet名称
            self.worksheet2 = self.workbook.add_worksheet("异常信息详情")
            self.worksheet3 = self.workbook.add_worksheet("近10次测试结果统计")
        except Ellipsis as e:
            print("新建excel遇到错误：",e)

    def get_format(self,wd,option={}):
        '''表格样式设置'''
        return wd.add_format(option)

    def get_format_center(self,wd, num=1):
        '''设置居中'''
        return wd.add_format({'align': 'center', 'valign': 'vcenter', 'border': num})

    def set_border_(self,wd, num=1):
        return wd.add_format({}).set_border(num)

    def _write_center(self,worksheet, cl, data, wd):
        '''写入Excel数据'''
        return worksheet.write(cl, data, self.get_format_center(wd))

    def GenCondition(self,worksheet,project_name=None,version=None,env=None):
        '''
        设置测试总况
        :param worksheet: sheet名
        :param project_name: 项目名
        :param version: 版本名称
        :param env: 环境
        '''

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

        success = sql_exc("SELECT check_result FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d"%self.num['data'][0][0])
        test_success = []
        test_failed = []
        for res in success['data']:
            i = '%s'%res[0]
            if 'No' in i or 'None' in i:
                test_failed.append('fail')
            else:
                test_success.append('pass')
        #print(test_failed,test_success)
        #数量统计
        data1 = {"test_sum": self.num['data'][0][0],
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

        resTime = sql_exc("SELECT response_time FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d"%self.num['data'][0][0])
        rt = []
        for resT in resTime['data']:
            rt.append(float(resT[0]))#存进列表并转类型

        self._write_center(worksheet, "F3", "平均响应时间", self.workbook)
        worksheet.merge_range('F4:F6', sum(rt)/int(self.num['data'][0][0]), self.get_format_center(self.workbook))#平均响应时间
        self.pie(self.workbook, worksheet)

        # 插入响应时间图
        resTime = sql_exc(
            "SELECT response_time FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d" % self.num['data'][0][0])
        y = []
        for resT in resTime['data']:
            y.append(float(resT[0]))  # 存进列表并转类型

        module_name = sql_exc("SELECT id FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d" % self.num['data'][0][0])
        x = []
        for name in module_name['data']:
            x.append(name[0])

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        # plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.bar(range(len(y)), y, color='rgb', tick_label=x)
        plt.savefig(RES_TIME)
        plt.clf() #重置画布（必须，否则画布会重叠）
        #plt.show()

        worksheet.insert_image("H3", RES_TIME)
        define_format_H = self.get_format(self.workbook, {'bold': True, 'font_size': 18})
        define_format_H.set_border(1)  # 设置表格边框
        # 设置居中和颜色
        define_format_H.set_align("center")
        worksheet.merge_range('G1:P1', '响应时间柱状图', define_format_H)

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

    def AbInformation(self,worksheet):
        '''
        设置异常信息详情
        :param worksheet: sheet名
        异常定义：1、检查点失败；2、单接口响应时间超过2秒
        '''
        # 设置行列宽高
        worksheet.set_column("A:A", 5)
        worksheet.set_column("B:B", 15)
        worksheet.set_column("C:C", 15)
        worksheet.set_column("D:D", 20)
        worksheet.set_column("E:E", 30)
        worksheet.set_column("F:F", 30)
        worksheet.set_column("G:G", 10)
        worksheet.set_column("H:H", 30)
        worksheet.set_column("F:F", 10)
        worksheet.set_row(0, 40)
        worksheet.set_row(1, 20)
        worksheet.set_row(2, 20)
        worksheet.set_row(3, 20)
        worksheet.set_row(4, 20)

        #初始化名称
        hang = ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
        name = ['ID','interface_tag','项目名称','模块','url', 'body','响应时间','返回结果','是否通过']
        dicti = dict(zip(hang, name))
        for i,v in dicti.items():
            self._write_center(worksheet, str(i), str(v), self.workbook)

        #查询需要的异常数据
        req = sql_exc("SELECT b.id,b.interface_tag,b.project,b.module,b.url,b.body,b.response_time,b.response_data,b.check_status FROM interface_exc_log a INNER JOIN (SELECT * FROM interface_exc_log ORDER BY id DESC LIMIT 0,%d) b on a.id = b.id WHERE b.check_status = 0 or b.response_time > 1"% self.num['data'][0][0])
        req_data = req['data']
        expenses = []
        for i in  req_data:
            expenses.append(list(i))
        row = 1
        col = 0
        #写入异常数据，并对异常进行标红加粗处理
        for a1, b1,c1,d1,e1,f1,g1,h1,i1 in (expenses):
            worksheet.write(row, col, a1)
            worksheet.write(row, col + 1, b1)
            worksheet.write(row, col + 2, c1)
            worksheet.write(row, col + 3, d1)
            worksheet.write(row, col + 4, e1)
            worksheet.write(row, col + 5, f1)
            if float(g1) > 2:
                cell_format = self.workbook.add_format()
                cell_format.set_font_color('red')
                cell_format.set_bold()
                worksheet.write(row, col + 6, g1,cell_format)
            else:
                worksheet.write(row, col + 6, g1)

            worksheet.write(row, col + 7, h1)
            if int(i1) != 1:
                cell_format = self.workbook.add_format()
                cell_format.set_font_color('red')
                cell_format.set_bold()
                worksheet.write(row, col + 8, i1, cell_format)
            else:
                worksheet.write(row, col + 8, i1)
            row += 1

    def TenRes(self,worksheet):
        '''
        设置近十次测试结果统计
        :param worksheet: sheet名
        异常定义：1、检查点失败；2、单接口响应时间超过2秒
        '''

        define_format_H4 = self.get_format(self.workbook, {'bold': True, 'font_size': 18})
        define_format_H4.set_border(1)  # 设置表格边框
        # 设置居中和颜色
        define_format_H4.set_align("center")
        worksheet.merge_range('A1:J1', '近十次异常数统计', define_format_H4)
        xu = list(range(1, 11, 1))
        worksheet.write_row('A2', xu)#写入生成的序号

        req = sql_exc("SELECT DISTINCT report_record FROM interface_exc_log ORDER BY id DESC LIMIT 0, 10")
        req_data = list(req['data'])
        #转成列表，不然不能写入Excel

        res = []
        for i in req_data:
            i = list(i)
            res.append(i)
        lie = ['A3','B3','C3','D3','E3','F3','G3','H3','I3','J3']
        dicti= dict(zip(lie, res))#组成字典

        #转成字典格式键值对写入excel,构造数据e_dict
        e_dict = {}
        for i,v in dicti.items():
            self._write_center(worksheet, str(i), str(v[0]), self.workbook)
            e_data = sql_exc("SELECT COUNT(*) FROM interface_exc_log WHERE report_record = '%s' AND (check_status != 1 or response_time > 2)"%str(v[0]))
            e_dict[v[0]] = str(e_data['data'][0][0])
        lie2 = ['A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'I4', 'J4']
        values = []
        for vs in e_dict.values():
            values.append(vs)
        dic_data = dict(zip(lie2,values))

        #生成折线图
        data = []
        for da in dic_data.values():
            data.append(int(da))
        worksheet.write_row('A4', data) #写入数据

        plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        plt.plot(xu, data,lw=1, c='purple', marker='s', ms=4, label='异常统计')
        plt.title('近十次异常统计(左边测试时间最近，右边最远)')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.savefig(TEN_TIMES)
        worksheet.insert_image("A6", TEN_TIMES) #插入折线图
        #plt.show()

    def main(self):
        self.GenCondition(self.worksheet, project_name="股先生", version="3.0.0", env="内网")
        self.AbInformation(self.worksheet2)
        self.TenRes(self.worksheet3)
        self.workbook.close()


if __name__=="__main__":
    op = opExcel()
    op.main()
