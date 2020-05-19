# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from projects import views

app_name = 'projects'
urlpatterns = [
    # 
    url(r'^index/',views.index,name="index"),
    url(r'^projectadd/',views.project_create,name="projectadd"),
    
]
