# -*-coding: utf-8 -*-
import json
import pymysql as pm


class Save2Mysql:
    def __init__(self):
        # 打开数据库连接
        self.db = pm.connect("localhost", "root", "Welcome1", "test", charset='utf8')
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()

    def insert(self, data):
        sql = "INSERT INTO tmallshoes(title,link, price, deal, shop) VALUES ('%s', '%s', '%s', '%s', '%s' )" % (
            ''.join(data['title']), ''.join(data['link']), ''.join(data['price']), ''.join(data['deal']),
            ''.join(data['shop']))
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 提交到数据库执行
            self.db.commit()
        except:
            # 发生错误时回滚
            self.db.rollback()
        finally:
            self.close()

    def close(self):
        self.db.close()

    def save_to_mysql(self):
        data = []
        with open('../tmallshoes/result.json', 'r', encoding='utf-8') as json_file:
            for line in json_file:
                data.append(json.loads(line))
                self.insert(json.loads(line))


def main():
    save = Save2Mysql()
    save.save_to_mysql()


if __name__ == '__main__':
    main()
