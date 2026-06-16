
from django.urls import path
from .import views

urlpatterns = [
    path("invoices/",views.InvoiceUpload.as_view()),
    path("invoices/<int:id>/", views.InvoiceDetail.as_view()),
    path("reports/",views.VendorReport.as_view()),

]