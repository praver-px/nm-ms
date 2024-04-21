from django.shortcuts import render, redirect

from app_01 import models
from app_01.utils.form import PrettynumModelForm, PrettynumEditModelForm


def prettynum_list(request):
    '''

    models.PrettyNum.objects.filter(mobile='13944445555', id=1)
    data_dict = {'mobile': '13944445555', 'id': 1}
    models.PrettyNum.objects.filter(**data_dict)

    # 数值比较
    models.PrettyNum.objects.filter(id=2)  # 获取id为2的数据
    models.PrettyNum.objects.filter(id__gt=2)  # id大于2的数据 gte 大于等于
    models.PrettyNum.objects.filter(id__lt=2)  # id小于2的数据 lte 小于等于

    # 模糊查询
    models.PrettyNum.objects.filter(mobile__startswith='1')  # 以1开头
    models.PrettyNum.objects.filter(mobile__contains='1')  # 包含1
    models.PrettyNum.objects.filter(mobile__endswith='1')  # 以1结尾
    '''
    # 给数据库插入数据
    # for i in range(100):
    #     first_digit = '1'
    #     remaining_digits = f"{random.randint(0, 9999999999):010d}"
    #     random_number = first_digit + remaining_digits
    #     models.PrettyNum.objects.create(
    #         mobile=random_number + '',
    #         price=10 + i,
    #         level=int(random.randint(1, 4)),
    #         status=int(random.randint(1, 2)),
    #     )

    data_dict = {}
    mobile_end = request.GET.get('mobile_end', '')

    if mobile_end:
        data_dict["mobile__endswith"] = mobile_end

    # 分页
    from app_01.utils.pagination import Pagination
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level')
    page_obj = Pagination(request, queryset)

    context = {
        'queryset': page_obj.query_set,
        'mobile_end': mobile_end,
        'page_string': page_obj.html()
    }
    return render(request, 'prettynum_list.html', context)


def prettynum_add(request):
    if request.method == 'GET':
        form = PrettynumModelForm()
        return render(request, 'prettynum_add.html', {'form': form})

    form = PrettynumModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    else:
        print(form.errors)
        return render(request, 'prettynum_add.html', {'form': form})


def prettynum_edit(request, id):
    instance = models.PrettyNum.objects.filter(id=id).first()
    if request.method == 'GET':
        form = PrettynumEditModelForm(instance=instance)
        return render(request, 'prettynum_edit.html', {'form': form})

    form = PrettynumEditModelForm(data=request.POST, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('/prettynum/list/')
    else:
        print(form.errors)
        return render(request, 'prettynum_edit.html', {'form': form})


def prettynum_delete(request, id):
    models.PrettyNum.objects.filter(id=id).delete()
    return redirect('/prettynum/list/')
