"""forumapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from forum import views

urlpatterns = [
    url(r'question/listing/$', views.Question_List_View, name='Question_List_View'),
    url(r'question/add/$',views.addquestion, name='addquestion'),
    url(r'question/(?P<question_id>[0-9]+)/$', views.question_page, name='question_page'),
    url(r'login/$', views.login_page, name='login_page'),
    url(r'signup/$', views.signup_page, name='signup_page'),
    url(r'answer/add/$',views.answer,name='answer'),
    url(r'answer/(?P<answer_id>[0-9]+)/$',views.answer_page,name='answer_page'),
    url(r'^search/$', views.search, name='search'),
    url(r'search/listing/$',views.topic_list,name='topic_list'),
    url(r'home/$',views.home_page, name='home_page'),


]