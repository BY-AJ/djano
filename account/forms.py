from django import forms
# 引入Django默认的用户模型User类
from django.contrib.auth.models import User
from .models import UserProfile,UserInfo

# 登录
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget = forms.PasswordInput)

# 注册
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label = "Password",widget = forms.PasswordInput)
    password2 = forms.CharField(label = "Confirm Password",widget = forms.PasswordInput)

    #内部类，声明本表单所应用的数据模型
    class Meta:
        model = User#表示将来表单的内容会写入到那个数据库表中的哪些记录里面
        fields = ("username","email")#只引用model里面指定的字段(username,email)

    #该方法在我们调用is_valid()方法时会被执行
    #注意:以"clean_+属性名称"命名方式所创建的方法，都有类似的功能
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2'] :
            raise forms.ValidationError("passwords do not match.")
        return cd['password2']       

# 添加注册信息
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ("phone","birth")

#用户信息
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ("school","company","profession","address","aboutme","photo")      

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields =("email",) 
