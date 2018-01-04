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
                 'status': Provider.REFUSED,
                 'moderation_reason': Provider.REPEATED}
        provider = Provider.objects.create(**props)
        provider.coverage.set([sc, go])
        self.resp = self.client.get(resolve_url('provider', 1))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/provider_detail.html')

    def test_html(self):
        data = ('Xpto', 'xp.to', 'twitter', 'Hall of Fame', 'Lorem', 'Goiás',
                'Status', 'Recusado', 'Provedor repetido')
        with self.subTest():
            for expected in data:
                self.assertContains(self.resp, expected)
