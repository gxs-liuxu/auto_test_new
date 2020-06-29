from public.interface.process_class import process_class
from public.interface.excel_database_exchange import to_database
from public.common.common import modify_hosts
from config.config import hosts

def main():
    #modify_hosts(hosts['CXTyf'])
    a = process_class()

    a.set_test_process(['APP股池']) #list内使用单引号隔开，不要使用双引号
    # a.set_test_project("股先生APP")
    #a.set_test_task("行情接口1")
    dict_set = {}
    a.set_global_dict(dict_set)

    a.run()
    print("master")


if __name__ == '__main__':
    #to_database()
    main()



