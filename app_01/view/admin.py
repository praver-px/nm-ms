from django.shortcuts import render, redirect

from app_01 import models
from app_01.utils.pagination import Pagination
from app_01.utils.form import AdminModelForm

def admin_list(request):
    """ 管理员列表"""
    data_dict = {}

    search_data = request.GET.get('search_name', '')
    if search_data:
        data_dict['username__contains'] = search_data

    queryset = models.Admin.objects.filter(**data_dict)  # 查询条件
    page_obj = Pagination(request, queryset)  # 实例化类
    '''用户列表'''
    context = {
        'queryset': page_obj.query_set,
        'page_string': page_obj.html()
    }
    return render(request, 'admin_list.html', context)


def admin_add(request):
    """ 添加管理原"""
    title = '添加管理员'

    if request.method == "GET":
        form = AdminModelForm()
        return render(request, 'change.html', {'form': form, "title": title})

    form = AdminModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')
    return render(request, 'change.html', {'form': form, "title": title})
