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
    url(r'^addProjectPermission/',views.AddProjectPermission,name="addProjectPermission"),
    url(r'^projectdetails/(?P<projectid>[0-9]+)',views.project_details,name="projectdetails"),
    url(r'^projectdetailsedit/(?P<projectid>[0-9]+)',views.project_details_edit,name="projectdetailsedit"),
    url(r'^projectdetailsdelete/(?P<projectid>[0-9]+)',views.project_details_delete,name="projectdetailsdelete"),
    url(r'^projectadd/',views.project_create,name="projectadd"),
    url(r'^filesadd/(?P<projectid>[0-9]+)/$',views.file_upload,name="filesadd"),
    url(r'^filesdelete/(?P<fileid>[0-9]+)/(?P<projectid>[0-9]+)/$',views.file_delete,name="filesdelete"),
    url(r'^admindashboard/',views.admindashboard,name="admindashboard"),
    url(r'^userprojects/(?P<username>\w+)',views.user_projects,name="userprojects"),
    url(r'^adminprojectdetails/(?P<projectname>\w+)',views.adminproject_details,name="adminprojectdetails"),
    url(r'^profile/',views.profile,name="profile"),
    url(r'^profileupdate/(?P<userid>[0-9]+)/$',views.profile_update,name="profileupdate"),
    url(r'^profilepicture/(?P<userid>[0-9]+)/$',views.profile_picture,name="profilepicture"),
]
