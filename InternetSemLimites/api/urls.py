from django.urls import path, register_converter

from InternetSemLimites.api.views import (
    by_state,
    fame,
    fame_by_state,
    home,
    provider,
    provider_new,
    shame,
    shame_by_state
)


class StateConverter:
    regex = '[\w]{2}'

    def to_python(self, value):
        return value.lower()

    def to_url(self, value):
        return value


register_converter(StateConverter, 'state')


app_name = 'api'


urlpatterns = [
    path('', home, name='home'),
    path('fame/', fame, name='fame'),
    path('shame/', shame, name='shame'),
    path('<state:abbr>/', by_state, name='by_state'),
    path('<state:abbr>/fame/', fame_by_state, name='fame_by_state'),
    path('<state:abbr>/shame/', shame_by_state, name='shame_by_state'),
    path('provider/new/', provider_new, name='new'),
    path('provider/<int:pk>/', provider, name='provider'),
]
