from django.shortcuts import resolve_url
from django.test import TestCase
from InternetSemLimites.core.models import Provider, State


class TestGet(TestCase):

    def setUp(self):
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')
        sp, *_ = State.objects.get_or_create(abbr='GO', name='São Paulo')
        props_published = {'name': 'Xpto',
                           'url': 'http://xp.to',
                           'source': 'http://twitter.com/xpto',
                           'category': Provider.FAME,
                           'other': 'Lorem ipsum',
                           'status': Provider.PUBLISHED}
        props_refused= {'name': 'Xpto',
                        'url': 'http://xp.to',
                        'source': 'http://twitter.com/xpto',
                        'category': Provider.FAME,
                        'other': 'Lorem ipsum',
                        'status': Provider.REFUSED}
        provider_published = Provider.objects.create(**props_published)
        provider_refused = Provider.objects.create(**props_refused)
        provider_published.coverage = [sc, go]
        provider_refused.coverage = [sp]
        self.resp = self.client.get(resolve_url('markdown:fame'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_type(self):
        self.assertEqual('text/markdown; charset=UTF-8', self.resp['Content-Type'])

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'markdown/fame.md')

    def test_contents(self):
        contents = ['Xpto', 'Goiás', 'Lorem', 'http://xp.to', 'twitter.com']
        for content in contents:
            with self.subTest():
                self.assertContains(self.resp, content)
        self.assertNotContains(self.resp, 'São Paulo')
