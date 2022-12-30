import mysql_op
import main

dbManager = mysql_op.DBManager()


class STUManager:  # 创建考生类
    def __init__(self, tab_name, column_1, call_1, call_2, column_2, column_3, value_1, value_2, value_3, option, sql):
        self.tab_name = tab_name
        self.column_1, self.column_2, self.column_3 = column_1, column_2, column_3
        self.call_1, self.call_2 = call_1, call_2
        self.value_1, self.value_2, self.value_3 = value_1, value_2, value_3
        self.option = option
        self.sql = sql

    def search_judge(self):  # 判断使用几个字段查询
        if self.option == '0':
            self.sql = "SELECT * FROM %s ORDER BY %s" % (self.tab_name, self.tab_name)

        if self.option == '1':
            self.value_1 = input("请输入%s：\n" % self.call_1)
            self.sql = "SELECT * FROM %s WHERE %s = '%s';" % (self.tab_name, self.column_1, self.value_1)

        if self.option == '2':
            self.value_2 = input("请输入%s：\n" % self.call_2)
            self.sql = "SELECT * FROM %s WHERE %s = %s AND %s = %s;" % (
                self.tab_name, self.column_1, self.value_1, self.column_2, self.value_2)

    def search_column(self):  # 查询字段信息
        tab_name = self.tab_name
        sql = "SELECT column_name FROM information_schema.columns WHERE table_name = '%s';" % tab_name
        print(sql)
        table_info = dbManager.fetchall(sql)
        return table_info

    def search_info(self):  # 查询信息
        self.search_judge()
        print(self.sql)
        info = dbManager.fetchall(self.sql)
        # print(info)

        if info is False:
            print("查无该%s\n" % self.call_1)
            return self.search_info()

        else:
            no = len(info)
            for i in range(no):
                print("编号%s" % (i + 1), "", info[i])
            return info, no

    def sub_edit(self):  # 化简sub_info和edit_info
        info_combine = self.search_info()
        if info_combine is False:
            return main
        info, no_1 = info_combine[0], info_combine[1]

        try:
            self.option = int(input("请输入编号：\n"))
        except TypeError:
            print("输入的不是数字！")
            return self.sub_info()

        if self.option not in range(0, (no_1 + 1)):
            print("输入编号有误")
            return self.sub_info()

        no_2 = self.search_column()
        # print(no_2)
        return info, no_2

    def add_info(self):  # 增加信息
        tab_name = self.tab_name
        default, no_1, no_2 = 0, 0, 0
        table, add_info = [], []
        str_add_info, str_table = "", ""

        for i in self.search_column():
            # print(i[0])
            add_info.append(i[0])
            # print(add_info)
            name = add_info[default]
            print("请输入", name, "信息")
            table.append(input())
            default += 1

        for i in add_info:
            str_add_info += i
            if no_1 < default - 1:
                str_add_info += ", "
            no_1 += 1

        for i in table:
            str_table += "'" + i + "'"
            if no_2 < default - 1:
                str_table += ", "
            no_2 += 1

        sql = "INSERT INTO %s ( " % tab_name + str_add_info + " ) VALUES ( " + str_table + ");"
        print(sql)
        dbManager.edit(sql)

    def sub_info(self):  # 删除信息
        info_combine = self.sub_edit()
        info, no_2 = info_combine[0], info_combine[1]

        for i in range(len(no_2)):
            # print(no_2[i][0])
            if no_2[i][0] == self.column_2:
                self.value_2 = info[self.option - 1][i]
            if no_2[i][0] == self.column_3:
                self.value_3 = info[self.option - 1][i]
        sql = "DELETE FROM %s WHERE (%s = '%s' AND %s = '%s');" % (
            self.tab_name, self.column_1, self.value_1, self.column_3, self.value_3)
        print(sql)
        dbManager.edit(sql)

    def edit_info(self):  # 修改信息
        info_combine = self.sub_edit()
        info, no_2 = info_combine[0], info_combine[1]
        column_info, course = [], 0

        for i in range(len(no_2)):
            if no_2[i][0] == self.column_3:
                self.value_2 = info[self.option - 1][i]
            column_info.append(no_2[i][0])

        print("可修改的字段有：", column_info)
        column_3 = input("请输入想要修改的字段：\n")
        value_3 = input("请输入想要修改的值：\n")

        sql = "UPDATE %s SET %s = %s WHERE %s = '%s' AND %s = '%s';" % (
            self.tab_name, column_3, value_3, self.column_1, self.value_1, self.column_3, self.value_2)
        print(sql)
        dbManager.edit(sql)


class COUManager(STUManager):  # 创建考题类，继承考生类
    def __init__(self, tab_name, column_1, call_1, call_2, column_2, column_3, value_1, value_2, value_3, option, sql):
        super().__init__(tab_name, column_1, call_1, call_2, column_2, column_3, value_1, value_2, value_3, option, sql)

    def judge(self):  # 判断使用哪个数据库
        option = input("请输入题型编号：\n")
        self.tab_name = '%s_que' % option
        print(self.tab_name)
        sql = "SELECT no_type from no_type WHERE no_type = %s" % option
        res = dbManager.fetchall(sql)
        if res is False:
            print("输入的题型编号有误!")
            return self.judge()

    def kno_info(self):  # 查询知识点信息
        self.tab_name, self.option = "no_course", '0'
        self.search_info()
        self.tab_name, self.option = "course_kno", '1'
        self.search_info()
        self.option = '2'
