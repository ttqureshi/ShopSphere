from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import generic
from django.views import View
from django.db.models import Q

from .models import Product, ReviewRating
from .forms import ReviewForm


class ProductsListingView(generic.ListView):
    model = Product
    template_name = "products/products_listing.html"
    context_object_name = "product_list"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category__name=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["selected_category"] = self.request.GET.get("category", "")
        return context


class ProductDetailView(generic.detail.DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["reviews"] = ReviewRating.objects.filter(product=context["product"])
        return context


class ProductSearchView(generic.ListView):
    model = Product
    template_name = "products/search.html"
    context_object_name = "search_results"
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get("search")
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) | Q(name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = self.request.GET.get("search", "")
        context["search_query"] = search_query
        context["no_results"] = self.get_queryset().count()
        context["selected_category"] = self.request.GET.get("category", "")
        return context


class SubmitReviewView(View):
    def post(self, request, product_id):
        url = request.META.get("HTTP_REFERER", "/")
        try:
            review = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thank you! Your review has been updated.")
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.product_id = product_id
                data.user = request.user
                data.save()
                messages.success(request, "Thank you! Your review has been submitted.")

        return redirect(url)
