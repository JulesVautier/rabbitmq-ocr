# Generated by Django 2.1.4 on 2019-01-04 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ocr_dispatcher', '0007_ocrrequest_number_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='ocrresult',
            name='status',
            field=models.CharField(default='WAITING', max_length=30),
        ),
    ]
