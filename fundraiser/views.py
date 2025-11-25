from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProjectForm, LoginForm
from .models import Project
from django.contrib import messages

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password")
        password2 = request.POST.get("confirm")
        phone = request.POST.get("phone")

        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()
        messages.success(request, "Account created successfully")
        return redirect("login")
    return render(request, "register.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request,username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("projects_list")
        else:
            messages.error(request, "Invalid email or password")

    return render(request, "login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            return redirect('projects_list')
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})


@login_required
def projects_list(request):
    projects = Project.objects.all()
    return render(request, 'projects_list.html', {'projects': projects})


@login_required
def edit_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects_list')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'edit_project.html', {'form': form})



@login_required
def delete_project(request, project_id):
    project = get_object_or_404(Project, id=project_id, owner=request.user)
    project.delete()
    return redirect('projects_list')

# views.py
@login_required
def show_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'show_project.html', {'project': project})



@login_required
def search_project(request):
    date = request.GET.get("date")
    results = Project.objects.filter(start_date=date)
    return render(request, 'search_project.html', {'projects': results})
