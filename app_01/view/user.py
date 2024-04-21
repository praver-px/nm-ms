from django.shortcuts import render, redirect

from app_01 import models
from app_01.utils.form import UserModelForm


def user_list(request):
    '''用户列表'''
    queryset = models.UserInfo.objects.all()
    '''
    for obj in queryset:
        obj.create_time.strftime('%Y-%m-%d')  # 格式化时间 
        obj.get_gender_display()  # 获取性别 格式 get_字段名_display
        obj.depart.title  # 获取部门 
    '''
    return render(request, 'user_list.html', {'queryset': queryset})


def user_add(request):
    context = {
        'gender_choices': models.UserInfo.gender_choices,
        'depart_list': models.Department.objects.all()
    }

    return render(request, 'user_add.html', context)


def user_create(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_create.html', {'form': form})

    # 用户post提交数据，对数据进行验证
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        form.save()
        return redirect('/user/list/')
    else:
        print(form.errors)
        return render(request, 'user_create.html', {'form': form})


def user_edit(request, id):
    instance = models.UserInfo.objects.filter(id=id).first()

    if request.method == 'GET':
        form = UserModelForm(instance=instance)
        print(form.initial)
        return render(request, 'user_edit.html', {'form': form})

    form = UserModelForm(data=request.POST, instance=instance)
    if form.is_valid():
        # form.instance.[字段名] =  [值] 用户输入后再新添加数据
        form.save()
        return redirect('/user/list/')
    return render(request, 'user_edit.html', {'form': form})


def user_delete(request, id):
    models.UserInfo.objects.filter(id=id).delete()
    return redirect('/user/list/')
