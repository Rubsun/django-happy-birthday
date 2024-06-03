# Generated by Django 5.0.6 on 2024-06-03 10:55

import HB_app.models
import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date_of_birth', models.DateField(validators=[HB_app.models.birthday_validator], verbose_name='Date of Birth')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'client',
                'verbose_name_plural': 'clients',
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('subscribed_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribed_to', to='HB_app.client')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscriptions', to='HB_app.client')),
            ],
            options={
                'verbose_name': 'subscription',
                'verbose_name_plural': 'subscriptions',
                'db_table': 'subscription',
            },
        ),
        migrations.AddConstraint(
            model_name='subscription',
            constraint=models.UniqueConstraint(fields=('user', 'subscribed_to'), name='unique_subscription'),
        ),
    ]
