from django.urls import path

from InternetSemLimites.markdown.views import fame, shame


app_name = 'markdown'


urlpatterns = [
    path('README.md', fame, name='fame'),
    path('HALL_OF_SHAME.md', shame, name='shame'),
]
