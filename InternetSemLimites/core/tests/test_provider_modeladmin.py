from unittest import skip
from unittest.mock import patch
from django.test import RequestFactory, TestCase
from django.contrib.admin.sites import AdminSite
from InternetSemLimites.core.admin import ProviderModelAdmin
from InternetSemLimites.core.models import Provider, State
from InternetSemLimites.core.forms import ProviderForm


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
        self.admin = ProviderModelAdmin(Provider, AdminSite())

    def test_states_field(self):
        self.assertEqual('GO, SC', self.admin.states(self.provider))

    @patch('InternetSemLimites.core.admin.ProviderModelAdmin.message_user')
    def test_publish_action(self, mock_message_user):
        self.admin.publish(RequestFactory(), Provider.objects.all())
        message = mock_message_user.call_args[0][1]
        self.assertEqual(1, Provider.objects.published().count())
        self.assertTrue('1 provedor publicado.', message)

    @patch('InternetSemLimites.core.admin.ProviderModelAdmin.message_user')
    def test_refuse(self, mock_message_user):
        self.admin.refuse(RequestFactory(), Provider.objects.all())
        total = Provider.objects.filter(status=Provider.REFUSED).count()
        message = mock_message_user.call_args[0][1]
        self.assertEqual(1, total)
        self.assertTrue('1 provedor tirado do ar.', message)

    @patch('InternetSemLimites.core.admin.ProviderModelAdmin.message_user')
    def test_unpublish(self, mock_message_user):
        self.admin.unpublish(RequestFactory(), Provider.objects.all())
        total = Provider.objects.filter(status=Provider.DISCUSSION).count()
        message = mock_message_user.call_args[0][1]
        self.assertEqual(1, total)
        self.assertTrue('1 provedor recolocado em discussão.', message)

    @patch('InternetSemLimites.core.admin.ProviderModelAdmin.message_user')
    def test_shame(self, mock_message_user):
        self.admin.shame(RequestFactory(), Provider.objects.all())
        total = Provider.objects.filter(category=Provider.SHAME).count()
        message = mock_message_user.call_args[0][1]
        self.assertEqual(1, total)
        self.assertTrue('1 provedor incluído no hall of shame.', message)

    @patch('InternetSemLimites.core.admin.ProviderModelAdmin.message_user')
    def test_fame(self, mock_message_user):
        self.provider.category = Provider.SHAME
        self.provider.save()
        self.admin.fame(RequestFactory(), Provider.objects.all())
        total = Provider.objects.filter(category=Provider.FAME).count()
        message = mock_message_user.call_args[0][1]
        self.assertEqual(1, total)
        self.assertTrue('1 provedor incluído no hall of shame.', message)

    def test_save_model(self):
        provider_edited = self.provider
        provider_edited.id = None
        provider_edited.save()

        self.provider.status = Provider.PUBLISHED
        self.provider.edited_from = provider_edited
        self.provider.save()

        form = ProviderForm()
        form.changed_data = ['status']

        self.admin.save_model(RequestFactory(), provider_edited, form, True)
        self.assertEqual(self.provider.status, Provider.OUTDATED)




