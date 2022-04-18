from django_filters import rest_framework as filters

from reviews.models import Title


class CharInFilter(filters.BaseInFilter, filters.CharFilter):
    """Filters in"""

    pass


class TitleFilter(filters.FilterSet):
    """Defines search"""

    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    year = filters.NumberFilter()
    category = filters.CharFilter(
        field_name="category__slug", lookup_expr="exact"
    )
    genre = CharInFilter(field_name="genre__slug", lookup_expr="in")

    class Meta:
        models = Title
        fields = ["category", "year", "name", "genre"]
