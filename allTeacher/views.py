import django.http
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
import time
import json
from index import models
from django.contrib.auth.decorators import login_required

@login_required
@xframe_options_exempt
def teachers(request):
    print('我是teachersShow页面')

    # 获取顶部的四个数据开始
    allClasses= models.courseCategoryModel.objects.all()  # 获取所有的培训班信息
    allTeachers = models.teacherModel.objects.all()  # 获取所有教师的信息
    teachersNum = allTeachers.count()  # 教师的人数
    classesNum = allClasses.count()  # 培训班数量
    peopleNum = 0  # 总的培训人次
    dayNum = 0  # 总的培训天数
    for one in allClasses:
        peopleNum = peopleNum + int(one.c_people)
        dayNum = dayNum + float(one.c_cycle)
    # 获取顶部的四个数据结束

    # 读取所有的字段数据，使用values_list可以读取期中的一个字段组成列表
    allTeachersInfo = models.teacherModel.objects.all()
    tEducation = [0] * 6
    tLevelJs = 0
    tLevelFjs = 0
    tLevelZjjs = 0
    tLevelZj = 0
    tLevelYjy = 0
    tLevelFyjy = 0
    tLevelZlyjy = 0
    tLevelYjsxy = 0
    tLevelQt = 0
    tSexM = 0
    tSexF = 0
    tTitle = [0] * 9
    tFrom = [0] * 6
    tProvince_sn = 0
    tProvince_sw = 0
    for one in allTeachersInfo:
        # 计算学历的个数
        if one.t_education == '博士研究生':
            tEducation[0] += 1
        elif one.t_education == '硕士研究生':
            tEducation[1] += 1
        elif one.t_education == '本科':
            tEducation[2] += 1
        elif one.t_education == '大专':
            tEducation[3] += 1
        elif one.t_education == '专科':
            tEducation[4] += 1
        else:
            tEducation[5] += 1

        # 计算职称的个数
        if one.t_level == '教授':
            tLevelJs = tLevelJs + 1
            name_tLevelJs = '教授 ' + str(tLevelJs) + '人'
        elif one.t_level == '副教授':
            tLevelFjs = tLevelFjs + 1
            name_tLevelFjs = '副教授 ' + str(tLevelFjs) + '人'
        elif one.t_level == '讲师':
            tLevelZjjs = tLevelZjjs + 1
            name_tLevelZjjs = '讲师 ' + str(tLevelZjjs) + '人'
        elif one.t_level == '助教':
            tLevelZj = tLevelZj + 1
            name_tLevelZj = '助教 ' + str(tLevelZj) + '人'
        elif one.t_level == '研究员':
            tLevelYjy = tLevelYjy + 1
            name_tLevelYjy = '研究员 ' + str(tLevelYjy) + '人'
        elif one.t_level == '副研究员':
            tLevelFyjy = tLevelFyjy + 1
            name_tLevelFyjy = '副研究员 ' + str(tLevelFyjy) + '人'
        elif one.t_level == '助理研究员':
            tLevelZlyjy = tLevelZlyjy + 1
            name_tLevelZlyjy = '助理研究员 ' + str(tLevelZlyjy) + '人'
        elif one.t_level == '研究实习员':
            tLevelYjsxy = tLevelYjsxy + 1
            name_tLevelYjsxy = '研究实习员 ' + str(tLevelYjsxy) + '人'
        else:
            tLevelQt = tLevelQt + 1
            name_tLevelQt = '其他 ' + str(tLevelQt) + '人'

        # 计算男女的个数
        if one.t_sex == '男':
            tSexM = tSexM + 1
            name_tSexM = '男 ' + '(' + str(tSexM) + '人)'
        else:
            tSexF = tSexF + 1
            name_tSexF = '女 ' + '(' + str(tSexF) + '人)'

        # 计算职级的个数
        print(tTitle[1])
        if one.t_title == '省部级':
            tTitle[0] += 1
        elif one.t_title == '正厅':
            tTitle[1] += 1
        elif one.t_title == '副厅':
            tTitle[2] += 1
        elif one.t_title == '正处':
            tTitle[3] += 1
        elif one.t_title == '副处':
            tTitle[4] += 1
        elif one.t_title == '正科':
            tTitle[5] += 1
        elif one.t_title == '副科':
            tTitle[6] += 1
        elif one.t_title == '科员':
            tTitle[7] += 1
        else:
            tTitle[8] += 1

        # 计算行业的个数
        if one.t_from == '政府机关':
            tFrom[1] += 1
        elif one.t_from == '党校':
            tFrom[2] += 1
        elif one.t_from == '高校':
            tFrom[3] += 1
        elif one.t_from == '企业':
            tFrom[4] += 1
        else:
            tFrom[5] += 1

        # 计算省内外的个数
        if one.t_province == '省内':
            tProvince_sn += 1
        else:
            tProvince_sw += 1

    tFrom[0] = tFrom[1] + tFrom[2] + tFrom[3] + tFrom[4] + tFrom[5]
    # ztbcPeople = ztbcPeople + int(float(i.c_people))

    return render(request, 'allTeacher.html', locals())
