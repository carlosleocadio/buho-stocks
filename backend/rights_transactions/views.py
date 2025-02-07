from django.utils.decorators import method_decorator
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from buho_backend.utils.token_utils import ExpiringTokenAuthentication
from companies.models import Company
from log_messages.models import LogMessage
from rights_transactions.models import RightsTransaction
from rights_transactions.serializers import RightsTransactionSerializer


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_id="List rights transactions",
        operation_description="Get a list of rights transactions of the current company",
        tags=["Rights"],
    ),
)
@method_decorator(
    name="post",
    decorator=swagger_auto_schema(
        operation_id="Create rights transaction",
        operation_description="Create a new rights transaction for the current company",
        tags=["Rights"],
    ),
)
class RightsTransactionListCreateAPIView(generics.ListCreateAPIView):
    """Get all the rights transactions from a company"""

    serializer_class = RightsTransactionSerializer
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        company_id = self.kwargs.get("company_id")
        user = self.request.user
        return RightsTransaction.objects.filter(company=company_id, user=user.id)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Log the operation
        company = Company.objects.get(id=serializer.data["company"])
        LogMessage.objects.create(
            message_type=LogMessage.MESSAGE_TYPE_ADD_RIGHTS,
            message_text=f"Rights added: {company.name} ({company.ticker}). {serializer.data.get('count')} - {serializer.data.get('gross_price_per_share')}. {serializer.data.get('notes')}",
            portfolio=company.portfolio,
            user=self.request.user,
        )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        operation_id="Retrieve rights transaction",
        operation_description="Get an existing rights transaction of the current user",
        tags=["Rights"],
    ),
)
@method_decorator(
    name="put",
    decorator=swagger_auto_schema(
        operation_id="Update rights transaction",
        operation_description="Update an existing rights transaction of the current user",
        tags=["Rights"],
    ),
)
@method_decorator(
    name="patch",
    decorator=swagger_auto_schema(
        operation_id="Patch rights transaction",
        operation_description="Patch an existing rights transaction of the current user",
        tags=["Rights"],
    ),
)
@method_decorator(
    name="delete",
    decorator=swagger_auto_schema(
        operation_id="Delete rights transaction",
        operation_description="Delete an existing rights transaction of the current user",
        tags=["Rights"],
    ),
)
class RightsTransactionDetailsDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    serializer_class = RightsTransactionSerializer
    authentication_classes = [ExpiringTokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "transaction_id"

    def get_queryset(self):
        transaction_id = self.kwargs.get("transaction_id")
        user = self.request.user
        return RightsTransaction.objects.filter(id=transaction_id, user=user.id)
