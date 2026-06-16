from django.db import models

# Create your models here.

class Invoice(models.Model):
    STATUS_CHOICES = [
        ("QUEUED", "Queued"),
        ("PROCESSING", "Processing"),
        ("DONE", "Done"),
        ("FAILED", "Failed"),]
    file = models.FileField(upload_to="invoices/")
    vendor = models.CharField(max_length=255,null=True,blank=True)
    amount = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)
    invoice_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default="QUEUED")
    retry_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Invoice {self.id}"
    