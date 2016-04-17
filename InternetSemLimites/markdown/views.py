from django.shortcuts import render
from django.http import HttpResponse
from InternetSemLimites.core.models import Provider, State


def fame(request):
    ctx = {'states': _fame_listed_by_states()}
    return _render_md(request, 'fame', ctx)


def shame(request):
    ctx = {'providers': Provider.objects.shame()}
    return _render_md(request, 'shame', ctx)


def _render_md(request, template, ctx):
    template = 'markdown/{}.md'.format(template)
    return render(request, template, ctx,
                  content_type='text/markdown; charset=UTF-8')


def _fame_listed_by_states():
    for state in State.objects.exclude(provider=None):
        yield (state.name, list(state.provider_set.fame()))
