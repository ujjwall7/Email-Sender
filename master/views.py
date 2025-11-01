from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from master . models import *
import csv
from master.helpers import sendMail
from django.conf import settings
from master . task import send_mail_task

def companyView(request):
    if request.method == "POST":
        print(f"{request.FILES = }")
    
        csv_file = request.FILES['company_csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Only CSV files are allowed.")
            return redirect('company')
        
        try:
            decoded_file = csv_file.read().decode('utf-8',errors='ignore').splitlines()
            reader = csv.DictReader(decoded_file)
            for row in reader:
                try:
                    # Create object but don't save yet
                    company_obj = Company(
                        s_no=row.get('s_no', '').strip(),
                        name=row.get('name', '').strip(),
                        email=row.get('email', '').strip(),
                        title=row.get('title', '').strip(),
                        company=row.get('company', '').strip()
                    )
                    # Validate fields
                    company_obj.full_clean()
                    company_obj.save()

                except Exception as e:
                    messages.error(request, f"Row {row.get('s_no')}: {e}")
                except Exception as e:
                    messages.error(request, f"Error saving row {row.get('s_no')}: {e}")

            messages.success(request, "CSV file processed successfully.")


        except Exception as e:
            messages.error(request, f"Error reading CSV file: {e}")
            return redirect('company')
        
        return redirect('company')

    return render(request, "company.html")


from django.http import HttpResponse
from io import BytesIO
import os
from master.task import *

def MailSender(request):
    hr_emails = list(Company.objects.all().values_list('email',flat=True))
    # hr_emails = ["sharmaujjwalm0000@gmail.com"]
    hr_emails.append("sharmaujjwal0921@gmail.com")
    company = Credentials.objects.all().last()

    pdf_buffer = BytesIO()
    pdf_buffer.write(b"%PDF-1.4 example PDF content")  # Replace with actual PDF bytes

    subject = company.subject
    from_email = "sharmaujjwalm0000@gmail.com"
    body = company.body
    pdf_filename = "Python 3 years exp"

    with open(company.resume.path, "rb") as f:
        pdf_bytes = f.read()

    for hr_email in hr_emails:
        # pdf_buffer.seek(0)  # Reset pointer each iteration
        send_mail_task.delay(
            subject=subject,
            from_email=from_email,
            to_email=hr_email,
            body=body,
            pdf_bytes=pdf_bytes,
            pdf_filename=pdf_filename,
            is_html=False
        )
    return HttpResponse("Email queued for sending!")

####################################################

# python 3.6 radha jiii om
# abc namahhhh