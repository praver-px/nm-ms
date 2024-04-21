"""
URL configuration for nm_ms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_01.view import depart, prettynum, user, admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('depart/list/', depart.depart_list),
    path('depart/add/', depart.depart_add),
    path('depart/delete/<int:id>/', depart.depart_delete),
    path('depart/edit/<int:id>/', depart.depart_edit),

    path('user/list/', user.user_list),
    path('user/add/', user.user_add),
    path('user/create/', user.user_create),
    path('user/edit/<int:id>/', user.user_edit),
    path('user/delete/<int:id>/', user.user_delete),

    path('prettynum/list/', prettynum.prettynum_list),
    path('prettynum/add/', prettynum.prettynum_add),
    path('prettynum/edit/<int:id>', prettynum.prettynum_edit),
    path('prettynum/delete/<int:id>', prettynum.prettynum_delete),

    path('admin/list/', admin.admin_list),

]
