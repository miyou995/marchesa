# Generated by Django 3.2.5 on 2021-08-03 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atributes', '0001_initial'),
        ('core', '0004_auto_20210802_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='couleur',
            field=models.ManyToManyField(blank=True, to='atributes.Couleur'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pointure',
            field=models.ManyToManyField(blank=True, to='atributes.Pointure'),
        ),
        migrations.AlterField(
            model_name='product',
            name='taille',
            field=models.ManyToManyField(blank=True, to='atributes.Taille'),
        ),
    ]