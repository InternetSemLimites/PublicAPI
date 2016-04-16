from django.db import models
from django.shortcuts import resolve_url
from InternetSemLimites.core.managers import ProviderManager


class State(models.Model):
    name = models.CharField('Nome', max_length=128)
    abbr = models.CharField('Sigla', max_length=2)

    def __str__(self):
        return '{} ({})'.format(self.name, self.abbr)

    class Meta:
        ordering = ['name']


class Provider(models.Model):

    FAME = 'F'
    SHAME = 'S'
    CATEGORIES = ((FAME, 'Hall of Fame (não utilizará limites/fraquia)'),
                  (SHAME, 'Hall of Shame (utilizará limites/franquia)'))

    NEW = 'N'
    DISCUSSION = 'D'
    PUBLISHED = 'P'
    REFUSED = 'R'
    STATUS = ((NEW, 'Aguardando moderação'),
              (DISCUSSION, 'Em discussão'),
              (PUBLISHED, 'Publicado'),
              (REFUSED, 'Recusado'))

    category = models.CharField('Categoria', max_length=1, choices=CATEGORIES)
    name = models.CharField('Nome do provedor', max_length=128)
    url = models.URLField('URL do provedor')
    source = models.URLField('URL da fonte da informação')
    coverage = models.ManyToManyField(State, verbose_name='Cobertura')
    other = models.CharField('Observações', max_length=140, blank=True)
    status = models.CharField('Status', max_length=1, choices=STATUS, default=NEW)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    moderation = models.TextField('Comentários da moderação', blank=True)

    objects = ProviderManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return resolve_url('provider', self.pk)

    @property
    def coverage_to_list(self):
        return [state.abbr for state in self.coverage.all()]

    class Meta:
        verbose_name = 'provedor'
        verbose_name_plural = 'provedores'
        ordering = ['name']
