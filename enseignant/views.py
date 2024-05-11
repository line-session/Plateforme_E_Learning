import os
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .forms import RegisterForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from .admin import model_Cours, model_Devoir
from django.db.models import Q
from django.utils.text import slugify
from django.core.files.storage import default_storage

# Create your views here.
@login_required(login_url='/enseignant/login')
def home(request):
    return render(request, 'main_t/home.html')

def sign_up(request):
    if request.method == "POST":
        Vemail = request.POST.get('email')
        Vusername = request.POST.get('username').strip()
        Vfirst = request.POST.get('first_name').strip(" ")
        Vlast = request.POST.get('last_name').strip()
        Vpassword1 = request.POST.get('password1')
        Vpassword2 = request.POST.get('password2')
        
        if Vpassword1 != Vpassword2 or len(Vpassword1) < 8:
            return render(request, 'registration_t/sign_up.html', {'error':True, 'username':Vusername, 'email':Vemail, 'first_name':Vfirst, 'last_name':Vlast})
        else:
            form = RegisterForm(request.POST)
            verify = User.objects.filter(username = Vusername, email__icontains = Vemail).first()
            if form.is_valid() and not verify:
                user = form.save()
                teacher_group = Group.objects.get(name='Teachers')
                teacher_group.user_set.add(user)
                login(request, user)
                return redirect('/enseignant/home')
            else:
                return render(request, 'registration_t/sign_up.html', {'exist':True,'username':Vusername, 'email':Vemail, 'first':Vfirst, 'last':Vlast})
    else:
        return render(request, 'registration_t/sign_up.html')

def login_views(request):
    if request.method == "POST":
        username = request.POST.get('username').strip()
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/enseignant/home')
        else:
            return render(request, 'registration_t/login.html', {'error':True})
    else:
        return render(request, 'registration_t/login.html')

def logout_views(request):
    logout(request)
    return redirect('/enseignant/login')

# @login_required(login_url='/enseignant/login')
# def cours(request):
#     if request.method == "GET":
#         v_teacher = request.user
#         ensemble = model_Cours.objects.filter(teacher=v_teacher).order_by('-id')
#         if ensemble:
#             need = [{
#                 "id": cours.id,
#                 "title": cours.title,
#                 "description": cours.description,
#                 "subject": cours.subject,
#                 "classe": cours.classe,
#                 "image_file": cours.image_file,
#             } for cours in ensemble]
#             return render(request, 'cours_t/cours.html', {'all_cours': need})
#         else:
#             return render(request, 'cours_t/cours.html', {'all_cours': []})
#     else: 
#         return redirect('/enseignant/home')

@login_required(login_url='/enseignant/login')
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
            return render(request, 'cours_t/cours.html', {'all_cours': need})
        else:
            v_teacher = request.user
            ensemble = model_Cours.objects.filter(teacher=v_teacher).order_by('-id')
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
            return render(request, 'cours_t/cours.html', {'all_cours': need})
    else: 
        return redirect('/enseignant/home')
    
def add(request):
    if request.method == "POST":
        v_teacher = request.user
        v_title = request.POST.get('title')
        v_subject = request.POST.get('subject')
        v_description = request.POST.get('description')
        v_classe = request.POST.get('classe')
        v_image_file = request.FILES.get('image')
        v_video_file = request.FILES.get('video')

        new_cours = model_Cours.objects.create(
            title = v_title,
            subject = v_subject,
            teacher = v_teacher,
            description = v_description,
            classe = v_classe,
            image_file = v_image_file,
            video_file = v_video_file,
        )

        if new_cours:
            return redirect(f'/enseignant/cours/media/{new_cours.id}')
        else:
            return render(request, 'cours_t/add.html', {'fail':True})
        
    return render(request, 'cours_t/add.html', {'start':True})

def update_course(request, id):
    course = get_object_or_404(model_Cours, pk=id)

    if request.method == "GET":
        return render(request, 'cours_t/update.html', {'start': True, 'course': course})

    if request.method == "POST":
        last_image = course.image_file
        last_video = course.video_file

        course.title = request.POST.get('title')
        course.subject = request.POST.get('subject')
        course.description = request.POST.get('description')
        course.classe = request.POST.get('classe')
        course.image_file = request.FILES.get('image')
        course.video_file = request.FILES.get('video')

        try:
            course.save()

            if last_image:
                default_storage.delete(last_image.name)
            if last_video:
                default_storage.delete(last_video.name)

            return redirect(f'/enseignant/cours/media/{id}')
        except:
            return redirect(f'/enseignant/cours/media/{id}')

def delete_course(request, id):
    course = get_object_or_404(model_Cours, id=id)
    course.delete()
    return redirect('/enseignant/cours')            

def video_page(request, id):
    course = get_object_or_404(model_Cours, id=id)

    if course.video_file:
        video_url = course.video_file.url
        return render(request, 'cours_t/video_page.html', {'course': course, 'video_url': video_url})
    else:
        return render(request, 'cours_t/video_page.html', {'course': course, 'video_url': None})

def search(request):
    if request.method == "POST":
        query = request.POST.get('query')
        user = request.user
        course = model_Cours.objects.filter(teacher=user).order_by('-id')
        
        result = course.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(subject__icontains=query) |
            Q(teacher__first_name__icontains=query) |
            Q(teacher__last_name__icontains=query)
        )
        if result:
            need = [{
                "id": cours.id,
                "title": cours.title,
                "description": cours.description,
                "subject": cours.subject,
                "classe": cours.classe,
                "image_file": cours.image_file,
            } for cours in result ]
            return render(request, 'cours_t/search.html', {'all_cours': need, 'query':query})
        else:
            return render(request, 'cours_t/search.html', {'all_cours': [], 'not_found':True, 'query':query})
    else:
        return redirect('/enseignant/cours')
    
def display_devoir_t(request):
     if request.method == "GET":
         v_teacher = request.user
         ensemble = model_Devoir.objects.filter(teacher=v_teacher).order_by('-id')
         if ensemble:
             need = [{
                 "id": cours.id,
                 "title": cours.title,
                 "description": cours.description,
                 "subject": cours.subject,
                 "classe": cours.classe,
                 "duration": cours.duration,
             } for cours in ensemble]
             return render(request, 'cours_t/cours.html', {'all_cours': need})
         else:
             return render(request, 'cours_t/cours.html', {'all_cours': []})
     else: 
         return redirect('/enseignant/home')


def download_devoir_t(request, id):
    devoir = get_object_or_404(model_Devoir, pk=id)
    path = devoir.document_file.path

    # Determine the file extension
    _, extension = os.path.splitext(path)

    # Open the file as binary data
    with open(path, 'rb') as document_file:
        # Create an HTTP response with the file as content
        response = HttpResponse(document_file.read(), content_type='application/octet-stream')

    # Set the Content-Disposition header to force download
    filename = slugify(devoir.title) + extension.lower()  # Use slugified title with original extension
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

