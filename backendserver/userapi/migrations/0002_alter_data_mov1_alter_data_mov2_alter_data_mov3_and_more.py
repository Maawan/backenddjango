# Generated by Django 4.2.3 on 2023-08-02 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='mov1',
            field=models.CharField(blank=True, default='The Shawshank Redemption', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='mov2',
            field=models.CharField(blank=True, default='The Godfather', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='mov3',
            field=models.CharField(blank=True, default='The Dark Knight', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='mov4',
            field=models.CharField(blank=True, default='Pulp Fiction', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='data',
            name='mov5',
            field=models.CharField(blank=True, default='American History X', max_length=50, null=True),
        ),
    ]
