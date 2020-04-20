#coding:utf-8
import pymysql
from .common.log import *

class mysql_handle():
    #初始化
    def __init__(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = ''
        self.conn = ''
        self.cur = ''
        #数据库连接状态，0为未连接，1为已连接
        self.status = 0

    #连接数据库
    def mysql_connect(self):
        try:
            self.conn = pymysql.connect(host = self.host, passwd = self.password, port = self.port, user = self.user, charset = "utf8")
            self.cur = self.conn.cursor()
            self.status = 1
            #logging.info('数据库连接成功.')
        except pymysql.Error as e:
            logging.error('数据库连接失败.\n\tERROR:' + str(e))
            print('mysql_connect error')

    #选择指定库
    def mysql_select_db(self, database):
        self.database = database
        try:
            self.conn.select_db(database)
            logging.info('选择数据库:' + database + '成功.')
        except pymysql.Error as e:
            logging.error('选择数据库:' + database + '失败.' + '\n\tERROR:' + str(e))
            print('mysql_select_db error')

    #关闭数据库
    def mysql_close_db(self):
        self.conn.close()
        logging.info('数据库关闭成功.')


    #sql查询命令执行,返回执行结果
    def exc_sql(self,sql):
        try:
            #返回结果list保存, return_result['row_num']为查询结果行数, return_result[1]为查询结果详细数据
            # return_result = []
            # return_result.append(self.cur.execute(sql))
            # self.conn.commit()
            # return_result.append(self.cur.fetchall())
            return_result = {}
            return_result['row_num'] = self.cur.execute(sql)
            self.conn.commit()
            return_result['data'] = self.cur.fetchall()
            logging.info('SQL执行成功:' + sql)
            return return_result
        except pymysql.Warning as w:
            logging.warning('WARNING:' + str(w))
            return False
        except pymysql.Error as e:
            logging.error('SQL执行失败!\n\tSQL:(' + sql + ')\n\tERROR:' + str(e))
            return False




        


    


