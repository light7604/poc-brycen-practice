# Generated by Django 4.2.4 on 2023-08-29 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_product_detail'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
    ]
