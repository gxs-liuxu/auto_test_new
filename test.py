from public.interface.process_class import process_class
from public.interface.excel_database_exchange import to_database
from public.opReport import opExcel


def main():
    a = process_class()
    #a.set_test_process(('登录=>登录','注册')) #支持tuple和list。使用单引号隔开，不要使用双引号
    a.set_test_project('股先生APP')
    a.set_test_task("日常巡检")
    #a.set_global_dict({"username":"15921757467","password":""})
    a.run()

    #生成报告
    report = opExcel()
    report.GenCondition(report.worksheet,project_name="股先生",version="3.0.0",env="内网")
    report.AbInformation(report.worksheet2)
    report.workbook.close()


if __name__ == '__main__':
    main()




    # 指定表接口、流程入数据库
    #to_database(r"C:\Users\Administrator\Desktop\interface.xls")