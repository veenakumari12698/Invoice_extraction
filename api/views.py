from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InvoiceSerializer
from .tasks import process_invoice
from backend.models import Invoice
from django.db.models import Sum
from PIL import Image
import pytesseract


class InvoiceUpload(APIView):
    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            invoice = serializer.save(status="QUEUED")
            process_invoice.delay(invoice.id)
            return Response({"message": "File uploaded","invoice_id": invoice.id,"status": "success"},status=status.HTTP_200_OK,)
        return Response({"message": "Invalid data","errors": serializer.errors,},
            status=status.HTTP_400_BAD_REQUEST,)
    

class InvoiceDetail(APIView):
    def get(self, request, id):
        invoice = Invoice.objects.get(id=id)
        return Response({
            "id": invoice.id,
            "status": invoice.status,
            "vendor": invoice.vendor,
            "amount": invoice.amount,
            "invoice_date": invoice.invoice_date,
            
        })

### Vendor Reports
class VendorReport(APIView):
    def get(self, request):
        data = (Invoice.objects.filter(status="DONE").values("vendor").annotate(total_amount=Sum("amount")).order_by("-total_amount"))
        return Response(data)
    


