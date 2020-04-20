from public.mysql_handle import mysql_handle
from public.xlrd_handle import xlrd_handle
from config.config import database_config

net_name = 'gxs_lan'
mh = mysql_handle(database_config[net_name]['host'],database_config[net_name]['port'],database_config[net_name]['user'],database_config[net_name]['password'])
mh.mysql_connect()
if mh.status == 1:
    mh.mysql_select_db('app.combine')
    sql = "SELECT id, business_id,available_balance,blocked_balance,init_balance,title,CASE `status` WHEN 0 THEN \'预售中\' WHEN 1 THEN \'运作中\' WHEN 2 THEN \'已完成\' WHEN 3 THEN \'已终止\' WHEN 1 THEN \'已失效\' END FROM pool_pool LIMIT 10,8"
    result = mh.exc_sql(sql)
    mh.mysql_close_db()
    if result[0] != 0:
        xh = xlrd_handle()
        xh.set_sheet_name('create')
        xh.set_file_path(r'C:\Users\Administrator\Desktop\abc.xls')
        xh.write_to_sheet(result[1], range(10,18), list[1,3,5,6,7,8,10])
