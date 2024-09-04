from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views import generic
from django.views import View

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
        context["reviews"] = ReviewRating.objects.filter(product=context['product'])
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
            queryset = queryset.filter(description__icontains=search_query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("search")
        return context


class SubmitReviewView(View):
    def post(self, request, product_id):
        url = request.META.get("HTTP_REFERER")
        try:
            review = ReviewRating.objects.get(
                user__id=request.user.id, product__id=product_id
            )
            form = ReviewForm(request.POST, instance=review)
            form.save()
            messages.success(request, "Thanks You! Your review has been updated")
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = form.save(commit=False)
                data.product = Product.objects.get(id=product_id)
                data.user = User.objects.get(id=request.user.id)
                data.save()
                messages.success(request, "Thank You! Your review has been submitted.")
                return redirect(url)
