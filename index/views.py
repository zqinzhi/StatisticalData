from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from index import models
from django.http import HttpResponse
# Create your views here.


@login_required
def index(request):
    print('I am index.html!')
    print(request.user)
    allClasses= models.courseCategoryModel.objects.all()  # 获取所有的培训班信息
    allTeachers = models.teacherModel.objects.all()  # 获取所有教师的信息
    teachersNum = allTeachers.count()  # 教师的人数
    classesNum = allClasses.count()  # 培训班数量
    peopleNum = 0  # 总的培训人次
    dayNum = 0  # 总的培训天数
    ztbc = 0  # 主体班次的数量
    sjxx = 0  # 送教下乡的数量
    gnwtb = 0  # 国内委托班次的数量
    gwwtb = 0  # 国内委托班次的数量
    for one in allClasses:
        peopleNum = peopleNum + int(one.c_people)
        dayNum = dayNum + float(one.c_cycle)
        if one.c_category == "主体班次":
            ztbc += 1
        elif one.c_category == "送教下乡":
            sjxx += 1
        elif one.c_category == "国内委托班次":
            gnwtb += 1
        else:
            gwwtb += 1
    ztbcLabel = '主体班次' + str(ztbc) + '期'
    sjxxLabel = '送教下乡' + str(sjxx) + '期'
    gnwtbLabel = '国内委托班次' + str(gnwtb) + '期'
    gwwtbLabel = '国外委托班次' + str(gwwtb) + '期'
    return render(request, "index.html", locals())


@login_required
def logout_view(request):
    #清除session，登出
    print('我退出了')
    auth.logout(request)
    return redirect("/user/login.html")
