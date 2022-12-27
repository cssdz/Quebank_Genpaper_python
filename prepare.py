import mysql_op

dbManager = mysql_op.DBManager()
sel_sql = "SELECT %s FROM %s;"


def view_page():    # 查询课程信息
    sql_ = "SELECT * FROM no_course order by no_course ASC limit %s,10"
    current_page_no = 1

    while True:
        sql = sql_ % ((current_page_no - 1) * 10)
        result = dbManager.fetchall(sql)

        if result is False:
            current_page_no -= 1
            print(f"{current_page_no}页已达最大值")
        else:
            for info in result:
                print("课程编号：%s" % info[0], "    课程名称：%s" % info[1])
            print(f"第{current_page_no}页")
        status = input("（1：上一页，2：下一页，q：退出）:")

        if status == 'q':
            return

        elif status == '1':
            if current_page_no > 1:
                current_page_no -= 1
            else:
                current_page_no = 1

        elif status == '2':
            current_page_no += 1

        else:
            print("请输入正确的代码。")
            continue


def create_class():     # 创建课程-班级表
    view_page()

    course = input("输入考试的课程名称：")  # 获取考试该课程的班级
    class_info = []
    sql_1, sql_2 = "DISTINCT class", "students WHERE course = '%s'" % course
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    try:
        for i in info:
            class_info.append(i[0])
    except TypeError:
        print("输入的课程有误！")
        return create_class()
    print(class_info)

    for i in range(len(class_info)):  # 创建考试班级
        table_name = course + "-" + class_info[i]
        sql = "CREATE TABLE IF NOT EXISTS `%s` " \
              "(`sno` INT(10) PRIMARY KEY, `sname` varchar(20), `score` float, `rank` int(2));" % table_name
        print(sql)
        res = dbManager.execute(sql)
        if res is False:
            exit()

        # 筛选班级学生
        sql_1, sql_2 = "Distinct sname, sno", "students where class = '%s' AND course = '%s'" % (info[i][0], course)
        sql = sel_sql % (sql_1, sql_2)
        # print(sql)
        stu_name = dbManager.fetchall(sql)
        # print(stu_name)

        for j in range(len(stu_name)):  # 导入学生
            name, no = stu_name[j][0], stu_name[j][1]
            print(name, no)
            sql = "INSERT INTO `%s` (sno, sname) values (%s, '%s') ON DUPLICATE KEY UPDATE sname='%s';" % (
                table_name, no, name, name)
            dbManager.edit(sql)


def export_course():    # 导入课程信息
    sql_1, sql_2 = 'no_course', 'no_course ORDER BY no_course DESC LIMIT 1'
    sql = sel_sql % (sql_1, sql_2)
    no_max = dbManager.fetchall(sql)
    if no_max is False:
        no_max = 0
    else:
        no_max = no_max[0][0]

    sql_1, sql_2 = 'DISTINCT course', 'students'
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    # print(info)

    for i in range(len(info)):
        no_max += 1
        course = info[i][0]

        sql_1, sql_2 = 'course', "no_course WHERE course = '%s'" % course
        sql = sel_sql % (sql_1, sql_2)
        res = dbManager.fetchall(sql)
        # print(res)

        if res is False:
            sql = "INSERT INTO `no_course` (no_course, course) values (%s, '%s') " % (no_max, course)
            dbManager.edit(sql)

        else:
            print("数据重复")

        print("导入完毕")


def create_view():  # 创建课程-题库视图
    no_course = input("输入课程编号：")

    sql_1, sql_2 = "no_type", "no_type"
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    for i in range(len(info)):
        view_name, table_name = "%s_%s_que" % (no_course, info[i][0]), "%s_que" % info[i][0]
        sql_1, sql_2 = "column_name", "information_schema.columns WHERE table_name = '%s'" % table_name
        sql = sel_sql % (sql_1, sql_2)
        column_info = dbManager.fetchall(sql)
        # print(column_info)

        columns, str_columns = [], ""
        for j in range(len(column_info)):
            columns.append(column_info[j][0])
            if column_info[j][0] == 'que':
                columns = list()
                columns.append(column_info[j][0])

        count, no = len(columns), 0
        for j in columns:
            str_columns += j
            if no < count - 1:
                str_columns += ", "
            no += 1
        print(str_columns)

        sql_1, sql_2 = str_columns, table_name
        sel = sel_sql % (sql_1, sql_2)
        sql = "CREATE VIEW `%s` AS %s" % (view_name, sel)
        res = dbManager.execute(sql)
        if res is not False:
            print("【数据库操作】视图创建成功")
        else:
            print("【数据库操作】视图创建失败")

# create_view()
