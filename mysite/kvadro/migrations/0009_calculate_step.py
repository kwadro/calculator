# Generated by Django 4.2.4 on 2023-09-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kvadro', '0008_remove_calculate_user_id_calculate_visitor_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculate',
            name='step',
            field=models.IntegerField(default=0),
        ),
    ]
