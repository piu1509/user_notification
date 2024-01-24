import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from modules.models import CrudConstrained


class Notification(CrudConstrained):
    """
            Notification model description.
    """
    gid = models.UUIDField(
        max_length=32, default=uuid.uuid4, unique=True, editable=False)
    slug = models.SlugField(max_length=100, unique=True)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE,
                                 related_name="receiver")
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_count = models.BooleanField(default=False)
    read_date = models.DateTimeField(_("Date deleted"), auto_now=True)

    def __str__(self):
        return self.sender.username

    class Meta:
        verbose_name_plural = 'Notifications'
        ordering = ('date_created',)

    def _get_unique_slug(self):
        """
                Generate unique slug for the Notification object.
                Used by the Notification object save method, while creating new notification.
        """
        slug = slugify(self.sender.username[:40 - 2])
        unique_slug = slug
        num = 1
        while Notification.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Notification, self).save(*args, **kwargs)
