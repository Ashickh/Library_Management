# Generated by Django 4.1.2 on 2022-11-10 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testapp', '0002_alter_student_roll_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='age',
            field=models.PositiveBigIntegerField(default=18),
            preserve_default=False,
        ),
    ]