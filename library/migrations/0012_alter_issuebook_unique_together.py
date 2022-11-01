# Generated by Django 4.1.2 on 2022-10-21 05:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('library', '0011_alter_book_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='issuebook',
            unique_together={('book', 'user', 'status')},
        ),
    ]
