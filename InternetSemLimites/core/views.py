from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import DetailView
from InternetSemLimites.core.forms import ProviderForm
from InternetSemLimites.core.mixins import EmailCreateView
from InternetSemLimites.core.models import Provider, State

HEADERS = {'category': '`F` for `Hall of Fame` or `S` for `Hall of Shame',
           'source': 'URL for the source of the info(use archive.is)',
           'coverage': 'List os states covered by this provider',
           'name': 'Name of the provider',
           'url': 'URL of the provider',
           'created_at': 'Dated the ISP info was submitted to our server',
           'other': 'General information (eg cities covered)'}

provider_new = EmailCreateView.as_view(model=Provider, form_class=ProviderForm,
                                       email_subject='+1 InternetSemLimites')

provider_details = DetailView.as_view(model=Provider)


def home(request):
    fame = _serialize(Provider.objects.fame())
    shame = _serialize(Provider.objects.shame())
    return JsonResponse({'hall-of-fame': list(fame),
                         'hall-of-shame': list(shame),
                         'headers': HEADERS})


def hall_of_fame(request):
    providers = _serialize(Provider.objects.fame())
    return JsonResponse({'providers': list(providers),
                         'headers': HEADERS})


def hall_of_shame(request):
    providers = _serialize(Provider.objects.shame())
    return JsonResponse({'providers': list(providers),
                         'headers': HEADERS})


def region(request, abbr):
    state = get_object_or_404(State, abbr=abbr.upper())
    fame = _serialize(state.provider_set.fame())
    shame = _serialize(state.provider_set.shame())
    return JsonResponse({'hall-of-fame': list(fame),
                         'hall-of-shame': list(shame),
                         'headers': HEADERS})


def regional_fame(request, abbr):
    state = get_object_or_404(State, abbr=abbr.upper())
    providers = _serialize(state.provider_set.fame())
    return JsonResponse({'providers': list(providers),
                         'headers': HEADERS})


def regional_shame(request, abbr):
    state = get_object_or_404(State, abbr=abbr.upper())
    providers = _serialize(state.provider_set.shame())
    return JsonResponse({'providers': list(providers),
                         'headers': HEADERS})


def readme(request):
    states = State.objects.exclude(provider=None)
    ctx = [(state.name, list(state.provider_set.fame())) for state in states]
    return render(request, 'core/readme.md', {'states': ctx},
                  content_type='text/markdown; charset=UTF-8')


def hall_of_shame_md(request):
    ctx = Provider.objects.shame()
    return render(request, 'core/hall_of_shame.md', dict(providers=ctx),
                  content_type='text/markdown; charset=UTF-8')


def _serialize(query):
    fields = [f.__str__().split('.')[-1] for f in Provider._meta.fields]
    fields.remove('id')
    for obj in query:
        output = {field: getattr(obj, field) for field in fields}
        output['coverage'] = obj.coverage_to_list
        yield output
