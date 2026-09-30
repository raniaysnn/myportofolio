import datetime

from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required  # Tambahkan baris ini
from django.core.exceptions import PermissionDenied        # Tambahkan baris ini

from main.models import Experience, Project

from main.forms import ProjectForm, ExperienceForm # tugas3

def is_editor(user):
    return user.groups.filter(name="Editor").exists()


def show_main(request):
    last_login = request.COOKIES.get('last_login', 'Belum ada sesi login / Cookie tidak ditemukan')
    context = {
        "name": "Rania Yasin",
        "npm": "2506621945",
        "study_program": "S1 Ilmu Komputer",
        "bio": (
            "Mahasiswa Ilmu Komputer Universitas Indonesia yang tertarik "
            "pada pengembangan perangkat lunak dan pendidikan."
        ),
        "last_login": last_login,
    }
    return render(request, "index.html", context)


def show_experience(request):
    json_response = get_experiences_json(request)

    experiences = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    experience_list = [experience.object for experience in experiences]

    context = {
        "name": "Rania Yasin",
        "experience_list": experience_list,
    }
    return render(request, "experience.html", context)

def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil ditambahkan!")
        return redirect("main:show_experience")

    context = {
        "name": "Rania Yasin",
        "form": form,
        "form_title": "Tambah Experience",
        "submit_label": "Tambah Experience",
    }
    return render(request, "experience_form.html", context)


def update_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Pengalaman berhasil diperbarui!")
        return redirect("main:show_experience")

    context = {
        "name": "Rania Yasin",
        "form": form,
        "form_title": "Edit Experience",
        "submit_label": "Simpan Perubahan",
    }
    return render(request, "experience_form.html", context)


def delete_experience(request, experience_id):
    experience = get_object_or_404(Experience, pk=experience_id)

    if request.method == "POST":
        experience.delete()
        messages.success(request, "Pengalaman berhasil dihapus!")

    return redirect("main:show_experience")


def get_experiences_json(request):
    experiences = Experience.objects.all().order_by("-started_at")
    experiences_json = serializers.serialize("json", experiences)
    return HttpResponse(experiences_json, content_type="application/json")

# def show_project(request):
#     project_list = Project.objects.all()

#     context = {
#         'name': 'Rania Yasin',
#         'project_list': Project.objects.all(),
#         'is_editor': request.user.is_authenticated and is_editor(request.user),
#     }

#     return render(request, "project.html", context)


def show_projects(request):
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rania Yasin",
        "title_query": title_query,
        "form": ProjectForm(),
    }
    return render(request, "project.html", context)


@login_required(login_url="/login/") 
def create_project(request):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_project")

    context = {
        "name": "Rania Yasin",
        "form": form,
    }
    return render(request, "project_form.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.prefetch_related('starred_by').all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    # Konstruksi data JSON secara manual agar bisa menyisipkan logika Star
    data = []
    for project in projects:
        starred_users = project.starred_by.all()
        is_starred = request.user in starred_users if request.user.is_authenticated else False
        starred_by_names = ", ".join([u.username for u in starred_users])

        data.append({
            "pk": str(project.id),
            "fields": {
                "title": project.title,
                "description": project.description,
                "category": project.category,
                "star_count": starred_users.count(),
                "is_starred": is_starred,
                "starred_by_names": starred_by_names,
            }
        })

    return JsonResponse(data, safe=False)

def show_projects(request):
    json_response = get_projects_json(request)

    projects = serializers.deserialize(
        "json",
        json_response.content.decode("utf-8"),
    )
    projects = [project.object for project in projects]
    title_query = request.GET.get("title", "").strip()

    context = {
        "name": "Rania Yasin",
        "project_list": projects,
        "title_query": title_query,
        "is_editor": request.user.is_authenticated and is_editor(request.user),
    }
    return render(request, "project.html", context)


@login_required(login_url="/login/") 
def delete_project(request, project_id):
    if not request.user.is_superuser:
        raise PermissionDenied
    
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_project")

    return redirect("main:show_project")

@login_required(login_url="/login/")
def update_projects(request, project_id):
    # UPDATE: boleh oleh superuser dan Editor
    if not request.user.is_superuser and not is_editor(request.user):
        raise PermissionDenied

    project = get_object_or_404(Project, pk=project_id)

    form = ProjectForm(
        request.POST or None,
        instance=project
    )

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek berhasil diperbarui!")
        return redirect("main:show_project")

    context = {
        "name": "Rania Yasin",
        "form": form,
        "form_title": "Edit Project",
        "submit_label": "Simpan Perubahan",
    }

    return render(request, "project_form.html", context)

def register(request):
    form = UserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Akun berhasil dibuat. Silakan login.")
        return redirect("main:login")

    context = {
        "name": "Rena",
        "form": form,
    }
    return render(request, "register.html", context)

def login_user(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        response = redirect("main:show_main")
        response.set_cookie('last_login', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        return response

    context = {
        "name": "Rena",
        "form": form,
    }
    return render(request, "login.html", context)

def logout_user(request):
    logout(request)
    response = redirect("main:show_main")
    response.delete_cookie('last_login')
    return response

# Tanpa cek is_superuser: semua akun yang sudah login boleh memberi star
@login_required(login_url="/login/")
def toggle_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        # Kalau akun ini sudah pernah memberi star, batalkan star-nya.
        # Kalau belum, tambahkan star.
        if request.user in project.starred_by.all():
            project.starred_by.remove(request.user)
        else:
            project.starred_by.add(request.user)

    return redirect("main:show_projects")