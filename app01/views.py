from django.shortcuts import render, HttpResponse, redirect
from django.contrib import auth
# Create your views here.
from app01 import models
from django.contrib.auth.models import User


def index(request):
    if not request.user.is_authenticated():
        return redirect("/login/")

    all_book_list = models.Book.objects.all()
    return render(request, "index.html", locals())


def add(request):
    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        pubDate = request.POST.get("pubDate")
        publish_id = request.POST.get("publisher")
        authors_id_list = request.POST.getlist("authorlist")

        current_book = models.Book.objects.create(title=title, price=price, publishDate=pubDate, publish_id=publish_id)
        authors = models.Author.objects.filter(id__in=authors_id_list)
        current_book.authorlist.add(*authors)
        print(request.POST)

        return redirect("/index/")
    publishList = models.Publish.objects.all()
    authorList = models.Author.objects.all()
    return render(request, "add.html", locals())


def edit(request, edit_book_id):
    edit_book = models.Book.objects.filter(id=edit_book_id).first()
    publishList = models.Publish.objects.all()
    authorList = models.Author.objects.all()
    edit_book_authors = edit_book.authorlist.all().values_list("id")
    print(edit_book_authors)
    l = []

    for i in edit_book_authors:
        l.append(i[0])  # [2,3]
    return render(request, "edit.html", locals())


def delet(request, id):
    models.Book.objects.filter(id=id).delete()
    return redirect('/index/')


def log_in(request):
    #:登录页面
    info = ""
    if request.method == "POST":
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        user = auth.authenticate(username=user, password=pwd)
        if user:
            auth.login(request, user)
            return redirect('/index/')
        else:
            info = "有错误"
            return render(request, "login.html", {"info": info})
    return render(request, 'login.html')


def log_out(request):
    #:注销
    auth.logout(request)
    return redirect('/login/')


def log_reg(request):
    #:注册
    err = ""
    if request.method == "POST":
        user = request.POST.get('user' ,None)
        pwd = request.POST.get("pwd", None)
        User.objects.create_user(username=user,password=pwd)
        return redirect("/login/")
    return render(request,"reg.html")

    # if request.method=="POST":
    #     user=request.POST.get('user',None)
    #     pwd=request.POST.get('pwd',None)
    #     pwd_q = request.POST.get("new_pwd",None)
    #     if not user:
    #         err = '用户名不能为空'
    #     elif not pwd or not pwd_q:
    #         err = "密码不能为空"
    #     elif not pwd != pwd_q:
    #         err = "密码输入不一致"
    #     elif User.objects.filter(username=user):
    #         err='用户名存在'
    #     else:
    #         User.objects.create_user(username=user,password=user)
    #         return redirect('/login/')
    # return render(request,"reg.html")


def setPwd(request):
    # ：修改密码
    if request.method == "POST":
        user = request.POST.get("user")
        old_pwd = request.POST.get("old_pwd")
        new_pwd = request.POST.get("new_pwd")

        username = request.user
        user = User.objects.get(username=username)

        ret = user.check_password(old_pwd)

        if ret:
            user.set_password(new_pwd)
            user.save()
            return redirect("/login/")
        else:
            info = "输入密码有误"
            return render(request, "setPwd.html", {"info": info})

    return render(request, "setPwd.html")
