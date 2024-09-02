from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include('allauth.urls')),
    path('accounts/', include('allauth.socialaccount.urls')),
    path("", views.homepage, name="home"),
    path("users/", include("users.urls")),
    path("products/", include("products.urls")),
    path('api/products/', include('products.api.urls')),
    path('api/users/', include('users.api.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path('api-auth/', include('rest_framework.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)