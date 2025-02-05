# Generated by Django 5.1.3 on 2025-02-01 20:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='store.basemodel')),
                ('code', models.CharField(max_length=100, unique=True)),
                ('discount', models.FloatField()),
                ('valid_from', models.DateTimeField()),
                ('valid_to', models.DateTimeField()),
                ('max_usage', models.PositiveBigIntegerField(default=1)),
                ('active', models.BooleanField(default=True)),
            ],
            bases=('store.basemodel',),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='final_price',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='carbooking',
            name='total_payment',
            field=models.FloatField(),
        ),
        migrations.AddField(
            model_name='carbooking',
            name='coupon_obj',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.coupon'),
        ),
    ]
