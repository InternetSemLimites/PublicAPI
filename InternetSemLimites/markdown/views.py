from django.shortcuts import render
from InternetSemLimites.core.models import Provider, State


def fame(request):
    ctx = {'states': _fame_listed_by_states()}
    return _render_md(request, 'fame', ctx)


def shame(request):
    ctx = {'providers': Provider.objects.shame()}
    return _render_md(request, 'shame', ctx)


def _render_md(request, template, ctx):
    template_path = f'markdown/{template}.md'
    return render(request, template_path, ctx,
                  content_type='text/markdown; charset=UTF-8')


def _fame_listed_by_states():
    for state in State.objects.exclude(provider=None):
        providers = list(state.provider_set.fame())
        if providers:
            yield (state.name, providers)
