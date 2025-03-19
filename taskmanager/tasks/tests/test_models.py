from django.test import TestCase
from django.core.exceptions import ValidationError
from ..models import Task, Project
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.project = Project.objects.create(name='Test Project', created_by=self.user)
        
    def test_task_creation(self):
        task = Task.objects.create(
            title='Test Task',
            created_by=self.user,
            project=self.project,
            due_date='2025-01-01',
            assigned_to=self.assignee,
        )
        self.assertEqual(str(task), 'Test Task')
        self.assertEqual(task.status, 'todo')

class ProjectModelTests(TestCase):
    def test_project_creation(self):
        user = User.objects.create_user(username='testuser', password='testpass')
        project = Project.objects.create(
            name='Test Project',
            created_by=user
        )
        self.assertEqual(str(project), 'Test Project')
        self.assertEqual(project.created_by, user)
