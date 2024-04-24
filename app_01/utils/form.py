from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app_01 import models
from app_01.utils.bootstrap import BootstrapForm
from app_01.utils.encrypt import md5


class UserModelForm(forms.ModelForm):
    password = forms.CharField(
        label='密码',
        min_length=3,
        max_length=10,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        # widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'gender', 'depart', 'create_time']
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control'}),
        #     'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'age': forms.NumberInput(attrs={'class': 'form-control'}),
        #     'gender': forms.Select(attrs={'class': 'form-control'}),
        #     'depart': forms.Select(attrs={'class': 'form-control'}),
        #     'create_time': forms.DateTimeInput(attrs={'class': 'form-control'})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环每个字段,给每个字段添加样式
        for name, field in self.fields.items():
            if name == 'create_time':
                field.widget.attrs = {'class': 'form-control'}
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}


# 继承BootstrapForm
class PrettynumModelForm(BootstrapForm):
    # 方式一
    mobile = forms.CharField(
        label='手机号',
        min_length=11,
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control'}),

        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]  # 正则验证
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status'] # 指定字段
        fields = '__all__'  # 全部字段
        # exclude = ['level'] 排除某个字段

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # 循环每个字段,给每个字段添加样式
    #     for name, field in self.fields.items():
    #         field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    # 方式二 clean_字段名
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']

        if models.PrettyNum.objects.filter(mobile=txt_mobile).exists():
            raise ValidationError('手机号已存在')
        else:
            return txt_mobile
        #
        # # 验证不通过raise ValidationError("错误信息") 通过 return 值
        # if len(txt_mobile) != 11:
        #     raise ValidationError('手机号格式错误')
        # else:
        #     return txt_mobile


class PrettynumEditModelForm(forms.ModelForm):
    # 方式一
    mobile = forms.CharField(
        label='手机号',
        min_length=11,
        max_length=11,
        widget=forms.TextInput(attrs={'class': 'form-control'}),

        validators=[RegexValidator(r'^1[3-9]\d{9}$', '手机号格式错误')]  # 正则验证
    )

    class Meta:
        model = models.PrettyNum
        # fields = ['mobile', 'price', 'level', 'status'] # 指定字段
        fields = '__all__'  # 全部字段
        # exclude = ['level'] 排除某个字段

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 循环每个字段,给每个字段添加样式
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control', 'placeholder': field.label}

    # 方式二 clean_字段名
    def clean_mobile(self):

        txt_mobile = self.cleaned_data['mobile']

        if models.PrettyNum.objects.exclude(id=self.instance.id).filter(mobile=txt_mobile).exists():
            raise ValidationError('手机号已存在')
        else:
            return txt_mobile


class AdminModelForm(BootstrapForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)

    def clean_confirm_password(self):
        confirm = self.cleaned_data['confirm_password']
        pwd = self.cleaned_data['password']
        if md5(confirm) != pwd:
            raise ValidationError('密码不一致')
        return confirm


class AdminEditModelForm(BootstrapForm):
    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootstrapForm):
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data['password']
        md5_pwd = md5(pwd)
        # 判断是否与历史密码相同
        if models.Admin.objects.filter(id=self.instance.pk, pwd=md5_pwd).exists():
            raise ValidationError('密码不能与历史密码相同')

        return md5_pwd

    def clean_confirm_password(self):
        confirm = self.cleaned_data['confirm_password']
        pwd = self.cleaned_data['password']
        if md5(confirm) != pwd:
            raise ValidationError('密码不一致')
        return confirm


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput,
        required=True,
        error_messages={'required': '用户名不能为空'}
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(render_value=True),
        required=True,
        error_messages={'required': '密码不能为空'}
    )

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return md5(pwd)
