# Generated by Django 3.2.18 on 2023-04-23 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MiningMachineProduct', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='nickname',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
