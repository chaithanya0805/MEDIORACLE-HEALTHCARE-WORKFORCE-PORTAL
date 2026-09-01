from django.contrib import admin
from apps.billing.models import Invoice, InvoiceLineItem, Payment, PaymentAdjustment, PaymentDispute

admin.site.register(Invoice)
admin.site.register(InvoiceLineItem)
admin.site.register(Payment)
admin.site.register(PaymentAdjustment)
admin.site.register(PaymentDispute)
