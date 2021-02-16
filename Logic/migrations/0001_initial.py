# Generated by Django 3.1 on 2021-01-15 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Konkurs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat', models.IntegerField()),
                ('start', models.BooleanField()),
                ('num', models.IntegerField()),
                ('organaiser', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('u_id', models.IntegerField()),
                ('konkurs_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('author', models.CharField(max_length=400)),
                ('author_id', models.IntegerField()),
                ('author_nick', models.CharField(max_length=400)),
                ('image_id', models.CharField(max_length=1000000000)),
                ('konkurs_id', models.IntegerField()),
                ('votes', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
