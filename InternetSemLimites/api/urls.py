from django.conf.urls import url
from InternetSemLimites.api.views import (by_state, fame, fame_by_state, home,
                                          provider_detail, provider_new, shame,
                                          shame_by_state)

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^fame/$', fame, name='fame'),
    url(r'^shame/$', shame, name='shame'),
    url(r'^(?P<abbr>[\w]{2})/$', by_state, name='by_state'),
    url(r'^(?P<abbr>[\w]{2})/fame/$', fame_by_state, name='fame_by_state'),
    url(r'^(?P<abbr>[\w]{2})/shame/$', shame_by_state, name='shame_by_state'),
    url(r'^provider/new/$', provider_new, name='new'),
    url(r'^provider/(?P<pk>[\d]+)/$', provider_detail, name='provider'),
]
