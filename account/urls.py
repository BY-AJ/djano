from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    #登录用户
    url(r'^login/$',views.user_login,name="user_login"),

    #退出登录(使用内置的退出功能)
    url(r'^logout/$',auth_views.logout,{"template_name":"account/logout.html"},name="user_logout"),

    #注册用户
    url(r'^register/$',views.user_register,name="user_register"),

    #修改密码
    url(r'^password-change/$',auth_views.password_change,{"post_change_redirect":"/account/password-change-done"},name='password_change'),
    url(r'^password-change-done/$',auth_views.password_change_done,name='password_change_done'),

    #重置密码
    url(r'^password-reset/$',auth_views.password_reset,
        {"template_name":"account/password_reset_form.html",
        "email_template_name":"account/password_reset_email.html","subject_template_name":"account/password_reset_subject.txt",
        "post_reset_redirect":"/account/password-reset-done"},
        name="password_reset"),

    url(r'^password-reset-done/$',auth_views.password_reset_done,
        {"template_name":"account/password_reset_done.html"},
        name="password_reset_done"),  

    url(r'^password-reset-confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/$',auth_views.password_reset_confirm,
        {"template_name":"account/password_reset_confirm.html",
        "post_reset_redirect":"/account/password-reset-complete"},
        name="password_reset_confirm"),

    url(r'^password-reset-complete/$',auth_views.password_reset_complete,
        {"template_name":"account/password_reset_complete.html"},name="password_reset_complete"),

    #个人信息
    url(r'^my-information/$',views.myself,name="my_information"),

    #编辑个人信息
    url(r'^edit-my-information/$',views.myself_edit,name="edit_my_information"),    

    #个人头像
    url(r'^my-image/$',views.my_image,name="my_image"),  
]