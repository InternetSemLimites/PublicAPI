from django.db import models


class ProviderQueryset(models.QuerySet):

    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def fame(self):
        return self.published().filter(category=self.model.FAME)

    def shame(self):
        return self.published().filter(category=self.model.SHAME)

ProviderManager = models.Manager.from_queryset(ProviderQueryset)
