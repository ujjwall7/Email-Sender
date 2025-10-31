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


def MailSender(request):
    send_mail_task.delay(
        subject = "Ujjwal sharma",
        body = "Hello",
        from_email = settings.EMAIL_HOST_USER,
        to_email = settings.EMAIL_HOST_USER,
        is_html = False
    )
    return HttpResponse("Email queued for sending!")


# python 3.6