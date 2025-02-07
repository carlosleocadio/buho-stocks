import logging

from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from buho_backend.utils.token_utils import ExpiringTokenAuthentication
from currencies.models import Currency
from currencies.serializers import CurrencySerializer

logger = logging.getLogger("buho_backend")


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_id="Get currencies",
        operation_description="Get a list of currencies",
        tags=["Currencies"],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_id="Get currency details",
        operation_description="Get an existing currency",
        tags=["Currencies"],
    ),
)
class CurrencyViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing currency instances.
    """

    serializer_class = CurrencySerializer
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "currency_id"

    def get_queryset(self):
        logger.debug(Currency.objects.all())
        return Currency.objects.all()
