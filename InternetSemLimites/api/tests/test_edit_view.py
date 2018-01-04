from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.forms import ProviderForm
from InternetSemLimites.core.models import Provider, State


class TestPostValid(TestCase):

    def setUp(self):
        User.objects.create_superuser(username='two', password='', email='42@xp.to')
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')

        self.provider = Provider.objects.create(
            name='Xpto',
            url='http://xp.to',
            source='http://twitter.com/xpto',
            category=Provider.SHAME,
            other='Lorem ipsum'
        )
        self.provider.coverage.add(sc)
        self.provider.coverage.add(go)

        self.data = {
            'name': 'XptoEdited',
            'url': 'http://xpedited.to',
            'source': 'http://twitter.com/xptoedited',
            'coverage': [sc.pk],
            'category': Provider.FAME,
            'other': 'Lorem ipsum dolor'
        }
        self.resp = self.client.post(resolve_url('api:provider', self.provider.pk), self.data)
        self.edited_provider = Provider.objects.last()

    def test_not_allowed_methods(self):
        url = resolve_url('api:provider', self.provider.pk)
        for r in (self.client.delete(url), self.client.patch(url, self.data)):
            with self.subTest():
                self.assertEqual(405, r.status_code)

    def test_post(self):
        self.assertRedirects(self.resp, resolve_url('api:provider', self.edited_provider.pk))

    def test_send_email(self):
        self.assertEqual(1, len(mail.outbox))

    def test_edit(self):

        edited_provider_coverage_ids = [state.id for state in self.edited_provider.coverage.all()]

        self.assertEqual(self.edited_provider.name, self.data['name'])
        self.assertEqual(self.edited_provider.url, self.data['url'])
        self.assertEqual(self.edited_provider.source, self.data['source'])
        self.assertEqual(self.edited_provider.category, self.data['category'])
        self.assertEqual(self.edited_provider.other, self.data['other'])
        self.assertEqual(edited_provider_coverage_ids, self.data['coverage'])


class TestPostInvalid(TestCase):

    def setUp(self):

        User.objects.create_superuser(username='two', password='', email='42@xp.to')
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')

        self.provider = Provider.objects.create(
            name='Xpto',
            url='http://xp.to',
            source='http://twitter.com/xpto',
            category=Provider.SHAME,
            other='Lorem ipsum'
        )
        self.provider.coverage.add(sc)
        self.provider.coverage.add(go)

        self.resp = self.client.post(resolve_url('api:provider', self.provider.pk), dict())

    def test_post(self):
        self.assertEqual(422, self.resp.status_code)

    def test_has_errors_on_empty_form(self):
        json_resp = self.resp.json()
        self.assertTrue(json_resp['errors'])

    def test_has_errors_on_non_empty_form(self):
        invalid_data = {'name': 'Xpto', 'coverage': ['xp', 'to'], 'url': ''}
        resp = self.client.post(resolve_url('api:provider', self.provider.pk), invalid_data)
        json_resp = resp.json()
        errors = json_resp['errors']
        with self.subTest():
            self.assertEqual('Este campo é obrigatório.', errors['category'][0])
            self.assertEqual('Este campo é obrigatório.', errors['source'][0])
            self.assertEqual('Este campo é obrigatório.', errors['url'][0])
            self.assertIn('não é um valor válido', errors['coverage'][0])
