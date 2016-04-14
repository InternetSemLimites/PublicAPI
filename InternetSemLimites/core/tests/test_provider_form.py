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
        sc = State.objects.get(abbr='SC')
        go = State.objects.get(abbr='GO')
        valid = {'name': 'Xpto',
                 'url': 'http://xp.to',
                 'source': 'http://twitter.com/xpto',
                 'coverage': [sc.pk, go.pk],
                 'category': Provider.SHAME,
                 'other': 'Lorem ipsum',
                 'published': True}
        form = ProviderForm(dict(valid, **kwargs))
        form.is_valid()
        return form
