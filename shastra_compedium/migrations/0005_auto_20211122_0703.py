# Generated by Django 3.0.14 on 2021-11-22 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shastra_compedium', '0004_auto_20211023_1332'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='summary',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterUniqueTogether(
            name='position',
            unique_together={('name', 'category'), ('category', 'order')},
        ),
    ]
