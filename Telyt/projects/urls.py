# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from projects import views

app_name = 'projects'
urlpatterns = [
    # 
    url(r'^$',views.index,name="index"),
    url(r'^index/',views.index,name="index"),
    url(r'^dashboard/',views.dashboard,name="dashboard"),
    url(r'^projectdetails/(?P<projectname>\w+)',views.project_details,name="projectdetails"),
    url(r'^projectadd/',views.project_create,name="projectadd"),
    url(r'^filesadd/(?P<projectname>\w+)/$',views.file_upload,name="filesadd"),
    
]
