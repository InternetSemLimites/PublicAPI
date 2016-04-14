from django.http import JsonResponse
from InternetSemLimites.core.models import Provider


def home(request):
    headers = {'category': '`F` for `Hall of Fame` or `S` for `Hall of Shame',
               'source': 'URL for the source of the info(use archive.is)',
               'coverage': 'List os states covered by this provider',
               'name': 'Name of the provider',
               'url': 'URL of the provider',
               'created_at': 'Dated the ISP info was submitted to our server',
               'other': 'General information (eg cities covered)'}
    providers = _serialize(Provider)
    return JsonResponse({'providers': list(providers), 'headers': headers})


def _serialize(model):
    fields = [field.__str__().split('.')[-1] for field in model._meta.fields]
    fields.remove('id')
    for obj in model.objects.all():
        if obj.published:
            output = {field: getattr(obj, field) for field in fields}
            output['coverage'] = [state.abbr for state in obj.coverage.all()]
            yield output
