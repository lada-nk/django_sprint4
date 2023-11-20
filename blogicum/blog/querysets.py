from datetime import datetime

from django.db import models
from django.db.models import Count


class DatePubQuerySet(models.query.QuerySet):

    def date_pub_filter(self):
        return self.filter(
            pub_date__lte=datetime.now(),
            is_published=True,
            category__is_published=True
        )

    def comm_count(self):
        return self.annotate(
            comment_count=Count('comments')).order_by('-pub_date')
