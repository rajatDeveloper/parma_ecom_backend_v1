# Generated by Django 4.2.5 on 2023-10-07 07:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zipCode', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_addresses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.IntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('dilveryStatus', models.CharField(choices=[('pending', 'Pending'), ('dispatch', 'Dispatch'), ('dilveried', 'Dilveried')], max_length=10)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='main_app.address')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=50)),
                ('imageData', models.ImageField(upload_to='product_image/')),
                ('shortDes', models.TextField(default='', max_length=120)),
                ('longDes', models.TextField(default='', max_length=120)),
                ('mainPrice', models.IntegerField(default=0)),
                ('afterDiscountPrice', models.IntegerField(default=0)),
                ('category', models.CharField(default='', max_length=50)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('isSale', models.BooleanField(default=False)),
                ('stock', models.IntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
        migrations.DeleteModel(
            name='Client',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(to='main_app.product'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
