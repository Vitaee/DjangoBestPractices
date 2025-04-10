from celery import shared_task
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task
def notify_magaza_change(magaza_id, action, user_id):
    """
    Send notification about store changes
    """
    from .models import Magaza
    
    try:
        magaza = Magaza.objects.get(pk=magaza_id)
        user = User.objects.get(pk=user_id)
        
        # Log the action
        logger.info(f"Mağaza {magaza.ad} was {action} by {user.username}")
        
        # Send email notification (simulated)
        subject = f"Mağaza {action.title()}: {magaza.ad}"
        message = f"""
        Dear {user.username},
        
        Your store '{magaza.ad}' has been {action}.
        
        Best regards,
        The Magaza Team
        """
        
        # This would actually send an email in production
        # We're just logging it for demonstration
        logger.info(f"Would send email: {subject}\n{message}")
        
        # Uncomment to actually send email
        # send_mail(
        #     subject,
        #     message,
        #     'noreply@example.com',
        #     [user.email],
        #     fail_silently=False,
        # )
        
        return f"Notification for {magaza.ad} sent successfully"
    except Exception as e:
        logger.error(f"Error in notify_magaza_change task: {str(e)}")
        return f"Error: {str(e)}"
