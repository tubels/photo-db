# Generated by Django 4.1.3 on 2022-12-02 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('photos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='camera',
            name='dateOfPurchase',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='endDate',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='place',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='photos',
            name='event',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='photos.event'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='film',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='photos.film'),
        ),
        migrations.AlterField(
            model_name='photos',
            name='filmend',
            field=models.DateTimeField(null=True),
        ),
    ]
