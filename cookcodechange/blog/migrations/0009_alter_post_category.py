# Generated by Django 5.1.4 on 2025-01-31 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.CharField(choices=[('VENTRE', 'Ventre'), ('TETE', 'Tête'), ('COEUR', 'Coeur')], default='VENTRE', max_length=50),
        ),
    ]
