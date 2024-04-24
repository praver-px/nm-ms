from django.shortcuts import render, redirect

from app_01 import models
from app_01.utils.form import LoginForm


def login(request):
    if request == 'GET':
        content = {'form': LoginForm()}
        return render(request, 'login.html', content)
    form = LoginForm(data=request.POST)
    if form.is_valid():
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()

        if not admin_obj:
            return render(request, 'login.html', {'form': form})

        request.session['user'] = {'id': admin_obj.id, 'name': admin_obj.username}
        return redirect('/user/list/')
    return render(request, 'login.html', {'form': form})
