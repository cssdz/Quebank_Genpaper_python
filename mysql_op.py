#!/usr/bin/python3
import pymysql


class DBManager:
    def __init__(self, host='localhost', user='root',
                 passwd='zixingche', db='student'):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.conn = None
        self.cur = None

    # 连接数据库
    def connectDatabase(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd,
                                        db=self.db)
        except:
            print("【数据库操作】connectDatabase failed")
            return False
        self.cur = self.conn.cursor()
        return True

    # 关闭数据库
    def close(self):
        # 如果数据打开，则关闭；否则没有操作
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()
        return True

    # 执行数据库的sql语句,主要用来做插入操作
    def execute(self, sql, params=None, commit=False):
        # 连接数据库
        rowcount = 0
        res = self.connectDatabase()
        if not res:
            return False
        try:
            if self.conn and self.cur:
                # 正常逻辑，执行sql，提交操作
                rowcount = self.cur.execute(sql, params)
                # print(rowcount)
                if commit:
                    self.conn.commit()
                else:
                    pass
        except:
            print("【数据库操作】execute failed: " + sql)
            print("【数据库操作】params: " + str(params))
            self.close()
            return False
        return rowcount

    # 查询所有数据
    def fetchall(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            print("【数据库操作】fetchall查询无结果")
            return False
        self.close()
        results = self.cur.fetchall()
        # print("【数据库操作】fetchall查询成功" + str(results))
        print("【数据库操作】fetchall查询成功 len=%d " % len(str(results)))
        return results

    # 查询一条数据
    def fetchone(self, sql, params=None):
        res = self.execute(sql, params)
        if not res:
            print("【数据库操作】fetchone查询无结果")
            return False
        self.close()
        result = self.cur.fetchone()
        # print("【数据库操作】fetchone查询成功" + str(result))
        print("【数据库操作】fetchone查询成功 len=%d " % len(str(result)))
        return result

    # 增删改数据
    def edit(self, sql, params=None):
        res = self.execute(sql, params, True)
        if not res:
            print("【数据库操作】edit操作失败")
            return False
        self.conn.commit()
        self.close()
        print("【数据库操作】edit操作成功" + str(res))
        return res
