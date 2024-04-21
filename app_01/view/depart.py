from django.shortcuts import render, redirect

from app_01 import models


# Create your views here.

def depart_list(request):
    '''部门列表'''
    queryset = models.Department.objects.all()
    return render(request, 'depart_list.html', {'queryset': queryset})


def depart_add(request):
    '''添加部门'''
    if request.method == 'GET':
        return render(request, 'depart_add.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)
    return redirect('/depart/list/')


def depart_delete(request, id):
    '''删除部门'''
    models.Department.objects.filter(id=id).delete()
    return redirect('/depart/list/')


def depart_edit(request, id):
    '''编辑部门'''
    if request.method == 'GET':
        depart = models.Department.objects.filter(id=id).first()
        return render(request, 'depart_edit.html', {'depart': depart})
    title = request.POST.get('title')
    models.Department.objects.filter(id=id).update(title=title)
    return redirect('/depart/list/')
