from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from app_01 import models
from app_01.utils.bootstrap import BootstrapForm


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