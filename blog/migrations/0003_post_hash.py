# Generated by Django 3.0.7 on 2021-01-02 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_remove_post_hash'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='hash',
            field=models.CharField(default=0, max_length=32, null=True),
        ),
    ]
