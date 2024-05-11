import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from enseignant.admin import model_Cours, model_Devoir
from django.db.models import Q
from django.utils.text import slugify
from django.core.files.storage import default_storage

# Create your views here.
@login_required(login_url='/etudiant/login')
def home(request):
    return render(request, 'main_s/home.html')

def sign_up(request):
    if request.method == "POST":
        Vemail = request.POST.get('email')
        Vusername = request.POST.get('username').strip()
        Vfirst = request.POST.get('first_name').strip(" ")
        Vlast = request.POST.get('last_name').strip()
        Vpassword1 = request.POST.get('password1')
        Vpassword2 = request.POST.get('password2')
        
        if Vpassword1 != Vpassword2 or len(Vpassword1) < 8:
            return render(request, 'registration_s/sign_up.html', {'error':True, 'username':Vusername, 'email':Vemail, 'first_name':Vfirst, 'last_name':Vlast})
        else:
            form = RegisterForm(request.POST)
            verify = User.objects.filter(username = Vusername, email__icontains = Vemail).first()
            if form.is_valid() and not verify:
                user = form.save()
                student_group = Group.objects.get(name='Students')
                student_group.user_set.add(user)
                login(request, user)
                return redirect('/etudiant/home')
            else:
                return render(request, 'registration_s/sign_up.html', {'exist':True,'username':Vusername, 'email':Vemail, 'first':Vfirst, 'last':Vlast})
    else:
        return render(request, 'registration_s/sign_up.html')

def login_views(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/etudiant/home')
        else:
            return render(request, 'registration_s/login.html', {'error':True})
    else:
        return render(request, 'registration_s/login.html')

def logout_views(request):
    logout(request)
    return redirect('/etudiant/login')