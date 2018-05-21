from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login,authenticate

from .models import UserInfo,UserProfile
from .forms import UserForm,UserInfoForm,UserProfileForm,LoginForm,RegistrationForm

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
# 用户登录视图函数
def user_login(request):
    if request.method == 'POST':
        # 构造表单实例对象
        login_form = LoginForm(request.POST)
        # 检查表单对象是否有效
        if login_form.is_valid():
            cd = login_form.cleaned_data
            #检查是否存在用户
            user = authenticate(username = cd['username'],password = cd['password'])
            if user:
                login(request,user)
                return HttpResponseRedirect('/blog')
            else:
                return HttpResponse('sorry,your username or password is not right.')
        else:        
            return HttpResponse('Invalid Login')
            
    if request.method == 'GET':
        login_form = LoginForm()
        return render(request,'account/login.html',{"form":login_form})

#用户注册视图函数
def user_register(request):
    if request.method == 'GET':
        user_form = RegistrationsForm()
        profile_form = UserProfileForm()
        return render(request,'account/register.html',{"form":user_form,"profile":profile_form})

    if request.method == 'POST':
        user_form = RegistrationsForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            new_profile = userprofile_form.save(commit = False)
            new_profile.user = new_user
            new_profile.save()
            
            # 保存用户注册信息后，同时绑定userinfo数据库表中写入该用户的ID信息
            UserInfo.objects.create(user = new_user)

            return HttpResponseRedirect('/account/login/')
        else:
            return HttpResponse("sorry,your can not resgiter") 

#查看用户个人信息
@login_required(login_url = 'account/login/')
def myself(request):
    #通过objects这个模型管理器的all()获得所有数据行
    #获取单个对象
    user = User.objects.get(username = request.user.username)
    userprofile = UserProfile.objects.get(user = user)
    userinfo = UserInfo.objects.get(user = user)
    return render(request,"account/myself.html",{"user":user,"userprofile":userprofile,"userinfo":userinfo})

#编辑个人信息
@login_required(login_url = 'account/login/')
def myself_edit(request):
    user = User.objects.get(username = request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo = UserInfo.objects.get(user=request.user)

    if request.method == 'POST' :
        user_form = UserForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        userinfo_form= UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid() :
            user_cd = user_form.cleaned_data
            userprofile_cd = userprofile_form.cleaned_data
            userinfo_cd = userinfo_form.cleaned_data
            print(user_cd["email"])
            user.email = user_cd["email"]
            userprofile.birth = userprofile_cd["birth"]
            userprofile.phone = userprofile_cd["phone"]
            userinfo.school = userinfo_cd["school"]
            userinfo.company = userinfo_cd["company"]
            userinfo.profession = userinfo_cd["profession"]
            userinfo.address = userinfo_cd["address"]
            userinfo.aboutme = userinfo_cd["aboutme"]
            user.save()
            userprofile.save()
            userinfo.save()
        #HttpResponseRedirect()函数实现URL的转向
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = UserProfileForm(initial={"birth":userprofile.birth, "phone":userprofile.phone})
        userinfo_form = UserInfoForm(initial={"school":userinfo.school, "company":userinfo.company, "profession":userinfo.profession, "address":userinfo.address, "aboutme":userinfo.aboutme})
        return render(request, "account/myself_edit.html", {"user_form":user_form, "userprofile_form":userprofile_form, "userinfo_form":userinfo_form})

#上传个人头像
@login_required(login_url = 'account/login/')
def my_image(request):
    if request.method == 'POST':
        img = request.POST['img']
        userinfo = UserInfo.objects.get(user = request.user.id)
        userinfo.photo = img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,'account/imagecrop.html')    
