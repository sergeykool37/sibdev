# Generated by Django 3.1.3 on 2020-11-15 03:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0009_auto_20201114_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='product',
            field=models.CharField(choices=[('TV', 'tv'), ('IPAD', 'ipad'), ('PLAYSTATION', 'playstation')], max_length=11),
        ),
    ]
