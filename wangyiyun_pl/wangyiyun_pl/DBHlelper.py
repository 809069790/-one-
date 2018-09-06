import time
import pymysql
from twisted.enterprise import adbapi
from scrapy.utils.project import get_project_settings  #导入seetings配置


class DBHelper():
    '''这个类也是读取settings中的配置，自行修改代码进行操作'''

    def __init__(self):
        settings = get_project_settings()  #获取settings配置，设置需要的信息

        dbparams = dict(
            host=settings['MYSQL_HOST'],  #读取settings中的配置
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            charset='utf8mb4',  #编码要加上，否则可能出现中文乱码问题
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=False,
        )
        #**表示将字典扩展为关键字参数,相当于host=xxx,db=yyy....
        dbpool = adbapi.ConnectionPool('pymysql', **dbparams)

        self.dbpool = dbpool

    def connect(self):
        return self.dbpool

    #创建数据库
    def insert(self, item):
        sql = "insert into `song_pl` (`song_id`, `user_name`, `content`, `user_id`, `zan_counts`, `create_time`, `user_img`) values (%s,%s,%s,%s,%s,%s,%s)"
        #调用插入的方法
        query = self.dbpool.runInteraction(self.insert_to_mysql, sql, item)
        #调用异常处理方法
        query.addErrback(self._handle_error)
        return item

    #写入数据库中
    def insert_to_mysql(self, tx, sql, item):
        # print(item["id"], item['goodName'], item['old_price'], item['new_price'], item['xinghao'], item['user_name'], item['score'], item['content'], item['commentTime'], item['guige'])
        params = (item["song_id"], item['user_name'], item['content'], item['user_id'], item['zan_counts'], item['create_time'], item['user_img'])
        tx.execute(sql, params)

    #错误处理方法

    def _handle_error(self, failue):
        print('--------------database operation exception!!-----------------')
        print(failue)