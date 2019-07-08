from django.test import Client, TestCase

from django.urls import reverse

from .views import IdeaListView

class IdeaViewTests(TestCase):
    def test_idea_list_view_200(self):
        client = Client()
        response = client.get(reverse('ideas:list'))
        self.assertIs(response.status_code, 200)

    def test_idea_list_view_html(self):
        client = Client()
        response = client.get(reverse('ideas:list'))
        self.assertIn('text/html', response._headers['content-type'][1])

    def test_idea_create_view_200(self):
        client = Client()
        response = client.get(reverse('ideas:create'))
        self.assertIs(response.status_code, 200)

    def test_idea_list_create_html(self):
        client = Client()
        response = client.get(reverse('ideas:create'))
        self.assertIn('text/html', response._headers['content-type'][1])

    def test_idea_list_view_only_queries_its_own_comments(self):
        # Need to get the context being passed and check against Comments.objects.filter() self
        pass
