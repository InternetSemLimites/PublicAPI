from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.http import (JsonResponse, HttpResponseNotAllowed,
                         HttpResponseRedirect)
from django.shortcuts import get_object_or_404, resolve_url
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from InternetSemLimites.core.forms import ProviderForm
from InternetSemLimites.core.models import Provider, State


def home(request):
    fame = _serialize_query(Provider.objects.fame())
    shame = _serialize_query(Provider.objects.shame())
    return _to_json(fame, shame)


def fame(request):
    providers = _serialize_query(Provider.objects.fame())
    return _to_json(providers)


def shame(request):
    providers = _serialize_query(Provider.objects.shame())
    return _to_json(providers)


def by_state(request, abbr):
    state = get_object_or_404(State, abbr=abbr.upper())
    fame = _serialize_query(state.provider_set.fame())
    shame = _serialize_query(state.provider_set.shame())
    return _to_json(fame, shame)


def fame_by_state(request, abbr):
    providers = _serialize_query(_providers_by_state(abbr).fame())
    return _to_json(providers)


def shame_by_state(request, abbr):
    providers = _serialize_query(_providers_by_state(abbr).shame())
    return _to_json(providers)


def provider_detail(request, pk):
    provider = get_object_or_404(Provider, pk=pk)
    return JsonResponse({'provider': _serialize_object(provider)})


@csrf_exempt
def provider_new(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    form = ProviderForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'errors': form.errors})

    provider = form.save()
    _send_mail('+1 InternetSemLimites',
               settings.DEFAULT_FROM_EMAIL,
               list(_get_admin_emails()),
               'core/provider_email.txt',
               dict(provider=provider))

    return HttpResponseRedirect(resolve_url('api:provider', provider.pk))


def _providers_by_state(abbr):
    state = get_object_or_404(State, abbr=abbr.upper())
    return state.provider_set


def _to_json(providers_or_fame, shame=None):
    if shame:
        ctx = {'hall-of-fame': list(providers_or_fame),
               'hall-of-shame': list(shame)}
    else:
        ctx = {'providers': list(providers_or_fame)}
    return JsonResponse(ctx)


def _serialize_query(query):
    for obj in query:
        yield _serialize_object(obj)


def _serialize_object(obj):
    fields = [f.__str__().split('.')[-1] for f in Provider._meta.fields]
    fields.remove('id')
    fields.remove('status')
    output = {field: getattr(obj, field) for field in fields}
    output['coverage'] = obj.coverage_to_list
    output['category'] = obj.category_name
    return output


def _get_admin_emails():
    for user in User.objects.exclude(email=''):
        yield user.email


def _send_mail(subject, sender, to, template_name, context):
    body = render_to_string(template_name, context)
    mail.send_mail(subject, body, sender, to)
