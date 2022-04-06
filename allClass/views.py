import django.http
from django.shortcuts import render
from django.views.decorators.clickjacking import xframe_options_exempt
import time
import json
from index import models
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
@xframe_options_exempt
def courses(request):
    if request.method == 'POST':
        print(request.POST['screenYear'])
    print('我是allCourses页面')
    # 读取所有的字段数据，使用values_list可以读取期中的一个字段组成列表

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

    allCourses = models.courseCategoryModel.objects.all()
    ztbc = models.courseCategoryModel.objects.filter(c_category='主体班次')
    ztbcNum = len(ztbc)
    sjxx = models.courseCategoryModel.objects.filter(c_category='送教下乡')
    sjxxNum = len(sjxx)
    gnwtbc = models.courseCategoryModel.objects.filter(c_category='国内委托班次')
    gnwtbcNum = len(gnwtbc)
    gwwtbc = models.courseCategoryModel.objects.filter(c_category='国外委托班次')
    gwwtbcNum = len(gwwtbc)
    jhnbcNum = ztbcNum + sjxxNum
    jhwbcNum = gwwtbcNum + gnwtbcNum
    nowYear = list(time.localtime())[0]  # 当前的年份
    addYears = 2014  # 学院起始于2014年
    everyYear = []  # 这是用来装是哪年，例如2014年、2015年......
    yearNumList = []  # 这个是用来装各年培训班期数的数组
    oneYearNum = []  # 这个用来存每年的人数
    perNum = 0
    allNum = 0
    for years in range(2014, nowYear + 1):
        filterYear = str(years) + '年'
        print(filterYear)
        everyYear.append(years)
        numyear = models.courseCategoryModel.objects.filter(c_year=filterYear)
        # 添加每年的总人数
        for i in numyear:
            perNum = int(float(i.c_people)) + perNum
            allNum = int(float(i.c_people)) + allNum
        yearNumList.append(len(numyear))
        oneYearNum.append(perNum)
        perNum = 0
        addYears = addYears + 1
        # 某年各月的培训人数
        theYearNum = str(nowYear) + '年'
        monthNum = [0] * 12
        if filterYear == theYearNum:
            for k in range(0, 12):
                monthNum[k] = 0
                for j in numyear:
                    if int(float(j.c_month)) == k + 1:
                        monthNum[k] = monthNum[k] + int(float(j.c_people))
    oneYearNum.append(allNum)

    # 获取各类培训班的人数
    ztbcPeople = 0
    sjxxPeople = 0
    gnwtbcPeople = 0
    gwwtbcPeople = 0
    for i in ztbc:
        ztbcPeople = ztbcPeople + int(float(i.c_people))
    for i in sjxx:
        sjxxPeople = sjxxPeople + int(float(i.c_people))
    for i in gnwtbc:
        gnwtbcPeople = gnwtbcPeople + int(float(i.c_people))
    for i in gwwtbc:
        gwwtbcPeople = gwwtbcPeople + int(float(i.c_people))
    allPeople = ztbcPeople + sjxxPeople + gnwtbcPeople + gwwtbcPeople

    print(yearNumList)
    print(everyYear)
    print(oneYearNum)
    print(monthNum)

    return render(request, 'allClass.html', locals())


@xframe_options_exempt
def oneYearInfo(request):
    print(request.POST['year'])
    numyear = models.courseCategoryModel.objects.filter(c_year=request.POST['year'])
    # 添加每年的总人数
    monthNum = [0] * 12
    # 传递数据初始化为字典
    backInfo = {'peopleNum': '', 'optionText': ''}
    # 某年各月的培训人数
    for k in range(0, 12):
        monthNum[k] = 0
        for j in numyear:
            if int(float(j.c_month)) == k + 1:
                monthNum[k] = monthNum[k] + int(float(j.c_people))
    print(monthNum)
    backInfo['peopleNum'] = monthNum
    backInfo['optionText'] = request.POST['year'] + '度各月份培训班人数情况'
    return django.http.HttpResponse(json.dumps(backInfo))  # 回传的时候要编成json格式，要不然全是字符串
