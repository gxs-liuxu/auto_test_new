from public.interface.process_class import process_class
from public.interface.excel_database_exchange import to_database
from public.common.common import modify_hosts
from config.config import hosts

def main():
    #modify_hosts(hosts['CXTyf'])
    a = process_class()
    #a.set_test_process(['APP数据中心']) #list内使用单引号隔开，不要使用双引号
    # a.set_test_project("股先生APP")
    a.set_test_task("行情接口")
    dict_set = {"appcode":"5c6bb51a113c8szji5nb6cur"}
    a.set_global_dict(dict_set)
    a.run()
    print("dev")


if __name__ == '__main__':
    #to_database(r"C:\Users\Administrator\Desktop\interface.xls")
    main()



