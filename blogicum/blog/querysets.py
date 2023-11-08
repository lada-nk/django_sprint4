from datetime import datetime

from django.db import models


class PublishedQuerySet(models.query.QuerySet):

    def custom_filter(self):
        """Общие для всех постов фильтры."""
        return self.filter(
            is_published=True,
            pub_date__lte=datetime.now(),
            category__is_published=True
        )
