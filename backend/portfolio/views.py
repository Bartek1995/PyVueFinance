from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Company, StockPrice
from .serializers import CompanySerializer, StockPriceSerializer

import yfinance as yf
from datetime import datetime
import pandas as pd

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class StockPriceViewSet(viewsets.ModelViewSet):
    queryset = StockPrice.objects.all()
    serializer_class = StockPriceSerializer

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

class FetchCompanyData(APIView):
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
            open_val = safe_get(row["Open"])
            close_val = safe_get(row["Close"])
            high_val = safe_get(row["High"])
            low_val = safe_get(row["Low"])
            volume_val = safe_get_int(row["Volume"])

            obj, was_created = StockPrice.objects.get_or_create(
                company=company,
                date=date,
                defaults={
                    "open": open_val,
                    "close": close_val,
                    "high": high_val,
                    "low": low_val,
                    "volume": volume_val,
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
        })
