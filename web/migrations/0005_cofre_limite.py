# Generated by Django 2.0.13 on 2019-06-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_transacao_lido'),
    ]

    operations = [
        migrations.AddField(
            model_name='cofre',
            name='limite',
            field=models.DecimalField(decimal_places=2, default=0.0, help_text='Limite do Cofre.', max_digits=10, verbose_name='Limite'),
        ),
    ]
