from django.shortcuts import render
from .models import ArticleColumn
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url="account/login")
def article_column(request):
    pass
