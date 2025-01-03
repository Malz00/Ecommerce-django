# Generated by Django 5.1.2 on 2024-11-25 07:40

import product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=56)),
                ('slug', models.SlugField(blank=True, default='abc', unique=True)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, default=12.99, max_digits=12)),
                ('image', models.ImageField(blank=True, null=True, upload_to=product.models.upload_image_path)),
                ('featured', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('timestamp', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
