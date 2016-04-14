from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.models import Provider, State


class TestGet(TestCase):

    def setUp(self):
        sc = State.objects.create(name='Santa Catarina', abbr='SC')
        go = State.objects.create(name='Goiás', abbr='GO')
        props = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'category': Provider.FAME,
                 'other': 'Lorem ipsum',
                 'published': True}
        provider = Provider.objects.create(**props)
        provider.coverage = [sc, go]
        self.resp = self.client.get(resolve_url('home'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        providers = json_resp['providers']
        with self.subTest():
            self.assertEqual('Xpto', providers[0]['name'])
            self.assertEqual('http://xp.to', providers[0]['url'])
            self.assertEqual('http://twitter.com/xpto', providers[0]['source'])
            self.assertEqual(['GO', 'SC'], providers[0]['coverage'])
            self.assertEqual('F', providers[0]['category'])
            self.assertEqual('Lorem ipsum', providers[0]['other'])
