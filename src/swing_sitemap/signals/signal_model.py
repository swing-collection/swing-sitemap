from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import MyModel  # Import your model
# Import any other necessary modules
 from .tasks import submit_sitemap  # Import the Celery task


@receiver(post_save, sender=MyModel)
def model_post_save(sender, instance, **kwargs):
    submit_sitemap()

@receiver(post_delete, sender=MyModel)
def model_post_delete(sender, instance, **kwargs):
    submit_sitemap()
