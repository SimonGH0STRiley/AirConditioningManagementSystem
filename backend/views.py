from django.db.models import Sum
from django.shortcuts import render, HttpResponse
from django.shortcuts import redirect

from . import forms
from . import models
from backend import models


# # Create your views here.
def test(request):
    var = models.Report.objects.filter(room_id=1, start_time__gt="2020-06-01", start_time__lt="2020-07-01")
    print(var.values())
    return HttpResponse("ok")


def index(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'backend/index.html')


def login(request):
    if request.session.get('is_login', None):  # 不允许重复登录
        return redirect('/index/')
    if request.method == "POST":
        login_form = forms.UserForm(request.POST)
        message = '请检查填写的内容！'
        if login_form.is_valid():
            # 验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            try:
                tenant = models.Tenant.objects.get(name=username)
            except:
                message = '不存在此房客！'
                return render(request, 'backend/login.html', locals())
            if tenant.password == password:
                request.session['is_login'] = True
                request.session['user_id'] = tenant.id
                request.session['user_name'] = tenant.name
                return redirect('/tenantview/')

            else:
                message = '密码不正确！'
                return render(request, 'backend/login.html', locals())
        else:
            return render(request, 'backend/login.html', locals())
    # 对于非POST方法发送数据时（比如GET方法请求页面），返回空的表单，让用户可以填入数据
    login_form = forms.UserForm()
    return render(request, 'backend/login.html', locals())


def register(request):
    if request.session.get('is_login', None):
        return redirect('/index/')
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        message = "请检查填写的内容！"
        if register_form.is_valid():
            username = register_form.cleaned_data.get('username')
            password1 = register_form.cleaned_data.get('password1')
            password2 = register_form.cleaned_data.get('password2')
            if password1 != password2:
                message = '两次输入的密码不同！'
                return render(request, 'backend/register.html', locals())
            else:
                same_name_tenant = models.Tenant.objects.filter(name=username)
                if same_name_tenant:
                    message = '用户名已经存在'
                    return render(request, 'backend/register.html', locals())

                new_tenant = models.Tenant()
                new_tenant.name = username
                new_tenant.password = password1
                new_tenant.save()

                return redirect('/login/')
        else:
            return render(request, 'backend/register.html', locals())
    register_form = forms.RegisterForm()
    return render(request, 'backend/register.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect("/login/")
    request.session.flush()
    return redirect("/login/")


def acadminview(request):
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')
    return render(request, 'backend/acadminview.html')


def waiterview(request):
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')
    return render(request, 'backend/waiterview.html')


def managerview(request):
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')
    return render(request, 'backend/managerview.html')


def tenantview(request):
    if not request.session.get('is_login', None):
        return redirect('/login/')
    return render(request, 'backend/tenantview.html')
