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
    fame = _serialize(Provider.objects.filter(category=Provider.FAME))
    shame = _serialize(Provider.objects.filter(category=Provider.SHAME))
    return JsonResponse({'hall-of-fame': list(fame),
                         'hall-of-shame': list(shame),
                         'headers': HEADERS})


def hall_of(request, fame_or_shame):
    providers = _serialize(Provider.objects.filter(category=fame_or_shame))
    return JsonResponse({'providers': list(providers),
                         'headers': HEADERS})


def regional_hall_of(request, region, fame_or_shame):
    region = get_object_or_404(State, abbr=region.upper())
    fame = _serialize(region.provider_set.filter(category=fame_or_shame))
    return JsonResponse({'providers': list(fame),
                         'headers': HEADERS})


def hall_of_fame(request):
    return hall_of(request, Provider.FAME)


def hall_of_shame(request):
    return hall_of(request, Provider.SHAME)


def region(request, region):
    region = get_object_or_404(State, abbr=region.upper())
    fame = _serialize(region.provider_set.filter(category=Provider.FAME))
    shame = _serialize(region.provider_set.filter(category=Provider.SHAME))
    return JsonResponse({'hall-of-fame': list(fame),
                         'hall-of-shame': list(shame),
                         'headers': HEADERS})


def regional_fame(request, region):
    return regional_hall_of(request, region, Provider.FAME)


def regional_shame(request, region):
    return regional_hall_of(request, region, Provider.SHAME)


def readme(request):
    ctx = dict()
    for state in State.objects.all():
        providers = state.provider_set.filter(category=Provider.FAME,
                                              published=True)
        if providers:
            ctx[state.name] = list(providers)
    return render(request, 'core/readme.md', {'states': ctx},
                  content_type='text/markdown; charset=UTF-8')


def _serialize(query):
    fields = [f.__str__().split('.')[-1] for f in Provider._meta.fields]
    fields.remove('id')
    for obj in query:
        if obj.published:
            output = {field: getattr(obj, field) for field in fields}
            output['coverage'] = [state.abbr for state in obj.coverage.all()]
            yield output
