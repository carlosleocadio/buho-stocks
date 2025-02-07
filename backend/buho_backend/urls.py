"""buho_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, register_converter, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from two_factor.urls import urlpatterns as tf_urls
from buho_backend.admin import AdminSiteOTPRequiredMixinRedirSetup
from buho_backend import path_converters
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# admin.site.__class__ = AdminSiteOTPRequired
admin.site.__class__ = AdminSiteOTPRequiredMixinRedirSetup

register_converter(path_converters.DateConverter, "date")

schema_view = get_schema_view(
    openapi.Info(
        title="Buho Backend API",
        default_version="v1",
        description="Backend docs",
        terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="GPL3 License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path("", include(tf_urls)),
    path("admin/", admin.site.urls),
    path("auth/", include("auth.urls"), name="authentication"),
    path(
        "api/v1/companies/<int:company_id>/shares/",
        include("shares_transactions.urls"),
        name="shares-transactions",
    ),
    path(
        "api/v1/companies/<int:company_id>/rights/",
        include("rights_transactions.urls"),
        name="rights-transactions",
    ),
    path(
        "api/v1/companies/<int:company_id>/dividends/",
        include("dividends_transactions.urls"),
        name="dividends-transactions",
    ),
    path(
        "api/v1/companies/<int:company_id>/stock-prices/",
        include("stock_prices.urls"),
        name="stocks-prices",
    ),
    path("api/v1/currencies/", include("currencies.urls.api")),
    path(
        "api/v1/exchange-rates/", include("exchange_rates.urls"), name="exchange_rates"
    ),
    path("api/v1/markets/", include("markets.urls.api")),
    path("api/v1/portfolios/", include("portfolios.urls"), name="portfolios"),
    path(
        "api/v1/portfolios/<int:portfolio_id>/messages/",
        include("log_messages.urls"),
        name="log-messages",
    ),
    path(
        "api/v1/portfolios/<int:portfolio_id>/companies/",
        include("companies.urls"),
        name="companies",
    ),
    path("api/v1/sectors/", include("sectors.urls.api")),
    path("api/v1/settings/", include("settings.urls")),
    path("api/v1/stats/", include("stats.urls")),
    path("api/v1/benchmarks/", include("benchmarks.urls.api")),
    path("admin-actions/benchmarks/", include("benchmarks.urls.admin")),
    path("admin-actions/currencies/", include("currencies.urls.admin")),
    path("admin-actions/markets/", include("markets.urls.admin")),
    path("admin-actions/sectors/", include("sectors.urls.admin")),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
