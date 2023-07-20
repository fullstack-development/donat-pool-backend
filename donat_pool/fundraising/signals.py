from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import CompletedFundraising, Fundraising


@receiver(
    post_save,
    sender=CompletedFundraising,
    dispatch_uid='delete_active_fundraising'
)
def delete_active_fundraising(
    sender, instance: CompletedFundraising, created, **kwargs
):
    try:
        fundraising = Fundraising.objects.get(pk=instance.path)
    except Fundraising.DoesNotExist:
        return
    fundraising.delete()
