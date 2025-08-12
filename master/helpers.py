from django.core.mail import EmailMessage
from django.template.loader import render_to_string

def sendMail(
    subject: str,
    from_email: str,
    to_email: str,
    body: str = None,
    html_template: str = None,
    context = None, 
    pdf_buffer=None,
    pdf_filename: str = None,
    is_html = False
):
    """
    Sends an email with optional HTML body, template rendering, and PDF attachment.
    Silently ignores all exceptions (useful in non-critical flows).

    Args:
        subject (str): Email subject (required)
        from_email (str): Sender email (required)
        to_email (str): Receiver email (required)
        body (str): Body content if not using template
        html_template (str): Django template path (optional)
        context (dict): Context for template (optional)
        pdf_buffer: BytesIO object (optional)
        pdf_filename (str): Name of attached PDF (default "attachment.pdf")
        is_html (bool): True if body is HTML (default False)
    """
    if not from_email or not to_email:
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
            return  # no content to send

        # Create the email
        email = EmailMessage(
            subject=subject,
            body=email_body,
            from_email=from_email,
            to=[to_email],
        )

        # Mark as HTML if specified
        if is_html:
            email.content_subtype = 'html'

        # Attach PDF if buffer provided
        if pdf_buffer:
            attachment_name = pdf_filename or "attachment.pdf"
            email.attach(attachment_name, pdf_buffer.getvalue(), 'application/pdf')

        email.send()

    except Exception as e:
        print(f"{e = }")
        pass 
