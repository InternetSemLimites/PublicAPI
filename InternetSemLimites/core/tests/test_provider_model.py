from django.test import TestCase
from InternetSemLimites.core.models import Provider, State


class TestProviderModel(TestCase):

    def setUp(self):
        sc = State.objects.get(abbr='SC')
        go = State.objects.get(abbr='GO')
        props = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'category': Provider.FAME,
                 'other': 'Lorem ipsum'}
        self.provider = Provider.objects.create(**props)
        self.provider.coverage = [sc, go]

    def test_create(self):
        self.assertTrue(Provider.objects.exists())

    def test_published_is_false_by_default(self):
        self.assertFalse(self.provider.published)
