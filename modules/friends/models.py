import uuid
from django.db import models
from django.contrib.auth.models import User
from modules.models import CrudConstrained
from django.utils.text import slugify
from django_fsm import FSMIntegerField, transition


class Friendrequest(CrudConstrained):
    STATUS_PENDING = 0
    STATUS_COMPLETED = 1
    STATUS_CANCELLED = 2
    STATUS_CHOICES = (
        (STATUS_PENDING, 'pending'),
        (STATUS_COMPLETED, 'completed'),
        (STATUS_CANCELLED, 'cancelled'),
    )
    gid = models.UUIDField(
        max_length=32, unique=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user")
    friend = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="friend")
    slug = models.SlugField(
        max_length=100, unique=True)
    status = FSMIntegerField(
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        protected=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Friendrequests"
        ordering = ('date_created',)

    @transition(field=status, source=STATUS_PENDING, target=STATUS_COMPLETED)
    def accept(self):
        print("The request is accepted.")

    @transition(field=status, source=STATUS_PENDING, target=STATUS_CANCELLED)
    def decline(self):
        print("The request is cancelled.")

    @transition(field=status, source=STATUS_CANCELLED, target=STATUS_PENDING)
    def pending(self):
        print("The request is pending.")


    def _get_unique_slug(self):
        """
        Generate unique slug for the Friendrequest object.
        Used by the Friendrequest object save method, while creating 
        new friendrequest.
        """
        slug = slugify(self.user.username[:40 - 2])
        unique_slug = slug
        num = 1
        while Friendrequest.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()
        super(Friendrequest, self).save(*args, **kwargs)
