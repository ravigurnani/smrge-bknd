# Generated by Django 4.0.5 on 2022-07-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile_email_userprofile_saved_profiles_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='facebook',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='insta',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_lat',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='last_lon',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='linkedin',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='profile',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twitter',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
