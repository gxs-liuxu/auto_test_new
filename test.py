from public.interface.process_class import process_class
from public.common.common import modify_hosts
from config.config import hosts

def main():
    #modify_hosts(hosts['CXTyf'])
    a = process_class()
    a.set_test_process(['后台登录']) #list内使用单引号隔开，不要使用双引号
    # a.set_test_project("股先生APP")
    # a.set_test_task("日常巡检")
    a.run()
    print("dev")


if __name__ == '__main__':
    main()

