# emails/tasks.py
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from io import BytesIO
from django.conf import settings



@shared_task
def send_mail_task(
    subject: str,
    from_email: str,
    to_email: str,
    body: str = None,
    html_template: str = None,
    context=None,
    pdf_bytes: bytes = None,
    pdf_filename: str = None,
    is_html=False
):
    """
    Celery task for sending an email with optional HTML body, 
    template rendering, and PDF attachment.
    """ 
    print("Ujjwal sharma")

    if not from_email or not to_email:
        print("Email not get")
        return

    try:
        # Generate email body
        if html_template:
            context = context or {}
            email_body = render_to_string(html_template, context)
            is_html = True
        elif body:
            email_body = body
        else:
            return  # nothing to send

        # Create email
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=from_email,
            to=[to_email],
        )

        # HTML flag
        if is_html:
            email.content_subtype = 'html'

        # PDF attachment
        if pdf_bytes:
            pdf_buffer = BytesIO(pdf_bytes)
            attachment_name = pdf_filename or "attachment.pdf"
            email.attach(attachment_name, pdf_buffer.getvalue(), 'application/pdf')

        email.send()
        print("Email Send Successfully")

    except Exception as e:
        print(f"{e = }")
        pass
