# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-21 20:19
from __future__ import unicode_literals

from django.db import migrations

REPEATED = 'R'
NOT_FOUND = 'N'
IMPRECISE = 'I'
NOT_ACCESSIBLE = 'A'
PRIVATE = 'P'
OTHER = 'O'
REASONS = ((REPEATED, 'Provedor repetido'),
           (NOT_FOUND, 'Fonte não encontrada (404)'),
           (IMPRECISE, 'Fonte com informações imprecisas ou erradas'),
           (NOT_ACCESSIBLE, 'Fonte não acessível (ex.: requer login)'),
           (PRIVATE, 'Fonte é comunicação privada (ex.: chat ou suporte)'),
           (OTHER, 'Outros'))
REASONS_DICT = dict(REASONS)


def set_reason(apps, schema_editor):
    Provider = apps.get_model('core', 'Provider')
    for provider in Provider.objects.exclude(moderation=''):
        reason = provider.moderation.lower()
        if ('não adesão' in reason or 'fonte não' in reason or 'errada' in reason):
            provider.moderation_reason = 'I'
        elif ('facebook' in reason or 'inacessível' in reason):
            provider.moderation_reason = 'A'
        elif ('chat' in reason or 'suporte' in reason):
            provider.moderation_reason = 'P'
        elif ('repetid' in reason):
            provider.moderation_reason = 'R'
        else:
            provider.moderation_reason = 'O'
            provider.moderation_comments = provider.moderation
        provider.save()


def set_moderation(apps, schema_editor):
    Provider = apps.get_model('core', 'Provider')
    for provider in Provider.objects.exclude(moderation_reason=''):
        standardized_reason = REASONS_DICT.get(provider.moderation_reason, '')
        moderation = f'{provider.moderation_comments} {standardized_reason}'
        provider.moderation = moderation
        provider.save()


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_auto_20160421_1718'),
    ]

    operations = [
        migrations.RunPython(set_reason, set_moderation),
    ]
