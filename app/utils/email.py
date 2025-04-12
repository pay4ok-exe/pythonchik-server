# app/utils/email.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

class EmailService:
    def __init__(self):
        # Default configuration - can be overridden in environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME", "your_email@gmail.com")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "your_app_password")
        self.from_email = os.getenv("FROM_EMAIL", "no-reply@pythonchick.com")
        self.from_name = os.getenv("FROM_NAME", "Pythonchick")
        
    def send_email(self, to_email, subject, html_content, text_content=None):
        """
        Send an email using SMTP
        
        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            html_content (str): HTML content of the email
            text_content (str, optional): Plain text content (fallback for non-HTML clients)
        
        Returns:
            bool: Success status
        """
        # Create message container - the correct MIME type is multipart/alternative
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"{self.from_name} <{self.from_email}>"
        msg['To'] = to_email
        
        # Create the body of the message
        if text_content is None:
            # Create a simple text version from HTML if not provided
            text_content = html_content.replace('<br>', '\n').replace('</p>', '\n').replace('</div>', '\n')
            # Remove all remaining HTML tags
            import re
            text_content = re.sub('<[^<]+?>', '', text_content)
        
        # Record the MIME types
        part1 = MIMEText(text_content, 'plain')
        part2 = MIMEText(html_content, 'html')
        
        # Attach parts into message container
        # According to RFC 2046, the last part of a multipart message is best and preferred
        msg.attach(part1)
        msg.attach(part2)
        
        try:
            # Send the message via SMTP server
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.ehlo()  # Identify ourselves to the server
                server.starttls()  # Secure the connection
                server.ehlo()  # Re-identify ourselves over TLS connection
                
                # Login if credentials are provided
                if self.smtp_username and self.smtp_password:
                    server.login(self.smtp_username, self.smtp_password)
                
                server.sendmail(self.from_email, to_email, msg.as_string())
                
            return True
        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            # In development mode, log the email content
            if settings.ENVIRONMENT == "development":
                print(f"Would have sent email to {to_email}:")
                print(f"Subject: {subject}")
                print(f"Content: {html_content}")
            return False
    
    def send_password_reset(self, to_email, reset_token, username):
        """
        Send a password reset email
        
        Args:
            to_email (str): Recipient email
            reset_token (str): Password reset token
            username (str): User's username
        
        Returns:
            bool: Success status
        """
        subject = "Password Reset Request - Pythonchick"
        
        # Create a password reset link
        reset_link = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}&email={to_email}"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #FF8C00;">Password Reset Request</h2>
            <p>Hello {username},</p>
            <p>We received a request to reset your password. Click the button below to reset it:</p>
            <div style="text-align: center; margin: 30px 0;">
                <a href="{reset_link}" style="background-color: #FF8C00; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Reset Password
                </a>
            </div>
            <p>If you didn't request a password reset, you can safely ignore this email.</p>
            <p>This link will expire in 30 minutes for security reasons.</p>
            <p>Best regards,<br>The Pythonchick Team</p>
        </div>
        """
        
        return self.send_email(to_email, subject, html_content)
    
    def send_verification_email(self, to_email, verification_code, username):
        """
        Send an email verification code
        
        Args:
            to_email (str): Recipient email
            verification_code (str): Verification code
            username (str): User's username
        
        Returns:
            bool: Success status
        """
        subject = "Verify Your Email - Pythonchick"
        
        html_content = f"""
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2 style="color: #FF8C00;">Email Verification</h2>
            <p>Hello {username},</p>
            <p>Thank you for registering with Pythonchick! Please use the verification code below to complete your registration:</p>
            <div style="text-align: center; margin: 30px 0;">
                <div style="font-size: 24px; letter-spacing: 5px; font-weight: bold; background-color: #f0f0f0; padding: 15px; border-radius: 5px;">
                    {verification_code}
                </div>
            </div>
            <p>This code will expire in 30 minutes.</p>
            <p>If you didn't create an account with us, you can safely ignore this email.</p>
            <p>Best regards,<br>The Pythonchick Team</p>
        </div>
        """
        
        return self.send_email(to_email, subject, html_content)

# Add to config.py - this is for development mode
# Update the settings class in app/config.py:
"""
class Settings(BaseSettings):
    # ... existing settings ...
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Frontend URL for redirects
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
"""