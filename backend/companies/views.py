from rest_framework.response import Response
from rest_framework.authentication import (
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from companies.serializers import CompanySerializer, CompanySerializerGet
from companies.models import Company
from currencies.models import get_currency_details


class CompaniesListAPIView(APIView):
    """Get all the companies from a user's portfolio"""

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # 1. List all
    @swagger_auto_schema(tags=["portfolio_companies"])
    def get(self, request, portfolio_id, *args, **kwargs):
        """
        List all the portfolio items for given requested user
        """
        elements = Company.objects.filter(user=request.user.id, portfolio=portfolio_id)
        for element in elements:
            base_currency = get_currency_details(element.base_currency)
            dividends_currency = get_currency_details(element.dividends_currency)
            element.base_currency = base_currency
            element.dividends_currency = dividends_currency

        serializer = CompanySerializerGet(
            elements, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    @swagger_auto_schema(tags=["portfolio_companies"], request_body=CompanySerializer)
    def post(self, request, portfolio_id, *args, **kwargs):
        """
        Create the company with given portfolio data
        """
        print(portfolio_id)
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "color": request.data.get("color"),
            "ticker": request.data.get("ticker"),
            "alt_tickers": request.data.get("alt_tickers"),
            "country_code": request.data.get("country_code"),
            "broker": request.data.get("broker"),
            "url": request.data.get("url"),
            "base_currency": request.data.get("base_currency"),
            "dividends_currency": request.data.get("dividends_currency"),
            "sector": request.data.get("sector"),
            "market": request.data.get("market"),
            "portfolio": portfolio_id,
        }
        serializer = CompanySerializer(data=data, context={"request": request})
        if serializer.is_valid():
            print("Serializer is valid")
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CompanyDetailAPIView(APIView):
    """Operations for a single Company"""

    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, portfolio_id, company_id, user_id):
        """
        Get a market object from a user given the portfolio id
        """
        try:
            return Company.objects.get(
                id=company_id, portfolio=portfolio_id, user=user_id
            )
        except Company.DoesNotExist:
            return None

    # 3. Retrieve
    @swagger_auto_schema(tags=["portfolio_companies"])
    def get(self, request, portfolio_id, company_id, *args, **kwargs):
        """
        Retrieve the company item with given company_id
        """
        instance = self.get_object(portfolio_id, company_id, request.user.id)
        if not instance:
            return Response(
                {"res": "Object with portfolio id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        base_currency = get_currency_details(instance.base_currency)
        dividends_currency = get_currency_details(instance.dividends_currency)
        instance.base_currency = base_currency
        instance.dividends_currency = dividends_currency
        serializer = CompanySerializerGet(instance, context={"request": request})
        new_data = serializer.data

        return Response(new_data, status=status.HTTP_200_OK)

    # 4. Update
    @swagger_auto_schema(tags=["portfolio_companies"], request_body=CompanySerializer)
    def put(self, request, portfolio_id, company_id, *args, **kwargs):
        """
        Update the company item with given company_id
        """
        instance = self.get_object(portfolio_id, company_id, request.user.id)
        if not instance:
            return Response(
                {"res": "Object with portfolio id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {
            "name": request.data.get("name"),
            "description": request.data.get("description"),
            "color": request.data.get("color"),
            "tiker": request.data.get("ticker"),
            "alt_tickers": request.data.get("alt_tickers"),
            "country_code": request.data.get("country_code"),
            "broker": request.data.get("broker"),
            "url": request.data.get("url"),
            "currency": request.data.get("currency"),
            "dividends_currency": request.data.get("dividends_currency"),
            "sector": request.data.get("sector"),
            "market": request.data.get("market"),
        }
        serializer = CompanySerializer(
            instance=instance, data=data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    @swagger_auto_schema(tags=["portfolio_companies"])
    def delete(self, request, portfolio_id, company_id, *args, **kwargs):
        """
        Delete the company item with given company_id
        """
        market_instance = self.get_object(company_id, portfolio_id, request.user.id)
        if not market_instance:
            return Response(
                {"res": "Object with company id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        market_instance.delete()
        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
