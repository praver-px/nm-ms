from django.shortcuts import render

from app_01 import models
from app_01.utils.pagination import Pagination


def admin_list(request):
    """ 管理员列表"""
    data_dict = {}
    queryset = models.Admin.objects.filter(**data_dict) # 查询条件
    page_obj = Pagination(request, queryset)  # 实例化类
    '''用户列表'''
    context = {
        'queryset': page_obj.query_set,
        'page_string': page_obj.html()
    }
    return render(request, 'admin_list.html', context)
