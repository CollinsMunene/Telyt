# Django imports
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from projects import views

app_name = 'projects'
urlpatterns = [
    # 
    url(r'^$',views.index,name="index"),
    url(r'^/',views.index,name="index"),
    url(r'^index/',views.index,name="index"),
    url(r'^dashboard/',views.dashboard,name="dashboard"),
    url(r'^projectdetails/(?P<projectname>\w+)',views.project_details,name="projectdetails"),
    url(r'^projectadd/',views.project_create,name="projectadd"),
    url(r'^filesadd/(?P<projectname>\w+)/$',views.file_upload,name="filesadd"),
    url(r'^admindashboard/',views.admindashboard,name="admindashboard"),
    url(r'^userprojects/(?P<username>\w+)',views.user_projects,name="userprojects"),
    url(r'^adminprojectdetails/(?P<projectname>\w+)',views.adminproject_details,name="adminprojectdetails"),
    
     url(r'^profile/',views.profile,name="profile"),
]
