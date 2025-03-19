from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Task, Project
from .forms import TaskForm, ProjectForm
import django_filters

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['icontains'],
            'status': ['exact'],
            'priority': ['exact'],
            'project': ['exact'],
            'due_date': ['gte', 'lte'],
        }

@login_required
def dashboard(request):
    user_tasks = Task.objects.filter(assigned_to=request.user).order_by('due_date')
    user_projects = Project.objects.filter(created_by=request.user)
    
    context = {
        'tasks': user_tasks,
        'projects': user_projects,
        'todo_count': user_tasks.filter(status='todo').count(),
        'in_progress_count': user_tasks.filter(status='in_progress').count(),
        'review_count': user_tasks.filter(status='review').count(),
        'done_count': user_tasks.filter(status='done').count(),
        # 'priority_count': user_tasks.filter(status='get_priority').count(),
    }
    return render(request, 'tasks/dashboard.html', context)

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'tasks/project_list.html'
    context_object_name = 'projects'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Project.objects.all()
        return Project.objects.filter(created_by=self.request.user)

class ProjectDetailView(LoginRequiredMixin, DetailView):
    model = Project
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(project=self.object)
        return context

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.created_by or self.request.user.is_superuser

class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('project-list')
    
    def test_func(self):
        project = self.get_object()
        return self.request.user == project.created_by and self.request.user.is_superuser

        # return self.request.user == project.created_by or self.request.user.is_superuser

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Task.objects.all()
        else:
            queryset = Task.objects.filter(project__created_by=self.request.user)
        
        self.filterset = TaskFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def test_func(self):
        task = self.get_object()
        # Allow superusers and the task creator to update
        return self.request.user.is_superuser or self.request.user == task.created_by

class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    success_url = reverse_lazy('task-list')
    
    def test_func(self):
        task = self.get_object()
        # Only allow superusers and the task creator to delete
        return self.request.user == task.created_by and self.request.user.is_superuser

    
    
    
# from django.contrib.auth.mixins import UserPassesTestMixin

# class AdminRequiredMixin(UserPassesTestMixin):
#     def test_func(self):
#         return self.request.user.is_admin
    
#     def handle_no_permission(self):
#         return redirect('home')

# class TaskDeleteView(AdminRequiredMixin, DeleteView):
#     model = Task
#     success_url = reverse_lazy('task-list')

# class ProjectDeleteView(AdminRequiredMixin, DeleteView):
#     model = Project
#     success_url = reverse_lazy('project-list')