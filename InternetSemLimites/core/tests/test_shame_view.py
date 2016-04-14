from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.models import Provider, State


class TestGet(TestCase):

    def setUp(self):
        sc = State.objects.get(abbr='SC')
        go = State.objects.get(abbr='GO')
        props = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'category': Provider.SHAME,
                 'other': 'Lorem ipsum',
                 'published': True}
        provider = Provider.objects.create(**props)
        provider.coverage = [sc, go]
        self.resp = self.client.get(resolve_url('shame'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        shame = json_resp['providers']
        with self.subTest():
            self.assertEqual(1, len(shame))
            self.assertNotIn('fame', json_resp)
            self.assertIn('headers', json_resp)
            self.assertEqual('Xpto', shame[0]['name'])
            self.assertEqual('http://xp.to', shame[0]['url'])
            self.assertEqual('http://twitter.com/xpto', shame[0]['source'])
            self.assertEqual(['GO', 'SC'], shame[0]['coverage'])
            self.assertEqual('S', shame[0]['category'])
            self.assertEqual('Lorem ipsum', shame[0]['other'])
