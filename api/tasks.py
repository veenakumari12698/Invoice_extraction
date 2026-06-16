from celery import shared_task
from backend.models import Invoice
from PIL import Image
from datetime import datetime
import pytesseract
import re
from decimal import Decimal


def clean_text(text):
    text = text.replace("----------------------------------------", "")
    text = text.replace("₹", "")
    text = text.strip()
    return text



def extract_vendor(text):
    patterns = [
        r"Vendor\s*[:\-]\s*(.+)",
        r"VENDOR\s*[:\-]\s*(.+)"]
    for p in patterns:
        match = re.search(p, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def extract_amount(text):
    amounts = re.findall(r'\d+\.\d{2}', text)
    if amounts:
        return amounts[-1] 
    return None

def extract_date(text):
    match = re.search(r'\d{2}[/-]\d{2}[/-]\d{4}', text)
    return match.group(0) if match else None


@shared_task(bind=True, max_retries=2)
def process_invoice(self, invoice_id):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        invoice.status = "PROCESSING"
        invoice.save()
        file_path = invoice.file.path
        if file_path.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            image = Image.open(file_path)
            text = pytesseract.image_to_string(image, config="--psm 6")
        text = clean_text(text)
        invoice.vendor = extract_vendor(text)
        amount = extract_amount(text)
        invoice.amount = Decimal(amount) if amount else None
        date_str = extract_date(text)
        if date_str:
            invoice.invoice_date = datetime.strptime(
                date_str.replace("-", "/"),
                "%d/%m/%Y"
            ).date()

        invoice.status = "DONE"
        invoice.save()
    except Exception as e:
        try:
            invoice.retry_count += 1
            invoice.save()
        except:
            pass
        if invoice.retry_count < 2:
            raise self.retry(exc=e, countdown=5)
        invoice.status = "FAILED"
        invoice.save()