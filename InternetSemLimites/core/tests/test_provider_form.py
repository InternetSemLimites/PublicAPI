from django.test import TestCase
from InternetSemLimites.core.forms import ProviderForm
from InternetSemLimites.core.models import Provider, State


class TestProviderForm(TestCase):

    def test_form_has_fields(self):
        form = ProviderForm()
        fields = ['category', 'name', 'url', 'source', 'coverage', 'other']
        self.assertSequenceEqual(list(form.fields), fields)

    def test_other_is_optional(self):
        form = self._valid_form(other='')
        self.assertFalse(form.errors)

    def test_valid_form(self):
        form = self._valid_form(other='')
        self.assertFalse(form.errors)

    def _valid_form(self, **kwargs):
        sc, *_ = State.objects.get_or_create(abbr='SC', name='Santa Catarina')
        go, *_ = State.objects.get_or_create(abbr='GO', name='Goiás')
        valid = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'coverage': [sc.pk, go.pk],
                 'category': Provider.SHAME,
                 'other': 'Lorem ipsum',
                 'status': Provider.PUBLISHED}
        form = ProviderForm(dict(valid, **kwargs))
        form.is_valid()
        return form
