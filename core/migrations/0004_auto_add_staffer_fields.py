# Generated by Django 2.1.4 on 2019-01-29 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_fix_member_post_overhaul'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffer',
            name='favorite_trips',
            field=models.TextField(blank=True, help_text='List of your favorite trips, one per line', null=True),
        ),
        migrations.AddField(
            model_name='staffer',
            name='nickname',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AddField(
            model_name='staffer',
            name='is_active',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='staffer',
            name='autobiography',
            field=models.TextField(default='I am too lazy and lame to upload a bio!', null=True, verbose_name='Self Description of the staffer'),
        ),
    ]
