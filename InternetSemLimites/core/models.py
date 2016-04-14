from django.db import models


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

    category = models.CharField('Categoria', max_length=1, choices=CATEGORIES)
    name = models.CharField('Nome do provedor', max_length=128)
    url = models.URLField('URL do provedor')
    source = models.URLField('URL da fonte da informação')
    coverage = models.ManyToManyField(State, verbose_name='Cobertura')
    other = models.CharField('Observações', max_length=140, blank=True)
    published = models.BooleanField('Publicado', default=False)
    created_at = models.DateTimeField('Criado em', auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Provedor'
        verbose_name_plural = 'Provedores'
