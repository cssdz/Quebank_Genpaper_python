import mysql_op
import random
import doc
import os

dbManager = mysql_op.DBManager()
sel_sql = "SELECT %s FROM %s;"


def type_info():  # 查询题型信息
    sql_1, sql_2 = '*', 'no_type'
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    print("可供选择的题型有： ")
    for i in range(len(info)):
        print("题型编号：%s" % info[i][0], " 题型名称：%s" % info[i][1])


def make_standard():  # 制定标准
    no_course = int(input("输入出卷的课程编号："))  # 查询题型信息
    type_info()

    print("------------------制定出题标准--------------------")
    print("输入：“[题型编号,题型分值,题型数量]”，d：删除上一条数据，q：退出")
    standard, single, combine = [], [], ""
    while 1:
        info = input()
        if info == 'q':
            break
        if info == 'd':
            try:
                standard.pop()
            except IndexError:
                print("制定标准里暂无数据")
                continue
        else:
            for i in info:
                if i == ',':
                    single.append(int(combine))
                    combine = ''
                else:
                    combine += i
            single.append(int(combine))
            standard.append(single)
            single, combine = [], ""
        print(standard)

    max_score = 0
    for i in range(len(standard)):
        max_score += standard[i][1] * standard[i][2]
    print(f"试卷满分为：{max_score}分")

    table_name = "%s_standard" % no_course  # 创建课程-考试标准表
    sql = "CREATE TABLE IF NOT EXISTS `%s` (no_type INT(3), type_value INT(2), amount INT(3));" % table_name
    dbManager.execute(sql)
    print(f"【数据库操作】创建{table_name}表")
    for i in range(len(standard)):
        no_type, type_value, amount = standard[i]
        sql_1, sql_2 = "*", "39_standard where no_type = %s" % no_type
        sql = sel_sql % (sql_1, sql_2)
        res = dbManager.fetchall(sql)
        if res is False:
            sql = "INSERT INTO `%s` (no_type, type_value, amount) VALUES (%s, %s, %s)" % (
                table_name, no_type, type_value, amount)
            dbManager.edit(sql)
        else:
            print("数据重复")


def gen_exam(no_course):  # 随机生成试卷
    sql_1, sql_2 = "COUNT(*)", "course_kno WHERE no_course = '%s'" % no_course  # 获取知识点数量
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    if info is False:
        print("数据库缺少该数据")
        return gen_exam(no_course)
    kno_count = info[0][0]
    # print(kno_count)

    table_name = "%s_standard" % no_course  # 获取考试标准
    sql_1, sql_2 = "*", "%s" % table_name
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    ran_count = len(info)

    que, ans = [], []
    for i in range(ran_count):  # 打乱知识点抽取顺序
        kno_info = []
        for j in range(kno_count):
            kno_info.append(random.randint(1, kno_count))

        view_name, table_name = "%s_%s_que" % (no_course, info[i][0]), "%s_que" % info[i][0]  # 获取题目信息
        sql_1, sql_2 = "column_name", "information_schema.columns WHERE table_name = '%s'" % table_name
        sql = sel_sql % (sql_1, sql_2)
        column_info = dbManager.fetchall(sql)
        # print(column_info)

        columns, str_columns = [], ""  # 筛选题目信息
        for j in range(len(column_info)):
            if column_info[j][0] == 'que':
                columns = list()
            if column_info[j][0] == 'diff':
                columns.pop()
            columns.append(column_info[j][0])

        count, no = len(columns), 0
        for j in columns:
            str_columns += j
            if no < count - 1:
                str_columns += ", "
            no += 1

        no_type, type_value, amount = info[i]  # 随机生成考题
        status, que_single, table_name = 1, [], "%s_que" % (i + 1)
        if amount >= kno_count:
            pub, pri, no = int(amount / kno_count), amount % kno_count, 0
            for j in range(kno_count):
                no += 1
                if no == pri + 1:
                    status = 0
                sql_1, sql_2 = str_columns, "%s WHERE no_kno = %s ORDER BY RAND() LIMIT %s" % (
                    table_name, kno_info[j], pub + status)
                sql = sel_sql % (sql_1, sql_2)
                # print(sql)
                que_info = dbManager.fetchall(sql)
                for k in que_info:
                    ans.append(list(k[-1:]))
                    # print(que_single_)
                    que_single.append(list(k[:-1]))

        else:
            for j in range(amount):
                sql_1, sql_2 = str_columns, "%s WHERE no_kno = %s ORDER BY RAND() LIMIT 1" % (
                    table_name, kno_info[j])
                sql = sel_sql % (sql_1, sql_2)
                que_info = dbManager.fetchall(sql)
                for k in que_info:
                    ans.append(list(k[-1:]))
                    # print(que_single_)
                    que_single.append(list(k[:-1]))

            # print(que_single)

        que.append(sorted(que_single, key=(lambda x: x[-1])))
    return que, ans


def export_report():
    no_course = input("输入课程编号：")
    sql_1, sql_2 = "course", "no_course WHERE no_course = %s" % no_course
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    course = info[0][0]

    sql_1, sql_2 = "DISTINCT class", "students WHERE course = '%s'" % course
    sql = sel_sql % (sql_1, sql_2)
    info = dbManager.fetchall(sql)
    print(info)

    for i in range(len(info)):
        class_info = info[i][0]
        sql_1, sql_2 = "sno, dept, sname, semester", "students WHERE course = '%s' AND class = '%s'" % (
            course, class_info)
        sql = sel_sql % (sql_1, sql_2)
        stu_info = dbManager.fetchall(sql)
        # print(stu_info)

        for j in range(len(stu_info)):
            sno, dept, sname, semester = stu_info[j]
            table_name = "%s_%s_%s" % (no_course, class_info, sno)
            sql = "CREATE TABLE IF NOT EXISTS `%s` (stu_ans VARCHAR(255), stand_ans VARCHAR(255));" % table_name
            dbManager.execute(sql)
            que, ans = gen_exam(no_course)

            for k in ans:
                for stand_ans in k:
                    sql = "INSERT INTO %s (stand_ans) VALUES ('%s')" % (table_name, stand_ans)
                    dbManager.edit(sql)

            # print(sno, dept, sname, semester)
            path_info = path(course, dept, class_info)

            report_name = "\\%s_%s_%s.docx" % (no_course, class_info, sno)
            create_paper = doc.CreatePaper(semester=semester, dept=dept, course=course, class_=class_info,
                                           s_name=sname, s_no=sno, report_name=report_name, que=que, path=path_info)
            create_paper.combine_file()


def path(course, dept, class_info):
    path_info = r".\试卷\%s\%s\%s" % (course, dept, class_info)
    # print(path_info)
    if os.path.isdir(path_info) is False:
        os.makedirs(path_info)
    return path_info

