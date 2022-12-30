import operateV2
import prepare
import ExamReport

if __name__ == '__main__':
    while 1:
        print("-------------题库与试卷生成系统-------------")
        option = input("请输入以下编号实现相应的功能：\n"
                       "1. 考生信息\n"
                       "2. 考题信息\n"
                       "3. 考前准备\n"
                       "4. 随机生成试卷\n"
                       "5. 批改试卷并导入成绩\n"
                       "6. 退出系统\n")

        if option == '1':
            print("-------------变更考生信息--------------")
            option_1 = input("请输入以下编号实现相应的功能：\n"
                             "1. 增加考生信息\n"
                             "2. 删除考生信息\n"
                             "3. 修改考生信息\n"
                             "4. 查询单个考生\n"
                             "5. 返回系统\n")

            opManager = operateV2.STUManager(tab_name='students', column_1='sname', call_1='姓名', call_2="",
                                             column_2='', column_3='course', value_1='', value_2='', value_3='', sql='',
                                             option='1')

            if option_1 == '1':
                print("增加考生信息")
                opManager.add_info()

            if option_1 == '2':
                print("删除考生信息")
                opManager.sub_info()

            if option_1 == '3':
                print("修改考生信息")
                opManager.edit_info()

            if option_1 == '4':
                print("获取单个考生信息")
                opManager.search_info()

            if option_1 == '5':
                print('重新返回系统')
                continue

        if option == '2':
            print("-------------变更考题信息--------------")
            option_2 = input("请输入以下编号实现相应的功能：\n"
                             "1. 增加考题信息\n"
                             "2. 删除考题信息\n"
                             "3. 修改考题信息\n"
                             "4. 获取单个考题信息\n"
                             "5. 查询知识点\n"
                             "6. 查询题型信息\n"
                             "7. 查询课程信息\n"
                             "8. 返回系统\n")

            opManager = operateV2.COUManager(tab_name='', column_1='no_course', call_1='课程编号', call_2="知识点编号",
                                             column_2='no_kno', column_3='no_que', value_1='', value_2='', value_3='',
                                             option='0', sql='1')

            if option_2 == '1':
                print("增加考题信息")
                ExamReport.type_info()
                opManager.judge()
                opManager.add_info()

            if option_2 == '2':
                print("删除考题信息")
                opManager.kno_info()
                ExamReport.type_info()
                opManager.judge()
                opManager.sub_info()

            if option_2 == '3':
                print("修改考题信息")
                opManager.kno_info()
                ExamReport.type_info()
                opManager.judge()
                opManager.edit_info()

            if option_2 == '4':
                print("获取单个考题信息")
                opManager.kno_info()
                ExamReport.type_info()
                opManager.judge()
                opManager.search_info()

            if option_2 == '5':
                print("获取知识点信息")
                print("查询知识点")
                opManager.kno_info()

            if option_2 == '6':
                print("查询题型信息")
                ExamReport.type_info()

            if option_2 == '7':
                print("查询课程信息")
                prepare.view_page()

            if option_2 == '8':
                print('重新返回系统')
                continue

        if option == '3':
            print("-------------考前准备--------------")
            option_3 = input("请输入以下编号实现相应的功能：\n"
                             "1. 创建班级\n"
                             "2. 导入考试科目\n"
                             "3. 创建题库视图\n"
                             "4. 返回系统\n")

            if option_3 == '1':
                print("创建班级")
                prepare.create_class()

            if option_3 == '2':
                print("导入考试科目")
                prepare.export_course()

            if option_3 == '3':
                print("创建题库视图")
                prepare.create_view()

            if option_3 == '4':
                print("重新返回系统")
                continue

        if option == '4':
            print("--------------试卷生成-----------------")
            option_4 = input("1. 制订试卷标准\n"
                             "2. 随机生成试卷\n"
                             "3. 返回系统\n")

            if option_4 == '1':
                print("制定试卷标准")
                ExamReport.make_standard()

            if option_4 == '2':
                print("随机生成试卷")
                ExamReport.export_report()

            if option_4 == '3':
                print('重新返回系统')
                continue

        if option == '5':
            print("批改试卷并导入成绩")

        if option == '6':
            print("程序已退出")
            break

        else:
            print("重新输入编号")
