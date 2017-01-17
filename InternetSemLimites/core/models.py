import re
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
    CATEGORIES_DICT = dict(CATEGORIES)

    NEW = 'N'
    DISCUSSION = 'D'
    PUBLISHED = 'P'
    REFUSED = 'R'
    EDIT = 'E'
    OUTDATED = 'O'
    ARCHIVED = 'A'
    STATUS = ((NEW, 'Aguardando moderação'),
              (DISCUSSION, 'Em discussão'),
              (PUBLISHED, 'Publicado'),
              (REFUSED, 'Recusado'),
              (EDIT, 'Edição aguardando moderação'),
              (OUTDATED, 'Substituído por versão atualizada'),
              (ARCHIVED, 'Arquivado'))

    BLANK = ''
    REPEATED = 'R'
    NOT_FOUND = 'N'
    IMPRECISE = 'I'
    NOT_ACCESSIBLE = 'A'
    PRIVATE = 'P'
    OTHER = 'O'
    REASONS = ((BLANK, 'Não se aplica'),
               (REPEATED, 'Provedor repetido'),
               (NOT_FOUND, 'Fonte não encontrada (404)'),
               (IMPRECISE, 'Fonte com informações imprecisas ou erradas'),
               (NOT_ACCESSIBLE, 'Fonte não acessível (ex.: requer login)'),
               (PRIVATE, 'Fonte é comunicação privada (ex.: chat ou suporte)'),
               (OTHER, 'Outros'))

    category = models.CharField('Categoria', max_length=1, choices=CATEGORIES)
    name = models.CharField('Nome do provedor', max_length=128)
    url = models.URLField('URL do provedor')
    source = models.URLField('URL da fonte da informação')
    coverage = models.ManyToManyField(State, verbose_name='Cobertura')
    other = models.CharField('Observações', max_length=140, blank=True)

    edited_from = models.ForeignKey('self', null=True, blank=True)
    status = models.CharField('Status', max_length=1, choices=STATUS, default=NEW)
    moderation_reason = models.CharField('Motivo', max_length=1, choices=REASONS, blank=True, default=BLANK)
    moderation_comments = models.TextField('Comentários da moderação', blank=True)

    created_at = models.DateTimeField('Criado em', auto_now_add=True)
    updated_at = models.DateTimeField('Editado em', auto_now=True)

    objects = ProviderManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return resolve_url('provider', self.pk)

    def get_moderation_reason(self):
        return dict(self.REASONS).get(self.moderation_reason)

    def get_status(self):
        return dict(self.STATUS).get(self.status)

    @property
    def coverage_to_list(self):
        return [state.abbr for state in self.coverage.all()]

    @property
    def category_name(self):
        category = self.CATEGORIES_DICT.get(self.category)
        return re.sub(r' \([\w\sáã\/]*\)$', '', category)

    class Meta:
        verbose_name = 'provedor'
        verbose_name_plural = 'provedores'
        ordering = ['name']
