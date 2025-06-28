from django.db import models

class Company(models.Model):
    ticker = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=128)
    isin = models.CharField(max_length=16, blank=True, null=True)
    country = models.CharField(max_length=32, blank=True, null=True)
    sector = models.CharField(max_length=64, blank=True, null=True)
    industry = models.CharField(max_length=64, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.ticker} ({self.name})"

class StockPrice(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='prices')
    date = models.DateField()
    open = models.DecimalField(max_digits=12, decimal_places=4)
    close = models.DecimalField(max_digits=12, decimal_places=4)
    high = models.DecimalField(max_digits=12, decimal_places=4)
    low = models.DecimalField(max_digits=12, decimal_places=4)
    volume = models.BigIntegerField()

    class Meta:
        unique_together = ('company', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.company.ticker} {self.date}: {self.close}"
