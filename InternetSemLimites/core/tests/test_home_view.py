from django.shortcuts import resolve_url
from django.test import TestCase


class TestGet(TestCase):

    def test_redirect(self):
        resp = self.client.get(resolve_url('home'))
        self.assertRedirects(resp, '/api/')
