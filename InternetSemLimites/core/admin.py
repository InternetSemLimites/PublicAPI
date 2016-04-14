from django.contrib import admin
from InternetSemLimites.core.models import Provider


class ProviderModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'states', 'published', 'category')
    actions = ['publish', 'unpublish', 'shame', 'fame']
    list_filter = ('published', 'created_at', 'category', 'coverage')

    def states(self, obj):
        states = (state.abbr for state in obj.coverage.all())
        return ', '.join(sorted(states))

    states.short_description = 'Cobertura'

    def publish(self, request, queryset):
        count = queryset.update(published=True)
        if count < 2:
            msg = '{} provedores publicados.'
        else:
            msg = '{} provedor publicado.'
        self.message_user(request, msg.format(count))

    publish.short_description = 'Publicar'

    def unpublish(self, request, queryset):
        count = queryset.update(published=False)
        if count < 2:
            msg = '{} provedores tirados do ar.'
        else:
            msg = '{} provedor tirado do ar.'
        self.message_user(request, msg.format(count))

    unpublish.short_description = 'Tirar do ar'

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
