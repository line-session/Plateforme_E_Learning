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
        v_classroom = request.POST.get('classe')
        
        if Vpassword1 != Vpassword2 or len(Vpassword1) < 8:
            return render(request, 'registration_s/sign_up.html', {'error':True, 'username':Vusername, 'email':Vemail, 'first_name':Vfirst, 'last_name':Vlast})
        else:
            form = RegisterForm(request.POST)
            verify = User.objects.filter(username = Vusername, email__icontains = Vemail).first()
            if form.is_valid() and not verify:
                user = form.save()
                student_group = Group.objects.get(name='Students')
                student_group.user_set.add(user)
                classroom_group = Group.objects.get(name=v_classroom)
                classroom_group.user_set.add(user)
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

@login_required(login_url='/etudiant/login')
def cours(request):
    if request.method == "GET":
        tri = request.GET.get('tri')
        if tri:
            v_teacher = request.user
            ensemble = model_Cours.objects.filter(teacher=v_teacher).order_by('-id')  # Tri par défaut
            if tri == 'dut1':
                ensemble = ensemble.filter(classe='DUT1')
            elif tri == 'dut2':
                ensemble = ensemble.filter(classe='DUT2')
            if ensemble.exists():
                need = [{
                    "id": cours.id,
                    "title": cours.title,
                    "description": cours.description,
                    "subject": cours.subject,
                    "classe": cours.classe,
                    "image_file": cours.image_file,
                } for cours in ensemble]
            else:
                need = []
            return render(request, 'cours_s/cours.html', {'all_cours': need})
        else:
            v_student = request.user
            classroom_dut1 = v_student.groups.filter(name='DUT1').first()
            classroom_dut2 = v_student.groups.filter(name='DUT2').first()
            ensemble = model_Cours.objects.all().order_by('-id')
            if ensemble.exists():
                courses_for_dut1 = []
                courses_for_dut2 = []
                for courses in ensemble:
                    if classroom_dut1 is not None and courses.classe == 'DUT1':
                        need = {
                            "id": courses.id,
                            "title": courses.title,
                            "description": courses.description,
                            "subject": courses.subject,
                            "classe": courses.classe,
                            "image_file": courses.image_file,
                        }
                        courses_for_dut1.append(need)
                    if classroom_dut2 is not None and courses.classe == 'DUT2':
                        need = {
                            "id": courses.id,
                            "title": courses.title,
                            "description": courses.description,
                            "subject": courses.subject,
                            "classe": courses.classe,
                            "image_file": courses.image_file,
                        }
                        courses_for_dut2.append(need)
            else:
                courses_for_dut1 = []
                courses_for_dut2 = []
            return render(request, 'cours_s/cours.html', {'courses_for_dut1': courses_for_dut1, 'courses_for_dut2':courses_for_dut2})
    else: 
        return redirect('/etudiant/home')

def video_page(request, id):
    course = get_object_or_404(model_Cours, id=id)

    if course.video_file:
        video_url = course.video_file.url
        return render(request, 'cours_s/video_page.html', {'course': course, 'video_url': video_url})
    else:
        return render(request, 'cours_s/video_page.html', {'course': course, 'video_url': None})

def search(request):
    if request.method == "POST":
        query = request.POST.get('query')
        user = request.user
        classroom_dut1 = user.groups.filter(name='DUT1').first()
        classroom_dut2 = user.groups.filter(name='DUT2').first()
        ensemble = model_Cours.objects.all().order_by('-id')
        if ensemble.exists():
            courses_for_dut1 = []
            courses_for_dut2 = []
            for courses in ensemble:
                if classroom_dut1 is not None and courses.classe == 'DUT1':
                    need = {
                        "id": courses.id,
                        "title": courses.title,
                        "description": courses.description,
                        "subject": courses.subject,
                        "classe": courses.classe,
                        "image_file": courses.image_file,
                    }
                    courses_for_dut1.append(need)
                if classroom_dut2 is not None and courses.classe == 'DUT2':
                    need = {
                        "id": courses.id,
                        "title": courses.title,
                        "description": courses.description,
                        "subject": courses.subject,
                        "classe": courses.classe,
                        "image_file": courses.image_file,
                    }
                    courses_for_dut2.append(need)
        else:
            courses_for_dut1 = []
            courses_for_dut2 = []
        
        result_dut1 = model_Cours.objects.filter(
            id__in=[c['id'] for c in courses_for_dut1] 
        )
        result_dut2 = model_Cours.objects.filter(
            id__in=[c['id'] for c in courses_for_dut2] 
        )
        
        result_dut1 = result_dut1.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query)
        )
        result_dut2 = result_dut2.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query)
        )
        
        if result_dut1:
            need = [{
                "id": cours.id,
                "title": cours.title,
                "description": cours.description,
                "subject": cours.subject,
                "classe": cours.classe,
                "image_file": cours.image_file,
            } for cours in result_dut1 ]
            return render(request, 'cours_s/search.html', {'courses_for_dut1': need, 'query':query})
        if result_dut2:
            need = [{
                "id": cours.id,
                "title": cours.title,
                "description": cours.description,
                "subject": cours.subject,
                "classe": cours.classe,
                "image_file": cours.image_file,
            } for cours in result_dut2 ]
            return render(request, 'cours_s/search.html', {'courses_for_dut2': need, 'query':query})
        else:
            return render(request, 'cours_s/search.html', {'all_cours': [], 'not_found':True, 'query':query})
    else:
        return redirect('/etudiant/cours')

def display_devoir_s(request):
    if request.method == "GET":
        v_student = request.user
        classroom_dut1 = v_student.groups.filter(name='DUT1').first()
        classroom_dut2 = v_student.groups.filter(name='DUT2').first()
        ensemble = model_Devoir.objects.all().order_by('-id')
        if ensemble.exists():
            devoir_for_dut1 = []
            devoir_for_dut2 = []
            for devoir in ensemble:
                if classroom_dut1 is not None and devoir.classe == 'DUT1':
                    need = {
                        "id": devoir.id,
                        "title": devoir.title,
                        "description": devoir.description,
                        "subject": devoir.subject,
                        "classe": devoir.classe,
                        "teacher": devoir.teacher,
                        "document_file": devoir.document_file,
                    }
                    devoir_for_dut1.append(need)
                if classroom_dut2 is not None and devoir.classe == 'DUT2':
                    need = {
                        "id": devoir.id,
                        "title": devoir.title,
                        "description": devoir.description,
                        "subject": devoir.subject,
                        "classe": devoir.classe,
                        "teacher": devoir.teacher,
                        "document_file": devoir.document_file,
                    }
                    devoir_for_dut2.append(need)
        else:
            devoir_for_dut1 = []
            devoir_for_dut2 = []
        return render(request, 'devoir_s/devoir.html', {'devoir_for_dut1': devoir_for_dut1, 'devoir_for_dut2':devoir_for_dut2})
    else: 
        return redirect('/etudiant/home')

def download_devoir_s(request, id):
    devoir = get_object_or_404(model_Devoir, pk=id)
    path = devoir.document_file.path

    _, extension = os.path.splitext(path)

    with open(path, 'rb') as document_file:
        response = HttpResponse(document_file.read(), content_type='application/octet-stream')

    filename = slugify(devoir.title) + extension.lower() 
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response
