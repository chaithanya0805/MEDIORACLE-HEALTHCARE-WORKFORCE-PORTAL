from django.db import models
from apps.facilities.models import Facility, Department, Ward

class DemandForecast(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='forecasts')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    ward = models.ForeignKey(Ward, on_delete=models.CASCADE)
    date = models.DateField()
    expected_census = models.IntegerField(default=15)
    required_staff = models.IntegerField(default=4)
    available_staff = models.IntegerField(default=3)
    shortage = models.IntegerField(default=1)
    surplus = models.IntegerField(default=0)
    forecast_accuracy = models.DecimalField(max_digits=5, decimal_places=2, default=95.00)

    def __str__(self):
        return f"Forecast for {self.ward.name} on {self.date}"
