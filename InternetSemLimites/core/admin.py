from django.contrib import admin
from import_export.resources import ModelResource
from import_export.admin import ImportExportModelAdmin

from InternetSemLimites.core.models import Provider


class ProviderResource(ModelResource):

    class Meta:
        model = Provider


class ProviderModelAdmin(ImportExportModelAdmin):
    resource_class = ProviderResource
    list_display = ('name', 'states', 'status', 'category', 'created_at', 'updated_at')
    actions = ['publish', 'unpublish', 'refuse', 'shame', 'fame']
    list_filter = ('status', 'moderation_reason', 'category', 'coverage', 'created_at', 'updated_at')
    search_fields = ('name',)

    def states(self, obj):
        states = (state.abbr for state in obj.coverage.all())
        return ', '.join(sorted(states))

    states.short_description = 'Cobertura'

    def publish(self, request, queryset):
        count = queryset.update(status=Provider.PUBLISHED)
        messages = (f'{count} provedor publicado.',
                    f'{count} provedores publicados.')
        self._pluralized_message_user(request, count, *messages)

    publish.short_description = 'Publicar'

    def refuse(self, request, queryset):
        count = queryset.update(status=Provider.REFUSED)
        messages = (f'{count} provedor tirado do ar.',
                    f'{count} provedores tirados do ar.')
        self._pluralized_message_user(request, count, *messages)

    refuse.short_description = 'Tirar do ar'

    def unpublish(self, request, queryset):
        count = queryset.update(status=Provider.DISCUSSION)
        messages = (f'{count} provedor recolocado em discussão.',
                    f'{count} provedores recolocados em discussão.')
        self._pluralized_message_user(request, count, *messages)

    unpublish.short_description = 'Voltar para discussão'

    def shame(self, request, queryset):
        count = queryset.update(category=Provider.SHAME)
        messages = (f'{count} provedor incluído no Hall of Shame.',
                    f'{count} provedores incluídos no Hall of Shame.')
        self._pluralized_message_user(request, count, *messages)

    shame.short_description = 'Incluir no Hall of Shame'

    def fame(self, request, queryset):
        count = queryset.update(category=Provider.FAME)
        messages = (f'{count} provedor incluído no Hall of Fame.',
                    f'{count} provedores incluídos no Hall of Fame.')
        self._pluralized_message_user(request, count, *messages)

    fame.short_description = 'Incluir no Hall of Fame'

    def _pluralized_message_user(self, request, count, single, plural):
        message = single if count == 1 else plural
        self.message_user(request, message)

    def save_model(self, request, obj, form, change):

        # Change original provider status if edition is accepted
        if 'status' in form.changed_data and obj.edited_from:
            if obj.status == Provider.PUBLISHED:
                obj.edited_from.status = Provider.OUTDATED
                obj.edited_from.save()

        return super().save_model(request, obj, form, change)


admin.site.register(Provider, ProviderModelAdmin)
