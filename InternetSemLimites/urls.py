"""InternetSemLimites URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from InternetSemLimites.core.views import (
    hall_of_fame,
    hall_of_shame,
    home,
    provider_details,
    provider_new,
    readme,
    region,
    regional_fame,
    regional_shame
)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),
    url(r'^fame/$', hall_of_fame, name='fame'),
    url(r'^shame/$', hall_of_shame, name='shame'),
    url(r'^(?P<region>[\w]{2})/$', region, name='region'),
    url(r'^(?P<region>[\w]{2})/fame/$', regional_fame, name='regional_fame'),
    url(r'^(?P<region>[\w]{2})/shame/$', regional_shame, name='regional_shame'),
    url(r'^new/$', provider_new, name='new'),
    url(r'^provider/(?P<pk>[\d]+)/$', provider_details, name='provider'),
    url(r'^README.md/$', readme, name='readme'),
]
