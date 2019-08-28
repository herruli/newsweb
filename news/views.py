from django.http import HttpResponse
from django.shortcuts import render
from .models import News

# Create your views here.
def newspage_view(request,*args, **kwargs):
    queryset = News.objects.all()
    newsList = {'object_list':queryset}
    return render(request,'news.html',newsList)

