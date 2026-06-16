# Invoice Processing System
This project is a Django-based system to upload and process invoices asynchronously. It extracts vendor, date, and amount from invoice files using OCR and regex.


## How it works
User uploads invoice via API
File is saved in database with status QUEUED
Celery processes file in background
Redis handles task queue
OCR extracts text (Tesseract)
Regex extracts required fields
Status updated to DONE / FAILED
## Retry
If processing fails, task is retried up to 2 times before marking as FAILED.
## Scaling
Multiple Celery workers can run in parallel to handle large number of uploads (1000+). Redis ensures smooth task distribution.
## Features
Django REST API
MySQL Database
Redis Queue
Celery Background Tasks
OCR using Tesseract
Dockerized Application

###### Run Project
docker compose up --build


## Upload Invoice
POST /api/invoices/
## Get Status
GET /api/invoices/<id>/
## Get Reports
GET /api/reports/


### Query 
SELECT *
FROM backend_invoice
WHERE status = 'FAILED'
AND retry_count > 1
AND created_at >= NOW() - INTERVAL '7 days';

## Tech Stack
Django, DRF, MySQL, Redis, Celery, Tesseract OCR, Docker