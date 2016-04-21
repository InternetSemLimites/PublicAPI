from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.views.generic import DetailView
from InternetSemLimites.core.forms import ProviderForm
from InternetSemLimites.core.mixins import EmailAdminCreateView
from InternetSemLimites.core.models import Provider

provider_new_args = {'model': Provider,
                     'form_class': ProviderForm,
                     'email_subject': '+1 InternetSemLimites'}

provider_new = EmailAdminCreateView.as_view(**provider_new_args)
provider_details = DetailView.as_view(model=Provider)


def redirect_to_api(request):
    return HttpResponseRedirect(resolve_url('api:home'))
