from datetime import datetime, date
from uuid import uuid4
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


def birthday_validator(date: datetime.date) -> None:
    if date > timezone.now().date():
        raise ValidationError('The date of birth cannot be in the future.')


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class Client(UUIDMixin):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='user', on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name='Date of Birth', validators=[birthday_validator])

    @property
    def username(self) -> str:
        return self.user.username

    @property
    def first_name(self) -> str:
        return self.user.first_name

    @property
    def last_name(self) -> str:
        return self.user.last_name

    @property
    def email(self) -> str:
        return self.user.email

    @property
    def age(self) -> int:
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))

    def __str__(self) -> str:
        return f'{self.username} {self.first_name} {self.last_name}'

    class Meta:
        db_table = "client"
        verbose_name = 'client'
        verbose_name_plural = 'clients'


class Subscription(UUIDMixin):
    user = models.ForeignKey(Client, related_name='user_subscriptions', on_delete=models.CASCADE)
    subscribed_to = models.ForeignKey(Client, related_name='subscribed_to', on_delete=models.CASCADE)

    def clean(self):
        if self.user == self.subscribed_to:
            raise ValidationError("A user cannot subscribe to themselves.")

    def __str__(self):
        return f'{self.user.username} -> {self.subscribed_to.username}'

    class Meta:
        db_table = "subscription"
        verbose_name = 'subscription'
        verbose_name_plural = 'subscriptions'
        constraints = [
            models.UniqueConstraint(fields=['user', 'subscribed_to'], name='unique_subscription')
        ]
