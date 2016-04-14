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
                 'category': Provider.FAME,
                 'other': 'Lorem ipsum',
                 'published': True}
        provider = Provider.objects.create(**props)
        provider.coverage = [sc, go]
        self.resp = self.client.get(resolve_url('provider', 1))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/provider_detail.html')

    def test_html(self):
        data = ('Xpto', 'xp.to', 'twitter', 'Hall of Fame', 'Lorem', 'Goiás')
        with self.subTest():
            for expected in data:
                self.assertContains(self.resp, expected)
