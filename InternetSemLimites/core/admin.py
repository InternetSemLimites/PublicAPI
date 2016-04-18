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
        if count < 2:
            msg = '{} provedores publicados.'
        else:
            msg = '{} provedor publicado.'
        self.message_user(request, msg.format(count))

    publish.short_description = 'Publicar'

    def refuse(self, request, queryset):
        count = queryset.update(status=Provider.REFUSED)
        if count < 2:
            msg = '{} provedores tirados do ar.'
        else:
            msg = '{} provedor tirado do ar.'
        self.message_user(request, msg.format(count))

    refuse.short_description = 'Tirar do ar'

    def unpublish(self, request, queryset):
        count = queryset.update(status=Provider.DISCUSSION)
        if count < 2:
            msg = '{} provedores recolocados em discussão.'
        else:
            msg = '{} provedor recolocado em discussão.'
        self.message_user(request, msg.format(count))

    unpublish.short_description = 'Voltar para discussão'

    def shame(self, request, queryset):
        count = queryset.update(category=Provider.SHAME)
        if count < 2:
            msg = '{} provedores incluídos no Hall of Shame.'
        else:
            msg = '{} provedor incluído no Hall of Shame.'
        self.message_user(request, msg.format(count))

    shame.short_description = 'Incluir no Hall of Shame'

    def fame(self, request, queryset):
        count = queryset.update(category=Provider.FAME)
        if count < 2:
            msg = '{} provedores incluídos no Hall of Fame.'
        else:
            msg = '{} provedor incluído no Hall of Fame.'
        self.message_user(request, msg.format(count))

    fame.short_description = 'Incluir no Hall of Fame'



admin.site.register(Provider, ProviderModelAdmin)
