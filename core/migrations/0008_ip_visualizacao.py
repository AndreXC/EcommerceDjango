# Generated by Django 5.0.3 on 2024-04-22 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_pedido'),
    ]

    operations = [
        migrations.CreateModel(
            name='IP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endereco', models.CharField(max_length=45, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visualizacao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_visualizacoes', models.IntegerField(default=0)),
            ],
        ),
    ]
