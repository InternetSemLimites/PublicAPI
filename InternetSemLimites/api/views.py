from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from InternetSemLimites.core.models import Provider, State


def home(request):
    fame = _serialize(Provider.objects.fame())
    shame = _serialize(Provider.objects.shame())
    return _to_json(fame, shame)


def fame(request):
    providers = _serialize(Provider.objects.fame())
    return _to_json(providers)


def shame(request):
    providers = _serialize(Provider.objects.shame())
    return _to_json(providers)


def by_state(request, abbr):
    state = get_object_or_404(State, abbr=abbr.upper())
    fame = _serialize(state.provider_set.fame())
    shame = _serialize(state.provider_set.shame())
    return _to_json(fame, shame)


def fame_by_state(request, abbr):
    providers = _serialize(_providers_by_state(abbr).fame())
    return _to_json(providers)


def shame_by_state(request, abbr):
    providers = _serialize(_providers_by_state(abbr).shame())
    return _to_json(providers)


def _providers_by_state(abbr):
    state = get_object_or_404(State, abbr=abbr.upper())
    return state.provider_set


def _to_json(providers_or_fame, shame=None):
    if shame:
        ctx = {'hall-of-fame': list(providers_or_fame), 'hall-of-shame': list(shame)}
    else:
        ctx = {'providers': list(providers_or_fame)}
    return JsonResponse(ctx)


def _serialize(query):
    fields = [f.__str__().split('.')[-1] for f in Provider._meta.fields]
    fields.remove('id')
    fields.remove('status')
    for obj in query:
        output = {field: getattr(obj, field) for field in fields}
        output['coverage'] = obj.coverage_to_list
        output['category'] = obj.category_name
        yield output
