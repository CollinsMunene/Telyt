from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Projects,Files
from .forms import ProjectCreateForm
import requests


# Create your views here.
# -*- coding: utf-8 -*-
@login_required
def index(request):
    form = ProjectCreateForm()
    return render(request, 'core/index.html',{'mes':'this is a message','form':form,'user':request.user})

@login_required
def project_create(request):
    #if post
    if request.method == 'POST':
        #create from instance
        form = ProjectCreateForm(request.POST)
        #if form is valid
        if form.is_valid():
            form.save()
            #success message
            messages.info(request, 'Project Creation succeded')
            #redirect
            project_name = form.cleaned_data['project_name']
            project_detailForm = FileAddForm()
            return render(request, 'core/projectpopulate.html',{'project_name':project_name,'form':project_detailForm})
    #if any other method
    else:
        #re-initialize form
        form = ProjectCreateForm()
        #error message
        messages.info(request, 'Project Creation failed')
        # return HttpResponse('METHOD SHOULD BE POST')
    
    return render(request, 'core/index.html',{'mes':'this is a message','form':form})