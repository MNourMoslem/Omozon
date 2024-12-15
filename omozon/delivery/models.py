from django.db import models
from django.conf import settings
from accounts.models import DELIVERY_MANAGER, CustomUser

class DeliveryManagerUser(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='delivery_manager_user'
    )

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.user.account_type = DELIVERY_MANAGER
        super().save(*args, **kwargs)
