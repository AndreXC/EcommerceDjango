# Generated by Django 5.0.3 on 2024-03-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UsuarioAdmin',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('email_cifrado', models.TextField()),
                ('senha_hash', models.TextField()),
                ('chave_criptografia', models.TextField()),
            ],
            options={
                'db_table': 'useradmin',
            },
        ),
        migrations.AlterModelTable(
            name='lanche',
            table=None,
        ),
    ]
