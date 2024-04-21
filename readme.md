# 开始

## 创建项目

- 使用pycharm创建项目
- 选择创建虚拟环境
- 创建项目
- 创建项目后进入[项目包名]setting中修改 `TEMPLATES` 中的`DIRS`信息置空，同时删除项目文件 `templates`

## 创建app

- 菜单栏`tools` -> `run manage.py task ...`
- 再打开的命令窗口中输入`startapp [app名]`
- 将创建的app在`setting`中进行注册，`INSTALLED_APPS` 中添加 `[app名].apps.[app名]Config`

## 设计表结构

- 在[app名]`models.py`中设计表结构(具体见文件)
- 在数据库中创建数据库

```mysql
create database [数据库名] default charset utf8 collate utf8_general_ci;
```

- 在setting中配置好数据库信息

```python
# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nm_ms',
        'USER': '用户名',
        'PASSWORD': '密码',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```

- 安装`pip install mysqlclient`
- 运行`python manage.py makemigrations`生成迁移文件
- 运行`python manage.py migrate`将迁移文件同步到数据库

## 静态文件管理

- 创建静态文件目录`static`
- 配置模板文件`templates`

## 部门管理

- 在`urls.py`中引入`from [app名] import views` 配置路由
- 在`views.py`中编写视图函数 `def [视图函数名](request):`
- 在`templates`中编写模板文件 `[模板文件名].html`
- 在`urls.py`中导入`from app_01 import models`
- 方法中进行数据库操作

- 模板
  ```html
  
    <!--# layout-->
    <style>
    {% block css %} {% endblock %}
    </style>
    <body>
    {% block content %} {% endblock %}
    </body>
  
    <!--# index -->
  
  {% extends 'layout.html' %}
  
  {% block css %}
  
  {% endblock %}
  {% block content %}
    <div class="container">
    </div>
    {% endblock %}
  
  ```

## Form 组件

- views.py
  ```python

  class MyForm(Form):
      user = forms.charField(widge=forms.Input)
      pwd = forms.charField(widge=forms.PasswordInput)
  
  
  def user_add(request):
    if request.method == 'GET'
        form = MyForm()
        return render(request, 'user_add.html', {'form': from}) 
  ```
    - html 代码
  ```html
      <form action="" method="post">
        {{from.user}}
        {{from.pwd}}
      <!--<input type="text" name="user" placeholder="请输入用户名">-->
      </form>
  ```
  ```html
     <form action="" method="post">
      {% for field in form%}
        {% field %}
        {$ endfor %}
     </form>
  ```

## ModelForm

- views.py
  ```python
  from django import forms
  
  class MyModelForm(forms.ModelForm):
    xx = forms.CharField(label='用户名')
      class Meta:
        model = models.UserInfo
        fields = ['user', 'pwd']
  
  def user_add(request):
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

  ```

### 模糊查询

  ```python
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

```

### 分页组件

```python
"""
分页

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

```

### bootstrap 样式父类

```python
from django import forms


class BootstrapForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field.widget.attrs:
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = field.label
            else:
                field.widget.attrs = {
                    'class': 'form-control',
                    'placeholder': field.label
                }

```