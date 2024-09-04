from django.contrib import admin, messages
from django.utils.translation import ngettext
from django.utils.translation import gettext_lazy as _

from .models import Product, Category, ReviewRating

class PriceFilter(admin.SimpleListFilter):
    title = _("price")
    parameter_name = "price"

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return [
            ("Rs.1000", _("more than 1000")),
            ("Rs.2000", _("more than 2000")),
            ("Rs.5000", _("more than 5000")),
            ("Rs.10000", _("more than 10000")),
            ("Rs.20000", _("more than 20000")),
        ]

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == "Rs.1000":
            return queryset.filter(price__gte=1000.00)
        if self.value() == "Rs.2000":
            return queryset.filter(price__gte=2000.00)
        if self.value() == "Rs.5000":
            return queryset.filter(price__gte=5000.00)
        if self.value() == "Rs.10000":
            return queryset.filter(price__gte=10000.00)
        if self.value() == "Rs.20000":
            return queryset.filter(price__gte=20000.00)

class RatingFilter(admin.SimpleListFilter):
    title = _("rating")
    parameter_name = "rating"

    def lookups(self, request, model_admin):
        return [
            ("less-than-1", _("<1")),
            ("greater-than-1", _(">1")),
            ("greater-than-2", _(">2")),
            ("greater-than-3", _(">3")),
            ("greater-than-4", _(">4")),
            ("equal-to-5", _("=5")),
        ]

    def queryset(self, request, queryset):
        if self.value() == "less-than-1":
            return queryset.filter(rating__lte=1.0)
        if self.value() == "greater-than-1":
            return queryset.filter(rating__gte=1.0)
        if self.value() == "greater-than-2":
            return queryset.filter(rating__gte=2.0)
        if self.value() == "greater-than-3":
            return queryset.filter(rating__gte=3.0)
        if self.value() == "greater-than-4":
            return queryset.filter(rating__gte=4.0)
        if self.value() == "equal-to-5":
            return queryset.filter(rating=5.0)

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "stock"]
    ordering = ["name"]
    actions = ["make_out_of_stock"]
    list_filter = [PriceFilter]

    @admin.action(description="Mark selected products as out of stock")
    def make_out_of_stock(self, request, queryset):
        updated = queryset.update(stock=0)
        self.message_user(
            request,
            ngettext(
                "%d product stock was successfully set to 0",
                "%d products stocks were successfully set to 0",
                updated,
            )
            %updated,
            messages.SUCCESS,
        )

class ReviewRatingAdmin(admin.ModelAdmin):
    list_filter = [RatingFilter]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(ReviewRating, ReviewRatingAdmin)
