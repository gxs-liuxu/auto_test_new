from config.config import database_config
from public.mysql_handle import mysql_handle

def sql_exc(sql,net_name = 'gxs_lan',database = 'gxs_test'):
    '''
    sql执行
    :param net_name: config中配置的数据库连接数据
    :param sql: sql语句
    :param database: 指定数据库名
    :return: 成功返回执行结果，失败返回False
    '''
    mh = mysql_handle(database_config[net_name]['host'], database_config[net_name]['port'],database_config[net_name]['user'], database_config[net_name]['password'])
    mh.mysql_connect()
    if mh.status == 1:
        mh.mysql_select_db(database)
        result = mh.exc_sql(sql)
        mh.mysql_close_db()
        return result
    else:
        return False
