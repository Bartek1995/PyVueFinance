from rest_framework import viewsets, generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Company, StockPrice
from .serializers import CompanySerializer, StockPriceSerializer

import yfinance as yf
from datetime import datetime
import pandas as pd

# --- ViewSets for CRUD operations ---

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

# --- Utility functions ---

def safe_get(val):
    if isinstance(val, pd.Series):
        val = val.values[0]
    if pd.notnull(val):
        return float(val)
    return 0

def safe_get_int(val):
    if isinstance(val, pd.Series):
        val = val.values[0]
    if pd.notnull(val):
        return int(val)
    return 0

# --- API for fetching company & price data from Yahoo ---

class FetchCompanyData(APIView):
    """
    POST: { ticker, start, end }
    Pobiera dane z Yahoo, zapisuje firmę + ceny w bazie.
    """
    def post(self, request):
        ticker = request.data.get("ticker", "").upper()
        start = request.data.get("start")
        end = request.data.get("end")

        if not ticker or not start or not end:
            return Response({"error": "Missing required fields"}, status=400)
        
        try:
            data = yf.download(ticker, start=start, end=end)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

        if data.empty:
            return Response({"error": f"No data for ticker: {ticker}"}, status=404)

        info = yf.Ticker(ticker).info
        name = info.get("shortName") or ticker

        company, created = Company.objects.get_or_create(
            ticker=ticker,
            defaults={
                "name": name,
                "isin": None,
                "country": info.get("country"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "description": info.get("longBusinessSummary"),
            }
        )

        added, skipped = 0, 0
        for date_str, row in data.iterrows():
            date = date_str.date() if hasattr(date_str, 'date') else datetime.strptime(str(date_str), "%Y-%m-%d").date()
            obj, was_created = StockPrice.objects.get_or_create(
                company=company,
                date=date,
                defaults={
                    "open": safe_get(row["Open"]),
                    "close": safe_get(row["Close"]),
                    "high": safe_get(row["High"]),
                    "low": safe_get(row["Low"]),
                    "volume": safe_get_int(row["Volume"]),
                }
            )
            if was_created:
                added += 1
            else:
                skipped += 1

        return Response({
            "company": CompanySerializer(company).data,
            "created": created,
            "prices_added": added,
            "prices_skipped": skipped,
        }, status=status.HTTP_201_CREATED)

# --- Read-only API for frontend ---

class CompanyDetailView(generics.RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'ticker'

class CompanyPriceHistory(generics.ListAPIView):
    serializer_class = StockPriceSerializer

    def get_queryset(self):
        ticker = self.kwargs["ticker"]
        company = get_object_or_404(Company, ticker=ticker)
        return company.prices.order_by("date").all()
