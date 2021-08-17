from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Projects,Files,ProjectUsers
from .forms import ProjectCreateForm,FileUploadForm,ProfileUpdateForm,ImageUploadForm
import requests
import json


# Create your views here.
# -*- coding: utf-8 -*-
def index(request):
    return render(request, 'core/index.html',{})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        return redirect('projects:admindashboard')
    else:
        users = User.objects.all()
        my_projects = Projects.objects.filter(owner=request.user)
        user_projects = ProjectUsers.objects.filter(user=request.user)
        form = ProjectCreateForm(instance=request.user)
        total_projects = user_projects.count()
        context = {
            'total_projects':total_projects,
            'form': form,
            'givenprojects': user_projects,
            'myprojects':my_projects,
            'users':users
        }
        return render(request, 'core/dashboard.html',context)


@login_required
def AddProjectPermission(request):
    #if post
    if request.is_ajax() and request.method == 'POST':
        print(request.POST.get('project_id'))
        print(request.POST.getlist('users[]'))
        #create from instance
        form = ProjectCreateForm(request.POST)
        #if form is valid
        # if form.is_valid():
        # process form data
        projectid = request.POST.get('project_id')
        users = request.POST.getlist('users[]')
        print(users[0])
        mainproject = Projects.objects.get(id=projectid)
        print(mainproject)
        for i in range(len(users)):
            mainuser = User.objects.get(id=users[i])
            ProjectUsers.objects.create(
                project=mainproject,user=mainuser
            )
        return render(request, 'core/dashboard.html',{})
    return render(request, 'core/index.html',{})


@login_required
def project_details(request,projectid):
    files = Files.objects.all()
    fileDetails = files.filter(project_parent__id__contains=projectid)
    projects = Projects.objects.all()
    print(projects)
    print(request.user)
    projectDetails = projects.filter(owner=request.user).filter(id=projectid)
    print(projectDetails.count())
    if projectDetails.count() == 0:
            projects = Projects.objects.all()
            user_projects = projects.filter(owner=request.user)
            total_projects = user_projects.count()
            form = ProjectCreateForm(instance=request.user)
            context = {
                'total_projects':total_projects,
                'form': form,
                'projects': user_projects,
            }
            return render(request, 'core/dashboard.html',context)
    else:
        f_form = FileUploadForm()
        form = ProjectCreateForm()
        context = {
            'project_name':projectid,
            'projectDetails': projectDetails,
            'f_form':f_form,
            'form':form,
            'fileDetails':fileDetails
        }
        return render(request, 'core/projectpopulate.html',context)

def project_details_delete(request,projectid):
    print(projectid)
    project = Projects.objects.get(id=projectid).delete()
    # projects = Projects.objects.all()
    # user_projects = projects.filter(owner=request.user)
    # form = ProjectCreateForm(instance=request.user)
    # total_projects = user_projects.count()
    # context = {
    #     'total_projects':total_projects,
    #     'form': form,
    #     'projects': user_projects,
    # }
    return redirect('projects:dashboard')

@login_required
def project_details_edit(request,projectid):
    #if post
    if request.method == 'POST':
        #create from instance
        form = ProjectCreateForm(request.POST)
        #if form is valid
        if form.is_valid():
            # process form data
            Projects.objects.filter(id=projectid).update(
                project_name=form.cleaned_data['project_name']
            )
            # projects = Projects.objects.all()
            # user_projects = projects.filter(owner=request.user)
            # form = ProjectCreateForm(instance=request.user)
            # total_projects = user_projects.count()
            # context = {
            #     'total_projects':total_projects,
            #     'form': form,
            #     'projects': user_projects,
            # }
            return redirect('projects:dashboard')
    #if any other method
    else:
        #re-initialize form
        # form = ProjectCreateForm(instance=request.user)
        #error message
        # messages.info(request, 'Project Creation failed')
        # return HttpResponse('METHOD SHOULD BE POST')
        return redirect('projects:dashboard')
    return redirect('projects:dashboard')

@login_required
def project_create(request):
    #if post
    if request.method == 'POST':
        #create from instance
        form = ProjectCreateForm(request.POST)
        #if form is valid
        if form.is_valid():
            # process form data
            obj = Projects() #gets new object
            obj.project_name = form.cleaned_data['project_name']
            obj.owner = request.user
            #finally save the object in db
            obj.save()
            #success message
            projects = Projects.objects.all()
            user_projects = projects.filter(owner=request.user)
            form = ProjectCreateForm(instance=request.user)
            total_projects = user_projects.count()
            ProjectUsers.objects.create(
                project=obj,user=request.user
            )
            context = {
                'total_projects':total_projects,
                'form': form,
                'projects': user_projects,
            }
            return redirect('projects:dashboard')
    #if any other method
    else:
        #re-initialize form
        form = ProjectCreateForm(instance=request.user)
        #error message
        messages.info(request, 'Project Creation failed')
        # return HttpResponse('METHOD SHOULD BE POST')
        return redirect('projects:dashboard')
    return redirect('projects:dashboard')

def file_upload(request,projectid):
    # Handle file upload
    if request.method == 'POST':
        print(projectid)
        projects = Projects.objects.all()
        projectDetails = projects.filter(owner=request.user).filter(id=projectid)
        project = Projects.objects.get(id=projectid)
        f_form = FileUploadForm()
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # process form data
            newdoc = Files() #gets new object
            newdoc.project_parent = project
            newdoc.file_upload = request.FILES['files']
            newdoc.file_name = request.FILES['files'].name
            #finally save the object in db
            newdoc.save()
            # messages.success(request, 'File uploaded successfuly')
            # Redirect to the document list after POST
            return redirect('projects:projectdetails',projectid=projectid)
    else:
        form = FileUploadForm() # A empty, unbound form
        return redirect('projects:projectdetails',projectid=projectid)

def file_delete(request,fileid,projectid):
    print(projectid)
    project = Files.objects.get(id=fileid).delete()
    form = FileUploadForm() # A empty, unbound form
    return redirect('projects:projectdetails',projectid=projectid)


@login_required
def admindashboard(request):
    if request.user.is_superuser:
        users = User.objects.all()
        total_users = users.count()
        context = {
            'users': users,
            'total_users':total_users,
        }
        return render(request, 'core/adminDashboard.html',context)
    else:
        HttpResponse("hello ordinary")

@login_required
def user_projects(request,username):
    projects = Projects.objects.all()
    user_projects = projects.filter(owner=username)
    total_projects = user_projects.count()
    if user_projects.count() == 0:
        context = {
            'total_projects':total_projects,
            'projects': user_projects,
        }
        return render(request, 'core/dashboard.html',context)
    else:
        context = {
            'total_projects':total_projects,
            'projects': user_projects,
        }
        return render(request, 'core/dashboard.html',context)

@login_required
def adminproject_details(request,projectname):
    files = Files.objects.all()
    fileDetails = files.filter(project_parent=projectname)
    context = {
        'fileDetails':fileDetails,
    }
    return render(request, 'core/adminprojectpopulate.html',context)

@login_required
def profile(request):
    users = User.objects.all()
    user_profile = users.filter(username=request.user)
    my_projects = Projects.objects.filter(owner=request.user)
    form = ProfileUpdateForm(instance=request.user)
    p_form = ImageUploadForm(instance=request.user.profile)
    return render(request, 'core/profile.html',{'user_profile':user_profile,'my_projects':my_projects,'form':form,'image_form':p_form})

def profile_update(request,userid):
    print(userid)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST)
        if form.is_valid():
            User.objects.filter(id=userid).update(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect('projects:profile')
        else:
            print(form.errors)
    return redirect('projects:profile')

def profile_picture(request,userid):
    if request.method == 'POST':
        p_form = ImageUploadForm(request.POST, request.FILES, instance=request.user.profile)
        if p_form.is_valid():
            print("saving image")
            p_form.save()
        else:
            print(p_form.errors)
        return redirect('projects:profile')
    else:
        return redirect('projects:profile')
    return redirect('projects:profile')