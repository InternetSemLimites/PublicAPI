from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.models import Provider, State


class TestGet(TestCase):

    def setUp(self):
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')
        props = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'category': Provider.FAME,
                 'other': 'Lorem ipsum',
                 'status': Provider.PUBLISHED}
        provider = Provider.objects.create(**props)
        provider.coverage.set([sc, go])
        self.resp = self.client.get(resolve_url('api:home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        fame = json_resp['hall-of-fame']
        shame = json_resp['hall-of-shame']
        with self.subTest():
            self.assertEqual(1, len(fame))
            self.assertEqual(0, len(shame))
            self.assertEqual('Xpto', fame[0]['name'])
            self.assertEqual('http://xp.to', fame[0]['url'])
            self.assertEqual('http://twitter.com/xpto', fame[0]['source'])
            self.assertEqual(['GO', 'SC'], fame[0]['coverage'])
            self.assertEqual('Hall of Fame', fame[0]['category'])
            self.assertEqual('Lorem ipsum', fame[0]['other'])
