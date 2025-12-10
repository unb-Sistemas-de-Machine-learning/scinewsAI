from app.services.email import send_email
import sys

to_email = "bruno.martval@gmail.com"
subject = "Test Email from SciNewsAI Docker"
content = """
<h1>Hello from Docker!</h1>
<p>This is a test email sent from the SciNewsAI backend container.</p>
<p>If you see this, the SMTP configuration is working correctly.</p>
"""

print(f"Attempting to send email to {to_email}...")
print(f"Subject: {subject}")

try:
    success = send_email(to_email, subject, content)
    if success:
        print("\nSUCCESS: Email sent successfully!")
    else:
        print("\nFAILURE: Email sending returned False check logs for details.")
except Exception as e:
    print(f"\nEXCEPTION: {e}")
