from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Projects,Files
from .forms import ProjectCreateForm,FileUploadForm
import requests


# Create your views here.
# -*- coding: utf-8 -*-
def index(request):
    return render(request, 'core/index.html',{})

@login_required
def dashboard(request):
    projects = Projects.objects.all()
    user_projects = projects.filter(owner=request.user)
    form = ProjectCreateForm(instance=request.user)
    context = {
        'form': form,
        'projects': user_projects,
    }
    return render(request, 'core/dashboard.html',context)

@login_required
def project_details(request,projectname):
    files = Files.objects.all()
    fileDetails = files.filter(project_parent__project_name__contains=projectname)
    projects = Projects.objects.all()
    projectDetails = projects.filter(owner=request.user).filter(project_name=projectname)
    if projectDetails.count() == 0:
            projects = Projects.objects.all()
            user_projects = projects.filter(owner=request.user)
            form = ProjectCreateForm(instance=request.user)
            context = {
                'form': form,
                'projects': user_projects,
            }
            return render(request, 'core/dashboard.html',context)
    else:
        f_form = FileUploadForm()
        form = ProjectCreateForm()
        context = {
            'project_name':projectname,
            'projectDetails': projectDetails,
            'f_form':f_form,
            'form':form,
            'fileDetails':fileDetails
        }
        return render(request, 'core/projectpopulate.html',context)

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
            messages.info(request, 'Project Creation succeded')
            #redirect
            project_name = form.cleaned_data['project_name']
            projects = Projects.objects.all()
            projectDetails = projects.filter(owner=request.user).filter(project_name=project_name)
            f_form = FileUploadForm()
            context = {
                'project_name':project_name,
                'projectDetails': projectDetails,
                'f_form':f_form,
            }
            return render(request, 'core/projectpopulate.html',context)
    #if any other method
    else:
        #re-initialize form
        form = ProjectCreateForm(instance=request.user)
        #error message
        messages.info(request, 'Project Creation failed')
        # return HttpResponse('METHOD SHOULD BE POST')
    
    return render(request, 'core/index.html',{'mes':'this is a message','form':form})

def file_upload(request,projectname):
    # Handle file upload
    if request.method == 'POST':
        print(projectname)
        projects = Projects.objects.all()
        projectDetails = projects.filter(owner=request.user).filter(project_name=projectname)
        project = Projects.objects.get(project_name=projectname)
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

            # Redirect to the document list after POST
            return redirect('projects:projectdetails projectname')
    else:
        form = FileUploadForm() # A empty, unbound form
        return redirect('projects:projectdetails projectname')

@login_required
def admindashboard(request):
    if request.user.is_superuser:
        users = User.objects.all()
        context = {
            'users': users,
        }
        return render(request, 'core/adminDashboard.html',context)
    else:
        HttpResponse("hello ordinary")

@login_required
def user_projects(request,username):
    projects = Projects.objects.all()
    user_projects = projects.filter(owner=username)
    if user_projects.count() == 0:
        context = {
            'projects': user_projects,
        }
        return render(request, 'core/dashboard.html',context)
    else:
        context = {
            'projects': user_projects,
        }
        return render(request, 'core/dashboard.html',context)

@login_required
def adminproject_details(request,projectname):
    files = Files.objects.all()
    print(projectname)
    fileDetails = files.filter(project_parent=projectname)
    context = {
        'fileDetails':fileDetails
    }
    return render(request, 'core/adminprojectpopulate.html',context)
            