import logging

from django.utils.decorators import method_decorator
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, generics
from drf_yasg.utils import swagger_auto_schema
from buho_backend.utils.token_utils import ExpiringTokenAuthentication
from markets.serializers import MarketSerializer, TimezoneSerializer
from markets.models import Market, get_all_timezones

logger = logging.getLogger("buho_backend")


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_id="Get markets",
        operation_description="Get a list of markets",
        tags=["Markets"],
    ),
)
@method_decorator(
    name="retrieve",
    decorator=swagger_auto_schema(
        operation_id="Get market details",
        operation_description="Get an existing market",
        tags=["Markets"],
    ),
)
class MarketViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing market instances.
    """

    serializer_class = MarketSerializer
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "market_id"

    def get_queryset(self):
        return Market.objects.all()


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_id="Get all timezones",
        operation_description="Get all the available timezones",
        tags=["Markets"],
    ),
)
class TimezoneList(generics.ListAPIView):
    queryset = get_all_timezones()
    serializer_class = TimezoneSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [ExpiringTokenAuthentication]
