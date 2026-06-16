from rest_framework import serializers
from backend.models import Invoice

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"
        read_only_fields = ("vendor", "amount", "invoice_date", "status", "retry_count")