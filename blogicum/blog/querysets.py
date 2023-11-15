from datetime import datetime

from django.db import models


class DatePubQuerySet(models.query.QuerySet):

    def date_pub_filter(self):
        return self.filter(
            pub_date__lte=datetime.now(),
            is_published=True,
            category__is_published=True
        )
