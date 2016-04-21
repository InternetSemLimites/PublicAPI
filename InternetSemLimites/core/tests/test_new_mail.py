from django.contrib.auth.models import User
from django.core import mail
from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.models import Provider, State


class TestValidPost(TestCase):

    def setUp(self):
        User.objects.create_user(username='one', password='', email='x@p.to')
        User.objects.create_superuser(username='two', password='', email='42@xp.to')
        User.objects.create_superuser(username='three', password='', email='hell@ye.ah')
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')
        data = {'name': 'Xpto',
                'url': 'http://xp.to',
                'source': 'http://twitter.com/xpto',
                'coverage': [sc.pk, go.pk],
                'category': Provider.SHAME,
                'other': 'Lorem ipsum'}
        self.resp = self.client.post(resolve_url('new'), data)
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('+1 InternetSemLimites', self.email.subject)

    def test_email_from(self):
        self.assertEqual('noreply@internetsemlimites.herokuapp.com',
                         self.email.from_email)

    def test_email_to(self):
        self.assertEqual(['x@p.to', '42@xp.to', 'hell@ye.ah'], self.email.to)

    def test_email_body(self):
        contents = ['Xpto', 'SC', 'Lorem ipsum', 'http://xp.to', 'twitter.com']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
