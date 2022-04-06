import django.http
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
import time
import json
from index import models
from django.contrib.auth.decorators import login_required

@login_required
@xframe_options_exempt
def courses(request):
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
    allCourses = models.courseName.objects.all()

    # 分组讨论 专题辅导  自学  影视教学  经验交流  结构化研讨  团队建设  现场教学 体验教学  示范课  案例教学
    fztl = 0  # 分组讨论
    ztfd = 0  # 专题辅导
    zx =  0  # 自学
    ysjx = 0  # 影视教学
    jyjl = 0  # 经验交流
    jghyt = 0  # 结构化研讨
    tdjs = 0  # 团队建设
    xcjx = 0  # 现场教学
    tyjx = 0  # 体验教学
    sfk = 0  # 示范课
    aljx = 0  # 案例教学
    lxNum = [0] * 11

    # 获取所有类型的课程
    for one in allCourses:
        if one.courseType == "分组讨论":
            lxNum[0] += 1
        elif one.courseType == "专题辅导":
            lxNum[1] += 1
        elif one.courseType == "自学":
            lxNum[2] += 1
        elif one.courseType == "影视教学":
            lxNum[3] += 1
        elif one.courseType == "经验交流":
            lxNum[4] += 1
        elif one.courseType == "结构化研讨":
            lxNum[5] += 1
        elif one.courseType == "团队建设":
            lxNum[6] += 1
        elif one.courseType == "现场教学":
            lxNum[7] += 1
        elif one.courseType == "体验教学":
            lxNum[8] += 1
        elif one.courseType == "示范课":
            lxNum[9] += 1
        elif one.courseType == "案例教学":
            lxNum[10] += 1


    # 课程模块的字段
    # 党的理论、党史学习、党性教育  共同体意识及民族类  知识素养  专业化能力  脱贫攻坚乡村振兴
    dxjy = 0  # 党的理论、党史学习、党性教育
    dxjyScore = 0  # 党性教育得分
    dxjyEffectiveNum = 0  # 党性教育有效分数的个数
    mzgtt = 0  # 共同体意识及民族类
    mzgttScore = 0  # 共同体意识得分
    mzgttEffectiveNum = 0  # 共同体意识有效分数的个数
    zssy = 0  # 知识素养
    zssyScore = 0  # 知识素养得分
    zssyEffectiveNum = 0  # 知识素养有效分数的个数
    zyhnl = 0  # 专业化能力
    zyhnlScore = 0  # 专业化能力得分
    zyhnEffectiveNum = 0  # 专业化能力有效分数的个数
    xczx = 0  # 脱贫攻坚乡村振兴
    xczxScore = 0  # 脱贫攻坚乡村振兴得分
    xczxEffectiveNum = 0  # 乡村振兴有效分数的个数
    mkNum = [0.0] * 5
    # 获取所有课程的模块
    for one in allCourses:
        if one.courseModule == "党的理论、党史学习、党性教育":
            dxjy += 1
            if float(one.courseScore) > 0:
                dxjyEffectiveNum += 1
                dxjyScore += one.courseScore
        elif one.courseModule == "铸牢中华民族共同体意识":
            mzgtt += 1
            if float(one.courseScore) > 0:
                mzgttEffectiveNum += 1
                mzgttScore += one.courseScore
        elif one.courseModule == "知识素养":
            zssy += 1
            if float(one.courseScore) > 0:
                zssyEffectiveNum += 1
                zssyScore += one.courseScore
        elif one.courseModule == "专业化能力":
            zyhnl += 1
            if float(one.courseScore) > 0:
                zyhnEffectiveNum += 1
                zyhnlScore += one.courseScore
        elif one.courseModule == "脱贫攻坚乡村振兴":
            xczx += 1
            if float(one.courseScore) > 0:
                xczxEffectiveNum += 1
                xczxScore += one.courseScore

    # 各模块平均分
    moduleAverage = [0.0] * 5
    moduleAverage[0] = round(float(dxjyScore / dxjyEffectiveNum), 2)  # 党性教育平均分
    moduleAverage[1] = round(float(mzgttScore / mzgttEffectiveNum), 2)  # 铸牢中华民族共同体意识平均分
    moduleAverage[2] = round(float(zssyScore / zssyEffectiveNum), 2)  # 知识素养平均分
    moduleAverage[3] = round(float(zyhnlScore / zyhnEffectiveNum), 2)   # 专业化能力平均分
    moduleAverage[4] = round(float(xczxScore / xczxEffectiveNum), 2)  # 脱贫攻坚乡村振兴平均分

    # 课专题评议得分
    # 最高分  最低分  平均分
    totalScore = 0  # 总分
    effectiveList = []  # 有效得分的数组
    scoreList = [0.0] * 3
    for one in allCourses:
        if one.courseScore != 0:
            effectiveList.append(one.courseScore)
            totalScore += one.courseScore
    print(effectiveList)
    print(len(effectiveList))
    scoreList[2] = max(effectiveList)  # 最高分
    scoreList[1] = min(effectiveList)  # 最低分
    scoreList[0] = float(totalScore/len(effectiveList))  # 评价分
    scoreList[0] = round(scoreList[0], 2)  # 评价分保留2位小数
    print('最高分：', scoreList[2])
    print('最低分：', scoreList[1])
    print('平均分：', scoreList[0])

    # 各模块平均分


    return render(request, 'allCourse.html', locals())
