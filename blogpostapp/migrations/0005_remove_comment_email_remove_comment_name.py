# Generated by Django 4.1.5 on 2023-02-01 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blogpostapp", "0004_favoriteblog"),
    ]

    operations = [
        migrations.RemoveField(model_name="comment", name="email",),
        migrations.RemoveField(model_name="comment", name="name",),
    ]