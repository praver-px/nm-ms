from django.db import models


# Create your models here.
class Department(models.Model):
    """ 部门表"""
    title = models.CharField(verbose_name="部门名称", max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """ 员工表 """
    name = models.CharField(verbose_name="姓名", max_length=16)
    password = models.CharField(verbose_name="密码", max_length=64)
    age = models.IntegerField(verbose_name="年龄")
    account = models.DecimalField(verbose_name="账户余额", max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name="入职时间")

    # 无约束
    # dept_id = models.IntegerField(verbose_name="部门ID")

    # 约束
    # to 与那个表关联 to_field 关联那个表的哪个字段
    # django自动生成
    # 写的是depart 生成的是depart_id
    # on_delete=models.CASCADE 关联的部门被删除，对应关联的员工也被删除
    # on_delete=models.SET_NULL 关联的部门被删除，对应关联的员工的部门字段被置为null,该列要允许为空
    depart = models.ForeignKey(verbose_name="部门", to="Department", to_field="id", on_delete=models.CASCADE)

    # django 中的约束
    gender_choices = (
        (1, "男"),
        (2, "女"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="号码", max_length=11)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, default=0)
    level_choices = (
        (1, "1级"),
        (2, "2级"),
        (3, "3级"),
        (4, "4级"),
    )
    level = models.SmallIntegerField(verbose_name="级别", choices=level_choices, default=1)
    status_choices = (
        (1, "已售"),
        (2, "未售"),
    )
    status = models.SmallIntegerField(verbose_name="状态", choices=status_choices, default=2)


class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name="用户名", max_length=32)
    password = models.CharField(verbose_name="密码", max_length=64)
