# Generated by Django 4.2 on 2025-02-12 16:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(max_length=500),
        ),
        migrations.AlterField(
            model_name='room',
            name='description',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='room',
            name='topic',
            field=models.ForeignKey(max_length=150, null=True, on_delete=django.db.models.deletion.SET_NULL, to='base.topic'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=models.CharField(max_length=150),
        ),
    ]
