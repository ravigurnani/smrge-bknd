# Generated by Django 4.0.5 on 2022-07-01 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='saved_profiles',
            field=models.ManyToManyField(blank=True, to='user.userprofile'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='token',
            field=models.CharField(default='', max_length=128, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='intersts',
            field=models.ManyToManyField(blank=True, to='user.interest'),
        ),
    ]