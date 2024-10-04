import django_filters
from django_filters import FilterSet
from django.forms import DateTimeInput

from .models import Post


class PostFilter(FilterSet):
    after_add = django_filters.DateTimeFilter(
        field_name=('add_time'),
        lookup_expr=('gt'),
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'}
        )
    )

    class Meta:
        model = Post
        fields = {
            'heading': ['icontains'],
            'category': ['exact']
        }
