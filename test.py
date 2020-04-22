from public.interface.process_class import process_class

def main():
    a = process_class()
    a.set_test_process(['看数据=>散户动态=>说明']) #list内使用单引号隔开，不要使用双引号
    a.set_test_project("股先生APP")
    a.set_test_task("日常巡检")
    a.run()
    print("11111")


if __name__ == '__main__':
    main()

