from public.interface.process_class import process_class
from public.interface.excel_database_exchange import *

def to_database(file_path = r"E:\其他\测试\interface.xls"):
    # 指定表接口入数据库
    interface_excel_to_database(file_path)
    process_excel_to_database(file_path)

    # 数据库数据写入excel
    # database_table_to_excel(r"F:\test\write.xls")


def main():
    a = process_class()
    a.set_test_process(['行情=>自选']) #list内使用单引号隔开，不要使用双引号
    a.set_test_project('股先生APP')
    a.set_test_task("日常巡检")
    a.set_global_dict({"username":"15921757467","password":""})
    a.run()


if __name__ == '__main__':
    main()
    #to_database()
