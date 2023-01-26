from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from todos.models import Todo


class TodoAPITestCase(APITestCase):
    def authenticate(self):
        user = {"email": "email@gmail.com", "password": "p@ssword!3"}
        self.client.post(reverse("register"), user)

        response = self.client.post(reverse("login"), user)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    def create_todo(self):
        sample_todo = {'title': "hello", "desc": "test"}
        response = self.client.post(reverse("todos"), sample_todo)
        return response


class TestListCreateTodos(TodoAPITestCase):

    def test_should_not_create_todo_with_no_auth(self):
        sample_todo = {'title': "hello", "desc": "test"}
        response = self.client.post(reverse("todos"), sample_todo)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_should_create_todo_with_auth(self):
        self.authenticate()
        previous_todo_count = Todo.objects.all().count()
        response = self.create_todo()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1)
        self.assertEqual(response.data['title'], 'hello')
        self.assertEqual(response.data['desc'], 'test')

    def test_to_retrieve_todos(self):
        self.authenticate()
        response = self.client.get(reverse("todos"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)
        sample_todo = {'title': "hello", "desc": "test"}
        self.client.post(reverse("todos"), sample_todo)

        res = self.client.get(reverse("todos"))
        self.assertIsInstance(res.data['count'], int)
        self.assertEqual(res.data['count'], 1)


class TestTodoDetailAPIView(TodoAPITestCase):
    def test_retrieve_one_item(self):
        self.authenticate()
        response = self.create_todo()

        res = self.client.get(reverse("todo", kwargs={'id': response.data['id']}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(todo.id, response.data['id'])

    def test_updates_one_item(self):
        self.authenticate()
        response = self.create_todo()

        res = self.client.patch(reverse("todo", kwargs={'id': response.data['id']}),
                                {"title": "New Todo", "is_complete": True})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        updated_todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(updated_todo.title, "New Todo")
        self.assertEqual(updated_todo.is_complete, True)

    def test_delete_one_item(self):
        self.authenticate()
        res = self.create_todo()
        previous_db_todo_count = Todo.objects.all().count()
        self.assertGreater(previous_db_todo_count, 0)
        self.assertEqual(previous_db_todo_count, 1)
        response = self.client.delete(reverse('todo', kwargs={'id': res.data['id']}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Todo.objects.all().count(), 0)