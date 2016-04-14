from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.forms import ProviderForm
from InternetSemLimites.core.models import Provider, State


class TestGet(TestCase):

    def setUp(self):
        self.resp = self.client.get(resolve_url('new'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('text/html', self.resp['Content-Type'][0:9])

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/provider_form.html')

    def test_contents(self):
        tags = (('<form', 1),
                ('<input', 32),
                ('<select ', 1),
                ('type="text"', 2),
                ('type="url"', 2))
        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_csrf(self):
        self.assertContains(self.resp, 'csrfmiddlewaretoken')

    def test_has_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, ProviderForm)


class TestPostValid(TestCase):

    def setUp(self):
        User.objects.create_superuser(username='two', password='', email='42@xp.to')
        sc = State.objects.get(abbr='SC')
        go = State.objects.get(abbr='GO')
        data = {'name': 'Xpto',
                'url': 'http://xp.to',
                'source': 'http://twitter.com/xpto',
                'coverage': [sc.pk, go.pk],
                'category': Provider.SHAME,
                'other': 'Lorem ipsum'}
        self.resp = self.client.post(resolve_url('new'), data)

    def test_post(self):
        self.assertRedirects(self.resp, resolve_url('provider', 1))

    def test_send_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_save(self):
        self.assertTrue(Provider.objects.exists())


class TestPostInvalid(TestCase):

    def setUp(self):
        self.resp = self.client.post(resolve_url('new'), dict())
        self.form = self.resp.context['form']

    def test_post(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/provider_form.html')

    def test_has_form(self):
        self.assertIsInstance(self.form, ProviderForm)

    def test_has_errors(self):
        self.assertTrue(self.form.errors)

    def test_dont_save(self):
        self.assertFalse(Provider.objects.exists())


class TemplateRegressionTest(TestCase):

    def test_template_has_form_errors(self):
        invalid_data = {'name': 'Xpto', 'coverage': ['xp', 'to'], 'url': ''}
        resp = self.client.post(resolve_url('new'), invalid_data)
        self.assertContains(resp, 'campo é obrigatório', 3)
