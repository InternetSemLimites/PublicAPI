from django.contrib import admin
from InternetSemLimites.core.models import Provider


class ProviderModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'states', 'status', 'category', 'created_at')
    actions = ['publish', 'unpublish', 'refuse', 'shame', 'fame']
    list_filter = ('status', 'created_at', 'category', 'coverage')
    search_fields = ('name',)

    def states(self, obj):
        states = (state.abbr for state in obj.coverage.all())
        return ', '.join(sorted(states))

    states.short_description = 'Cobertura'

    def publish(self, request, queryset):
        count = queryset.update(status=Provider.PUBLISHED)
        messages = ('{} provedor publicado.', '{} provedores publicados.')
        self._pluralized_message_user(request, count, *messages)

    publish.short_description = 'Publicar'

    def refuse(self, request, queryset):
        count = queryset.update(status=Provider.REFUSED)
        messages = ('{} provedor tirado do ar.',
                    '{} provedores tirados do ar.')
        self._pluralized_message_user(request, count, *messages)

    refuse.short_description = 'Tirar do ar'

    def unpublish(self, request, queryset):
        count = queryset.update(status=Provider.DISCUSSION)
        messages = ('{} provedor recolocado em discussão.',
                    '{} provedores recolocados em discussão.')
        self._pluralized_message_user(request, count, *messages)

    unpublish.short_description = 'Voltar para discussão'

    def shame(self, request, queryset):
        count = queryset.update(category=Provider.SHAME)
        messages = ('{} provedor incluído no Hall of Shame.',
                    '{} provedores incluídos no Hall of Shame.')
        self._pluralized_message_user(request, count, *messages)

    shame.short_description = 'Incluir no Hall of Shame'

    def fame(self, request, queryset):
        count = queryset.update(category=Provider.FAME)
        messages = ('{} provedor incluído no Hall of Fame.',
                    '{} provedores incluídos no Hall of Fame.')
        self._pluralized_message_user(request, count, *messages)

    fame.short_description = 'Incluir no Hall of Fame'

    def _pluralized_message_user(self, request, count, single, plural):
        message = single if count == 1 else plural
        self.message_user(request, message.format(count))


admin.site.register(Provider, ProviderModelAdmin)
