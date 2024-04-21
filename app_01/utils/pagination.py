"""
分页

使用跳转无法保留请求参数

def func(request):
    queryset = models.PrettyNum.objects.filter(**data_dict).order_by('-level') # 查询条件
    page_obj = Pagination(request, queryset) # 实例化类

    context = {
        'queryset': page_obj.query_set,
        'page_string': page_obj.html()
    }
    return render(request, 'func.html', context)


     <ul class="pagination">
                {{ page_string }}
     </ul>
"""
from django.utils.safestring import mark_safe


class Pagination(object):

    def __init__(self, request, query_set, page_size=10, page_param='page', step=5):
        """

        :param request: 请求对象
        :param query_set: 查询的数据
        :param page_size: 条数
        :param page_param: 获取分页的参数
        :param step: 显示当前页前后页数
        """

        # 获取请求参数
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict

        page = request.GET.get(page_param, "1")
        # 将 page 转换为整数
        try:
            page = int(page)
        except ValueError:
            page = 1  # 如果转换失败，使用默认值 1

        self.page = page

        self.page_size = page_size
        self.page_param = page_param

        self.start = (self.page - 1) * page_size
        self.end = page * page_size
        self.query_set = query_set[self.start:self.end]
        total_count = query_set.count()
        total_page_count, div = divmod(total_count, page_size)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.step = step

    def html(self):
        if self.total_page_count <= 2 * self.step + 1:
            start_page = 1
            end_page = self.total_page_count + 1
        else:
            if self.page <= self.step + 1:
                start_page = 1
                end_page = 2 * self.step + 1
            else:
                if self.page + self.step > self.total_page_count:
                    start_page = self.total_page_count - 2 * self.step
                    end_page = self.total_page_count + 1
                else:
                    start_page = self.page - self.step
                    end_page = self.page + self.step + 1

        page_str_list = []

        self.query_dict.setlist(self.page_param, [1])
        first_page = '<li><a href="?{}">首页</a></li> \n'.format(self.query_dict.urlencode())
        page_str_list.append(first_page)
        if self.page == 1:
            prev = '<li><a href="?{}">&laquo;</a></li> \n'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page - 1])
            prev = '<li><a href="?{}">&laquo;</a></li> \n'.format(self.query_dict.urlencode())
        page_str_list.append(prev)
        for i in range(start_page, end_page):
            self.query_dict.setlist(self.page_param, [i])
            if i == self.page:
                ele = '<li class="active"><a href="?{}">{}</a></li> \n'.format(self.query_dict.urlencode(), i)
            else:
                ele = '<li><a href="?{}">{}</a></li> \n'.format(self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        if self.page == self.total_page_count:
            self.query_dict.setlist(self.page_param, [self.total_page_count])
            next = '<li><a href="?{}">&raquo;</a></li> \n'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            next = '<li><a href="?{}">&raquo;</a></li> \n'.format(self.query_dict.urlencode())
        page_str_list.append(next)
        self.query_dict.setlist(self.page_param, [self.total_page_count])
        last_page = '<li><a href="?{}">尾页</a></li> \n'.format(self.query_dict.urlencode())
        page_str_list.append(last_page)

        page_search = """
            <li>
               <form method="get" style="float: left;margin-left: 20px">
                   <div class="input-group" style="width: 100px;">
                       <input type="text" class="form-control" placeholder="页码" name="page"/>
                       <span class="input-group-btn">
                      <button type="submit" class="btn btn-default">
                          <span class="glyphicon glyphicon-arrow-right" aria-hidden="true"></span>
                      </button>
                   </span>
                   </div>
               </form>
           </li>
           """
        page_str_list.append(page_search)

        return mark_safe(''.join(page_str_list))
