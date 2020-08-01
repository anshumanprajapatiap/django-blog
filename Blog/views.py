from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from datetime import date

# Create your views here.
def All_category():
    all_cat = Categorie.objects.all()
    return all_cat

def recent_and_popular():
    allpost = Post.objects.all()

    recent_three = allpost[::-1][:3]
    like = []
    le = len(allpost)
    newpost = []
    for i in allpost:
        l = LikeComment.objects.filter(post_data=i, like=True).count()
        like.append(l)
        for i in range(le):
            if max(like) > 0:
                m = max(like)
                p = like.index(m)
                po = allpost[p]
                like.pop(p)
                like.insert(p, 0)
                newpost.append(po)
        top_three = newpost[:3]
        return top_three, recent_three

def Index(request):
    post_data = Post.objects.all()

    li = []
    for i in post_data:
        like = LikeComment.objects.filter(post_data=i,like=True).count()
        li.append(like)
    z =zip(post_data, li)
    top3, recent3 = recent_and_popular()
    d={"allcat": All_category(), "post_data":z, "top3": top3,"recent3": recent3}
    print(All_category())
    return render(request, 'index.html', d)


def Login(request):
    error = False
    exist = False
    if request.method == 'POST':
        x = request.POST
        try:
            us = x['usr']
            pa = x['pas']
            user = authenticate(username=us, password=pa)
            if user:
                login(request, user)
                return redirect('Index')
            else:
                error = True
        except:
            U = x['username']
            F = x['first']
            L = x['last']
            E = x['email']
            P = x['password']
        udata = User.objects.filter(username=U)
        if udata:
            exist = True
        else:
            user = User.objects.create_user(username=U, password=P, email=E, first_name=F, last_name=L)
            UserDetail.objects.create(usr=user)
            return redirect('login')

    d = {"allcat": All_category(), "error": error, "exist":exist}
    return render(request, 'signin.html', d)


def Logout(request):
    logout(request)
    return redirect('login')

def Profile(request):
    data = UserDetail.objects.filter(usr=request.user).first()
    post_data = Post.objects.all()
    if request.method == "POST":
        i = request.FILES['img']
        data.image = i
        data.save()
        return redirect('profile')
    d = {"allcat": All_category(), "userdata":data, "post_data": post_data}
    return render(request, 'profile.html', d)

def add_blog(request):
    data = UserDetail.objects.filter(usr=request.user).first()
    if request.method == "POST":
        dd = request.POST
        c = dd['cat']
        s = dd['short']
        l = dd['long']
        t = dd['title']
        img = request.FILES['img']
        cdata = Categorie.objects.get(id = c)
        user = request.user
        td = date.today()
        Post.objects.create(Cat=cdata, usr=user, Title=t, Short_dis=s, Long_dis=l, image=img, Post_date=td)
        return redirect('profile')
    d = {"allcat": All_category(), "userdata":data}
    return render(request, 'newpost.html', d)

def Blog_detail(request,bid):
    pdata = Post.objects.get(id=bid)
    cdata = LikeComment.objects.all()
    top3, recent3 = recent_and_popular()
    data = UserDetail.objects.all()
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        user = request.user
        td = date.today()
        d = request.POST
        c = d['Message']
        print(c)
        data = LikeComment.objects.filter(usr=request.user, post_data=pdata).first()
        if data:
            data.comment = c
            data.save()
        else:
            LikeComment.objects.create(usr=user, post_data=pdata, comment=c, date=td)
    d = {"allcat": All_category(), "data": pdata, 'cdata':cdata, "top3": top3,"recent3": recent3, 'udata':data}
    return render(request, 'single.html', d)

def Cat_Blog(request, sid):
    udata = UserDetail.objects.all()
    datai = Categorie.objects.get(id=sid)
    dataf = Post.objects.all()
    top3, recent3 = recent_and_popular()
    d = {"allcat": All_category(), 'datai':datai, 'dataf':dataf, 'udata':udata, "top3": top3,"recent3": recent3}
    return render(request, 'same-cat.html',d)

def blog_delete(request,bid):
    data = Post.objects.get(id=bid)
    data.delete()
    return redirect('profile')

def edit_blog(request, eid):
    data = Post.objects.get(id=eid)
    if request.method == "POST":
        dd = request.POST
        if dd['title'] == None:
            pass
        else:
            t = dd['title']
            data.Title = t
            data.save()

        if dd['short'] == None:
            pass
        else:
            s = dd['short']
            data.Short_dis = s
            data.save()

        if dd['long'] == None:
            pass
        else:
            l = dd['long']
            data.Long_dis = l
            data.save()

        return redirect('profile')
    d = {"allcat": All_category(), "data": data}
    return render(request, 'editblog.html', d)

def Like_post(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    data = Post.objects.get(id = pid)
    data2 = LikeComment.objects.filter(usr=request.user, like=True, post_data=data)

    if not data2:
        LikeComment.objects.create(post_data=data, usr=request.user, like=True)
        return redirect('Index')
    else:
        return redirect('Index')

def Post_comment(request, pid):
    if not request.user.is_authenticated:
        return redirect('login')
    pdata = Post.objects.get(id=pid)
    user = request.user
    td = date.today()
    if request.method == "POST":
        d = request.POST
        c = d['Message']
        data = LikeComment.objects.filter(usr=request.user,post_data=pdata).first()
        if data:
            data.comment = c
            data.save()
        else:
            LikeComment.objects.create(usr=user, post_data=pdata, comment=c, date=td)
        return redirect('detail', pid)