from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from tasks.models import Task, Project

User = get_user_model()

class TaskViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            is_admin=False
        )
        self.admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass'
        )
        self.project = Project.objects.create(
            name='Test Project',
            created_by=self.admin
        )
        self.task = Task.objects.create(
            title='Test Task',
            created_by=self.admin,
            project=self.project,
            due_date='2025-01-01',
            priority='medium',
            status='todo',
            assigned_to=self.user
        )

    # Task List View
    def test_task_list_view_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(reverse('task-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Task')

    # def test_task_list_view_as_user(self):
    #     self.client.login(username='testuser', password='testpass123')
    #     response = self.client.get(reverse('task-list'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, 'Test Task')

    # Task Creation
    def test_task_creation_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('task-create'), {
            'title': 'New Task',
            'description': 'Task details',
            'due_date': '2025-01-01',
            'priority': 'medium',
            'status': 'todo',
            'project': self.project.id,
            'assigned_to': self.user.id
        })
        self.assertRedirects(response, reverse('task-detail', args=[Task.objects.latest('id').id]))

    # Task Update
    def test_task_update_as_creator(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('task-update', args=[self.task.id]), {
            'title': 'Updated Task',
            'description': 'Updated details',
            'due_date': '2025-01-01',
            'priority': 'high',
            'status': 'in_progress',
            'project': self.project.id,
            'assigned_to': self.user.id
        })
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Task')
        self.assertRedirects(response, reverse('task-detail', args=[self.task.id]))

    # Task Deletion
    def test_task_delete_as_admin(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('task-list'))
        self.assertEqual(Task.objects.count(), 0)

    def test_task_delete_as_non_admin(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('task-delete', args=[self.task.id]))
        self.assertEqual(response.status_code, 403)
        

