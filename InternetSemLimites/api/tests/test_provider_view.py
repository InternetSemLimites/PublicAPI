from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.models import Provider, State


class TestGet(TestCase):

    def setUp(self):
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')
        sp, *_ = State.objects.get_or_create(abbr='SP', name='São Paulo')
        props = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'category': Provider.FAME,
                 'other': 'Lorem ipsum',
                 'status': Provider.REFUSED,
                 'moderation_reason': Provider.REPEATED}
        provider = Provider.objects.create(**props)
        provider.coverage.set([sc, go])
        self.resp = self.client.get(resolve_url('api:provider', 1))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('application/json', self.resp['Content-Type'])

    def test_contents(self):
        json_resp = self.resp.json()
        provider = json_resp['provider']
        with self.subTest():
            self.assertEqual('Xpto', provider['name'])
            self.assertEqual('http://xp.to', provider['url'])
            self.assertEqual('http://twitter.com/xpto', provider['source'])
            self.assertEqual(['GO', 'SC'], provider['coverage'])
            self.assertEqual('Hall of Fame', provider['category'])
            self.assertEqual('Lorem ipsum', provider['other'])
            self.assertEqual('Recusado', provider['status'])
            self.assertEqual('Provedor repetido', provider['moderation_reason'])

    def test_404(self):
        resp = self.client.get(resolve_url('api:provider', 42))
        self.assertEqual(404, resp.status_code)
