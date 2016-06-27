from django.test import TestCase
from django.contrib.admin.sites import AdminSite
from InternetSemLimites.core.admin import ProviderModelAdmin
from InternetSemLimites.core.models import Provider, State


class TestProviderModelAdmin(TestCase):

    def setUp(self):
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')
        props = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'category': Provider.FAME,
                 'other': 'Lorem ipsum'}
        self.provider = Provider.objects.create(**props)
        self.provider.coverage = [sc, go]
        self.model_admin = ProviderModelAdmin(Provider, AdminSite())

    def test_states(self):
        self.assertEqual('GO, SC', self.model_admin.states(self.provider))
