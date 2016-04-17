from django.conf.urls import url
from InternetSemLimites.markdown.views import fame, shame

urlpatterns = [
    url(r'^README.md$', fame, name='fame'),
    url(r'^HALL_OF_SHAME.md$', shame, name='shame'),
]
