from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.forms import ProviderForm
from InternetSemLimites.core.models import Provider, State


class TestGet(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('api:new'))

    def test_get(self):
        self.assertEqual(405, self.resp.status_code)


class TestPostValid(TestCase):

    def setUp(self):
        User.objects.create_superuser(username='two', password='', email='42@xp.to')
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')
        data = {'name': 'Xpto',
                'url': 'http://xp.to',
                'source': 'http://twitter.com/xpto',
                'coverage': [sc.pk, go.pk],
                'category': Provider.SHAME,
                'other': 'Lorem ipsum'}
        self.resp = self.client.post(resolve_url('api:new'), data)

    def test_post(self):
        self.assertRedirects(self.resp, resolve_url('api:provider', 1))

    def test_send_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save(self):
        self.assertTrue(Provider.objects.exists())


class TestPostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post(resolve_url('api:new'), dict())

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_dont_save(self):
        self.assertFalse(Provider.objects.exists())

    def test_has_errors_on_empty_form(self):
        json_resp = self.resp.json()
        self.assertTrue(json_resp['errors'])

    def test_has_errors_on_non_empty_form(self):
        invalid_data = {'name': 'Xpto', 'coverage': ['xp', 'to'], 'url': ''}
        resp = self.client.post(resolve_url('api:new'), invalid_data)
        json_resp = resp.json()
        errors = json_resp['errors']
        with self.subTest():
            self.assertEqual('Este campo é obrigatório.', errors['category'][0])
            self.assertEqual('Este campo é obrigatório.', errors['source'][0])
            self.assertEqual('Este campo é obrigatório.', errors['url'][0])
            self.assertIn('não é um valor válido para', errors['coverage'][0])
