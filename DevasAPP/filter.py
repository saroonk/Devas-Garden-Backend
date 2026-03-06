import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):

    availability = django_filters.CharFilter(method="filter_availability")
    price = django_filters.CharFilter(method="filter_price")

    sort = django_filters.CharFilter(method="filter_sort")

    class Meta:
        model = Product
        fields = []

    def filter_availability(self, queryset, name, value):
        if value == "in-stock":
            return queryset.filter(stock__gt=0)
        elif value == "out-of-stock":
            return queryset.filter(stock=0)
        return queryset

    def filter_price(self, queryset, name, value):
        if value == "0-500":
            return queryset.filter(new_price__lte=500)
        elif value == "500-1000":
            return queryset.filter(new_price__gte=500, new_price__lte=1000)
        elif value == "1000+":
            return queryset.filter(new_price__gte=1000)
        return queryset

    def filter_sort(self, queryset, name, value):

        if value == "price-asc":
            return queryset.order_by("new_price")

        elif value == "price-desc":
            return queryset.order_by("-new_price")

        elif value == "newest":
            return queryset.order_by("-created_at")

        elif value == "oldest":
            return queryset.order_by("created_at")

        return queryset