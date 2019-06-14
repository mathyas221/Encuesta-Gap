# Generated by Django 2.2.2 on 2019-06-06 21:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('D1', 'Dominio 1'), ('D2', 'Dominio 2'), ('D3', 'Dominio 3'), ('D4', 'Dominio 4'), ('D5', 'Dominio 5'), ('D6', 'Dominio 6'), ('D7', 'Dominio 7'), ('D8', 'Dominio 8'), ('D9', 'Dominio 9'), ('D10', 'Dominio 10'), ('D11', 'Dominio 11')], max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Personal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(choices=[('AD1', 'Administrador 1'), ('AD2', 'Administrador 2'), ('GG', 'Gerente General'), ('VR', 'Vendedor')], max_length=3)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.BooleanField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questions.Question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Questions.Personal')),
            ],
            options={
                'unique_together': {('question', 'user')},
            },
        ),
    ]